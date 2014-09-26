#! /bin/bash
# Compile all compass projects within a Magento project.

# Web root
cd /var/www/magento/htdocs

# All instances of config.rb, the compass config file
CONFIGS=`find -L skin/frontend -type f | grep "config.rb" | grep -v "rwd"`

# Compile each compass project
for config in $CONFIGS
do
  COMPASS_DIR=`dirname $config`

  compass clean $COMPASS_DIR
  compass compile $COMPASS_DIR -e "development"
done
