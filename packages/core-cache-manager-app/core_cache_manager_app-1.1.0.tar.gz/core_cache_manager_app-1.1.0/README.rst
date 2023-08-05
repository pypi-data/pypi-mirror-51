Core Cache Manager App
======================

Cache management feature for the curator core project.


Configuration
=============

1. Add "core_cache_manager_app" to your INSTALLED_APPS setting like this
------------------------------------------------------------------------

.. code:: python

    INSTALLED_APPS = [
        ...
        "core_cache_manager_app",
    ]

2. Include the core_cache_manager_app URLconf in your project urls.py like this
-------------------------------------------------------------------------------

.. code:: python

    url(r'^', include("core_cache_manager_app.urls")),
