# The Redbox Appliance

A Vagrant box for developing Magento websites.

## Installation

We are in the process of getting a better installation set up than
this, preferably via the Vagrant Cloud. But for now,

```
git clone git@github.com:redbox-digital/magento-virtual-appliance.git
cd magento-virtual-appliance
vagrant up
vagrant package --output=/tmp/rbd_appliance.box
vagrant box add -f --name="rbd/appliance" /tmp/rbd_appliance.box
```

## What's Inside?

- PHP 5.4, with everything needed to run Magento
- Percona 5.5
- Nginx, configured to run one Magento site.
- Vim, Git, and N98-Magerun (by extension, Composer)
- Compass 0.12
- Fabric, for automating all the things.

The web root is configured to be `/var/www/magento/htdocs`, all requests
to port 80 are forwarded there. Of course, Magento validates the
`base_url`, so be sure to edit your hosts file to give it something.
