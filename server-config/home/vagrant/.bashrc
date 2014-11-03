# Source global definitions
if [ -f /etc/bashrc ]; then
  source /etc/bashrc
fi

# Add global composer binaries to runtime path
export PATH="~/.composer/vendor/bin:$PATH"
