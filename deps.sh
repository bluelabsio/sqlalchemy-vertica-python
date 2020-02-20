#!/bin/bash -e


if [ "$(uname)" == Darwin ]
then
  brew update && ( brew upgrade pyenv || true )
fi

python_version=3.8.1
# zipimport.ZipImportError: can't decompress data; zlib not available:
#    You may need `xcode-select --install` on OS X
#    https://github.com/pyenv/pyenv/issues/451#issuecomment-151336786
pyenv install -s "${python_version:?}"
if [ "$(uname)" == Darwin ]
then
  # Python has needed this in the past when installed by 'pyenv
  # install'.  The current version of 'psycopg2' seems to require it
  # now, but Python complains when it *is* set.  🤦
  CFLAGS="-I$(brew --prefix openssl)/include"
  export CFLAGS
  LDFLAGS="-L$(brew --prefix openssl)/lib"
  export LDFLAGS
fi
pyenv virtualenv "${python_version:?}" sqlalchemy-vertica-python-"${python_version:?}" || true
pyenv local sqlalchemy-vertica-python-"${python_version:?}"

pip3 install --upgrade pip

pip3 install -r requirements.txt -e .
