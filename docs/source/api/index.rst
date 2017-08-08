.. _api-index:

##################
The JupyterHub API
##################

:Release: |release|
:Date: |today|

JupyterHub also provides a REST API for administration of the Hub and users.
The `Using JupyterHub's REST API <../rest.html>`_ section gives information
about:

- what you can do with the API
- creating an API token
- adding API tokens to the config files
- making an API request programmatically using the requests library
- learning more about JupyterHub's API

An interactive version of the `JupyterHub API`_ using the `OpenAPI Initiative`_
(fka Swagger™) specification describes and documents the RESTful API.

JupyterHub API and Source Code Reference
----------------------------------------

.. toctree::

    app
    auth
    spawner
    proxy
    user
    service-api
    services.auth


.. _OpenAPI Initiative: https://www.openapis.org/
.. _JupyterHub API: http://petstore.swagger.io/?url=https://raw.githubusercontent.com/jupyterhub/jupyterhub/master/docs/rest-api.yml#!/default