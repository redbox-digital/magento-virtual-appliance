import hashlib
import json
import os

from xml.etree import ElementTree
from fabric.api import local, env, run, get, cd, lcd, task

project_root = '/var/www/magento'
magento_root = os.path.join(project_root, 'htdocs')
config = json.load(open(os.path.join(project_root, 'config.json')))

env.hosts = [config['ssh_host']]
env.port = config['ssh_port']
env.user = config['ssh_username']

# Set up SSH for password or certificate based authentication
env.password = config['ssh_password'] or None
if config['ssh_certificate']:
    env.key_filename = os.path.join('/vagrant', config['ssh_certificate'])
else:
    env.key_filename = None

def random_filename(extension):
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
        local('n98-magerun install --installationFolder . --installSampleData --noDownload --dbHost="localhost" --dbUser="root" --dbPass="" --dbName="mage_local" --dbPort="3306" --no-interaction --baseUrl="http://magento.local/"')

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
def configure():
    """Grab bag of things that need doing.

    Note that arbitrary config settings can be added in config.json,
    under "other_config"
    """
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
    global project_root
    project_root = '/var/www/magento'

    global magento_root
    magento_root = '/var/www/magento/htdocs'

    clean_up()
    git_clone()
    install()
