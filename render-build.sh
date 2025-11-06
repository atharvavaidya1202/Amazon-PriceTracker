#!/usr/bin/env bash
# render-build.sh
set -o errexit

echo "Installing Python 3.11.9 manually..."
pyenv install -s 3.11.9
pyenv global 3.11.9
python --version

pip install -r requirements.txt
