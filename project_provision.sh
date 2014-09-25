#! /bin/bash

project="screwfix-ie"

cd /var/www/magento

git clone git@bitbucket.org:redbox-digital/projects-$project.git .
git checkout appliance

cd
fab init


