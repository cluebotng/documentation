Architecture
============

Runtime dependencies
--------------------

- `CLUEBOT3_BOT_PASSWORD` environment variable containing the Wiki account password

Build dependencies
------------------

- https://github.com/cluebotng/wikipedia.git (managed via `composer.json`)

Health checking
---------------

The runtime executes `health_check.php` which causes a restart if the bot hasn't edited within the last 24 hours.

The last edit time is exported via the `monitoring-probes <probes_repo_>`_,
with alerting via the `monitoring <monitoring_repo_>`_ setup.

.. _monitoring_repo: https://github.com/cluebotng/monitoring
.. _probes_repo: https://github.com/cluebotng/monitoring-probes
