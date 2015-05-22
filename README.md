# The Redbox Appliance

A Vagrant box for developing Magento websites.

## Installation

The box can be found on [Atlas][atlas].

```
vagrant init redbox-digital/appliance
vagrant up
```

## What's Inside?

- CentOS 6.
- PHP 5.5, with everything needed to run Magento;
- Percona 5.6;
- Nginx, configured to run one Magento site;
- Vim, Git, Composer, N98-Magerun, Tmux and Jq;
- The Magento Project Mess Detector;
- NodeJS, NPM, Uglify, Bower, Grunt-CLI and Gulp;
- Compass;
- Fabric, for automating all the things.

The web root is configured to be `/var/www/magento/htdocs`, all requests
to port 80 are forwarded there. Of course, Magento validates the
`base_url`, so be sure to edit your hosts file to give it something
sensible.

[atlas]: https://atlas.hashicorp.com/redbox-digital/boxes/appliance

