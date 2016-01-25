# JupyterHub: A multi-user server for Jupyter notebooks

Questions, comments? Visit our Google Group:

[![Google Group](https://img.shields.io/badge/-Google%20Group-lightgrey.svg)](https://groups.google.com/forum/#!forum/jupyter)
[![Build Status](https://travis-ci.org/jupyter/jupyterhub.svg?branch=master)](https://travis-ci.org/jupyter/jupyterhub)
[![CircleCI](https://circleci.com/gh/jupyter/jupyterhub.svg?style=shield&circle-token=:circle-token](https://circleci.com/gh/jupyter/jupyterhub)

[![Documentation Status](https://readthedocs.org/projects/jupyterhub/badge/?version=latest)](http://jupyterhub.readthedocs.org/en/latest/?badge=latest)

JupyterHub, a multi-user server, manages and proxies multiple instances of the single-user <del>IPython</del> Jupyter notebook server.

Three actors:

- multi-user Hub (tornado process)
- configurable http proxy (node-http-proxy)
- multiple single-user IPython notebook servers (Python/IPython/tornado)

Basic principles:

- Hub spawns proxy
- Proxy forwards ~all requests to hub by default
- Hub handles login, and spawns single-user servers on demand
- Hub configures proxy to forward url prefixes to single-user servers


## Dependencies

JupyterHub requires [IPython](https://ipython.org/install.html) >= 3.0 (current master) and [Python](https://www.python.org/downloads/) >= 3.3.

Install [nodejs/npm](https://www.npmjs.com/), which is available from your
package manager. For example, install on Linux (Debian/Ubuntu) using:

    sudo apt-get install npm nodejs-legacy

(The `nodejs-legacy` package installs the `node` executable and is currently
required for npm to work on Debian/Ubuntu.)

Next, install JavaScript dependencies:

    sudo npm install -g configurable-http-proxy

### (Optional) Installation Prerequisite (pip)

Notes on the `pip` command used in the installation directions below:
- `sudo` may be needed for `pip install`, depending on the user's filesystem permissions.
- JupyterHub requires Python >= 3.3, so `pip3` may be required on some machines for package installation instead of `pip` (especially when both Python 2 and Python 3 are installed on a machine). If `pip3` is not found, install it using (on Linux Debian/Ubuntu):

        sudo apt-get install python3-pip


## Installation

JupyterHub can be installed with pip:

    pip3 install jupyterhub

If you plan to run notebook servers locally, you may also need to install the
Jupyter ~~IPython~~ notebook:

    pip3 install notebook


### Development install

For a development install, clone the repository and then install from source:

    git clone https://github.com/jupyter/jupyterhub
    cd jupyterhub
    pip3 install -r dev-requirements.txt -e .

If the `pip3 install` command fails and complains about `lessc` being unavailable, you may need to explicitly install some additional JavaScript dependencies:

    npm install

This will fetch client-side JavaScript dependencies necessary to compile CSS.

You may also need to manually update JavaScript and CSS after some development updates, with:

    python3 setup.py js    # fetch updated client-side js (changes rarely)
    python3 setup.py css   # recompile CSS from LESS sources


## Running the server

To start the server, run the command:

    jupyterhub

and then visit `http://localhost:8000`, and sign in with your unix credentials.

To allow multiple users to sign into the server, you will need to
run the `jupyterhub` command as a *privileged user*, such as root.
The [wiki](https://github.com/jupyter/jupyterhub/wiki/Using-sudo-to-run-JupyterHub-without-root-privileges)
describes how to run the server as a *less privileged user*, which requires more
configuration of the system.

## Getting started

See the [getting started document](docs/source/getting-started.md) for the
basics of configuring your JupyterHub deployment.

### Some examples

Generate a default config file:

    jupyterhub --generate-config

Spawn the server on ``10.0.1.2:443`` with **https**:

    jupyterhub --ip 10.0.1.2 --port 443 --ssl-key my_ssl.key --ssl-cert my_ssl.cert

The authentication and process spawning mechanisms can be replaced,
which should allow plugging into a variety of authentication or process control environments.
Some examples, meant as illustration and testing of this concept:

- Using GitHub OAuth instead of PAM with [OAuthenticator](https://github.com/jupyter/oauthenticator)
- Spawning single-user servers with Docker, using the [DockerSpawner](https://github.com/jupyter/dockerspawner)

# Getting help

We encourage you to ask questions on the mailing list:

[![Google Group](https://img.shields.io/badge/-Google%20Group-lightgrey.svg)](https://groups.google.com/forum/#!forum/jupyter)

and you may participate in development discussions or get live help on Gitter:

[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/jupyter/jupyterhub?utm_source=badge&utm_medium=badge)

## Resources
- [Project Jupyter website](https://jupyter.org)
- [Documentation for JupyterHub](http://jupyterhub.readthedocs.org/en/latest/) [[PDF](https://media.readthedocs.org/pdf/jupyterhub/latest/jupyterhub.pdf)]
- [Documentation for Project Jupyter](http://jupyter.readthedocs.org/en/latest/index.html) [[PDF](https://media.readthedocs.org/pdf/jupyter/latest/jupyter.pdf)]
- [Issues](https://github.com/jupyter/jupyterhub/issues)
- [Technical support - Jupyter Google Group](https://groups.google.com/forum/#!forum/jupyter)
