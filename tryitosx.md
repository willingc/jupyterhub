# Trying out JupyterHub on OS X

## Prerequisite (Python)
Install Python version 3.5.1. See python.org

## Create a project directory
mkdir myhub
cd myhub

## Create a Python virtual environment
pyenv testhub
source testhub/bin/activate

## Install node and npm
npm install -g config-http-proxy

## Install jupyterhub
pip install jupyterhub

## Install notebook locally
pip install --upgrade notebook

## Run jupyterhub
jupyterhub

## Navigate in browser
Go to https://127.0.0.1:8000
Sign in and you can user the notebook
