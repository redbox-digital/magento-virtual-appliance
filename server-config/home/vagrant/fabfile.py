import hashlib
import json
import os

from xml.etree import ElementTree
from fabric.api import local, env, run, get, cd, lcd, task

project_root = '/var/www/magento'
magento_root = os.path.join(project_root, 'htdocs')
config = json.load(open(os.path.join(project_root, 'config.json')))

env.hosts = [config.get('ssh_host')] if config.get('ssh_host') else []
env.port = config.get('ssh_port')
env.user = config.get('ssh_username')

# Set up SSH for password or certificate based authentication
env.password = config.get('ssh_password')
if config.get('ssh_certificate'):
    env.key_filename = os.path.join('/vagrant', config['ssh_certificate'])
else:
    env.key_filename = None

def random_filename(extension):
    """A random filename (with optional extension)"""
    extension = '.' + extension if extension else ''
    return hashlib.md5(os.urandom(64)).hexdigest() + extension

@task
def clean_up():
    """Remove the project directory to get ready."""
    local('/bin/rm -rf %s' % magento_root)
    local('/bin/rm -rf %s/vendor' % project_root)

@task
def git_clone():
    """Clone a clean Magento installation into htdocs."""
    with lcd(project_root):
        local('git clone %s htdocs' % config['magento_mirror'])
    with lcd(magento_root):
        local('git checkout "%s"' % config['magento_version'])
    local('/bin/rm -rf .git composer.json')

@task
def install():
    """Run the install command and install sample data."""
    with lcd(magento_root):
        local('n98-magerun.phar install --installationFolder . --installSampleData --noDownload --dbHost="localhost" --dbUser="root" --dbPass="" --dbName="mage_local" --dbPort="3306" --admin-password="pass1234" --no-interaction --baseUrl="%s"' % config.get('base_url', 'http://magento.local/')')

@task
def get_local_xml():
    local('cp %s/localdotxml/local.xml.local %s/app/etc/local.xml' %
            (project_root, magento_root))

@task
def get_media_dump():
    """SSH to remote server and get media folder.

    This uses the magical N98-Magerun, and it needs to be a fairly
    recent version, so make sure that it's installed somewhere globally
    accessible.

    In config.json, there is a field to supply the path to it, so there
    really is no excuse.

    The dump is then downloaded and unzipped into the Magento instance.
    """
    media_filename = random_filename('zip')
    media_location = os.path.join(config['tmp_dir'], media_filename)

    with cd(config['magento_root']):
        run('%s media:dump --strip %s' %
                (config['magerun'], media_location))

        get(remote_path=media_location, local_path='/tmp')

    with lcd('/tmp'):
        local('unzip %s' % media_filename)
        local('cp -r media %s' % magento_root)

@task
def create_database():
    """Create the database specified locally."""
    with lcd(magento_root):
        local('n98-magerun.phar db:create')

@task
def get_database_dump():
    """Get a database dump from the server.

    This dumps the data and imports it, assuming that the database
    has been created.
    """
    db_filename = random_filename('sql')
    db_location = os.path.join(config['tmp_dir'], db_filename)
    with cd(config['magento_root']):
        run('%s db:dump -f %s' %
                (config['magerun'], db_location))

        get(remote_path=db_location, local_path='/tmp')

    with lcd(magento_root):
        local('n98-magerun.phar db:import %s' % '/tmp/' + db_filename)

@task
def install_dependencies():
    """Run composer.phar update."""
    with lcd(project_root):
        local('composer.phar install --no-dev')

@task
def generate_composer_json():
    """Install Magento with all a module's dependencies"""
    composer_json_location = os.path.join(project_root, 'src/composer.json')
    composer_json = json.load(open(composer_json_location))

    # Get only the repositories with a type.
    repositories = [repo for repo in composer_json.get('repositories', []) if repo.get('type') != None]

    # Preformatted strings of package:version
    require = ' '.join(['%s:%s' % req
        for req in composer_json.get('require', dict()).items()])

    require_dev = ' '.join(['%s:%s' % req
        for req in composer_json.get('require-dev', dict()).items()])

    with lcd(project_root):
        # Make a completely emtpy composer.json
        local('composer.phar init --no-interaction')

        # Add in all repositories specified in the module
        local('composer.phar config repositories.firegento composer http://packages.firegento.com')
        for idx, repo in enumerate(repositories):
            local('composer.phar config repositories.%s %s %s' %
                    (str(idx), repo['type'], repo['url']))

            # Require everything
        local('composer.phar require --no-interaction --no-update magento-hackathon/magento-composer-installer:~2')
        local('composer.phar require --no-interaction --no-update %s' % require)
        local('composer.phar require --no-interaction --no-update --dev %s' % require_dev)

        # Add the correct extra stuff
        # - magento-root-dir
        # Composer doesn't support arbitrary addition of stuff to
        # extra. A better way might be a template composer.json,
        # rather than `composer.phar init`.
        extra = { 'magento-root-dir': 'htdocs/' }
        with open(os.path.join(project_root, 'composer.json'), 'r+') as comp:
            comp_json = json.load(comp)
            comp_json['extra'] = extra
            comp.truncate(0)
            comp.seek(0)
            comp.write(json.dumps(comp_json, indent=4, separators=(',', ': ')))

@task
def install_module():
    """Install a module.

    Look at the mappings in composer.json and apply the symlinks.
    """
    composer_json_location = os.path.join(project_root, 'src/composer.json')
    composer_json = json.load(open(composer_json_location))

    mappings = composer_json['extra'].get('map', [])

    for mapping in mappings:
        src = os.path.join(project_root, 'src', mapping[0])
        dest = os.path.join(magento_root, mapping[1])

        local('mkdir -p %s' % os.path.dirname(dest))
        local('ln -s %s %s' % (src, dest))

@task
def configure():
    """Grab bag of things that need doing."""
    with lcd(magento_root):
        local('n98-magerun.phar script < %s/n98/n98-config-script.txt.local' %
                project_root)

@task
def compass():
    """Compile all compass projects."""
    with lcd('~'):
        local('./compass_compile.sh')

@task
def clean_cache():
    """Flush Magento caches."""
    with lcd(magento_root):
        local('n98-magerun.phar cache:flush')

@task
def init():
    """All together now (!)"""
    clean_up()
    git_clone()
    get_local_xml()
    get_media_dump()
    create_database()
    get_database_dump()
    install_dependencies()
    configure()
    compass()
    clean_cache()


@task
def init_vanilla():
    """Install a vanilla version of magento"""
    clean_up()
    git_clone()
    install()
    generate_composer_json()
    install_dependencies()
    install_module()
