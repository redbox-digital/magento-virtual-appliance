# The Redbox Appliance

A Vagrant box for developing Magento websites.

## Installation

We are in the process of getting a better installation set up than
this, preferably via the Vagrant Cloud. But for now,

```
vagrant init redbox-digital/appliance
vagrant up
```

## What's Inside?

- CentOS 6.
- PHP 5.4, with everything needed to run Magento;
- Percona 5.5;
- Nginx, configured to run one Magento site;
- Vim, Git, Composer, N98-Magerun;
- Compass 0.12;
- Fabric, for automating all the things.

The web root is configured to be `/var/www/magento/htdocs`, all requests
to port 80 are forwarded there. Of course, Magento validates the
`base_url`, so be sure to edit your hosts file to give it something.
