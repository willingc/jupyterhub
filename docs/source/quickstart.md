# Quickstart

This section provides brief steps on installing JupyterHub:

- Prerequisites
- Installing JupyterHub
- Starting the Hub server
- Signing in to the Hub

We *recommend* reading the complete installation section of the User Guide and
the Configuration Guide before beginning a deployment.
The JupyterHub **tutorial** provides a video and documentation that explains
and illustrates the fundamental steps for installation and configuration.
[Repo](https://github.com/jupyterhub/jupyterhub-tutorial)
| [Tutorial documentation](http://jupyterhub-tutorial.readthedocs.io/en/latest/)


## Prerequisites

- [Python](https://www.python.org/downloads/) 3.3 or greater

  An understanding of using [`pip`](https://pip.pypa.io/en/stable/) or
  [`conda`](http://conda.pydata.org/docs/get-started.html) for
  installing Python packages is helpful.

- [nodejs/npm](https://www.npmjs.com/)
  [Install nodejs/npm](https://docs.npmjs.com/getting-started/installing-node),
  using your operating system's package manager.

  For example, install on Linux (Debian/Ubuntu) using:

  ```bash
  sudo apt-get install npm nodejs-legacy
  ```
  
  (The `nodejs-legacy` package installs the `node` executable and is currently
  required for npm to work on Debian/Ubuntu.)

- TLS certificate and key for HTTPS communication

- Domain name

Before running the single-user notebook servers (which may be on the same
system as the Hub or not):

- [Jupyter Notebook](https://jupyter.readthedocs.io/en/latest/install.html)
  version 4 or greater


## Installing JupyterHub

JupyterHub can be installed with `pip` or `conda`:

**pip (npm is used to install the proxy)**
```bash
python3 -m pip install jupyterhub
npm install -g configurable-http-proxy
```

**conda** (one command installs jupyterhub and proxy):
```bash
conda install -c conda-forge jupyterhub
```

Test your installation:

```bash
jupyterhub -h
configurable-http-proxy -h
```

To run notebook servers locally, you will need to install Jupyter notebook:

**pip:**
```bash
python3 -m pip install notebook
```

**conda:**
```bash
conda install notebook
```


## Starting the Hub server

To start the Hub server, run the command:

```bash
jupyterhub
```


## Signing in to the Hub

Visit `https://localhost:8000` in your browser, and sign in with your unix
credentials.

To allow multiple users to sign into the Hub server, start `jupyterhub`
as a **privileged user**, such as root:

```bash
sudo jupyterhub
```

The [wiki](https://github.com/jupyterhub/jupyterhub/wiki/Using-sudo-to-run-JupyterHub-without-root-privileges)
describes how to run the Hub server as a *less privileged user*, which requires
additional configuration of the Hub.