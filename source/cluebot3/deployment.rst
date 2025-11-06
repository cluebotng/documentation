Deployment
==========

The bot runs on `Toolforge <toolforge_>`_ (part of Wikimedia Cloud Services).

.. _toolforge: https://wikitech.wikimedia.org/wiki/Portal:Toolforge

There is currently only 1 (production) instance of the bot.

Production
----------

- Toolforge user: `cluebot3`
- Toolforge component/job: `cluebot3`

Setup
-----

We handle secrets using `envvars <envvars_url_>`_, which need to be created by hand prior to a deployment.

This should only be required if setting up a new account, or a secret needs to be rotated.

From within the tool account (see below)

.. code-block:: bash

    toolforge envvars create CLUEBOT3_BOT_PASSWORD
    Enter the value of your envvar (Hit Ctrl+C to cancel): <production password>

.. _envvars_url: https://wikitech.wikimedia.org/wiki/Help:Toolforge/Envvars

Deployment
----------

Deployments are handled via `components <deploy_url_>`_,
which coordinates building the image via `pack <pack_url_>`_ and running the component via `jobs <jobs_url_>`_.

.. _deploy_url: https://wikitech.wikimedia.org/wiki/Help:Toolforge/Deploy_your_tool
.. _jobs_url: https://wikitech.wikimedia.org/wiki/Help:Toolforge/Running_jobs
.. _pack_url: https://wikitech.wikimedia.org/wiki/Help:Toolforge/Building_container_images

Any tagged releases will be deployed via GitHub actions using `component-configs <component_configs_url_>`_.

.. _component_configs_url: https://github.com/cluebotng/component-configs/

Troubleshooting
---------------

First login to the tool account:

.. code-block:: bash

    $ ssh login.toolforge.org
    $ become cluebot3
    tools.cluebot3@tools-bastion-13:~$

Check the job is running
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    tools.cluebot3@tools-bastion-12:~$ toolforge jobs list
    +-----------+------------+---------+
    | Job name: | Job type:  | Status: |
    +-----------+------------+---------+
    | cluebot3  | continuous | Running |
    +-----------+------------+---------+

If the job is missing, check the recent deployment status

.. code-block:: bash

    tools.cluebot3@tools-bastion-15:~$ toolforge components deployment show
    Deployment ID: 20251104-171541-c2415tqylj
    Created: 20251104-171541
    Status: successful
    Long status:
      Finished at 2025-11-04 17:15:43.053902

    Builds:
      cluebot3(skipped): id:cluebot3-buildpacks-pipelinerun-45jbr Reusing existing build

    Runs:
      cluebot3(successful): job cluebot3 is already up to date, [info](Job cluebot3 is already up to date)

    Tool config:
      components:
        cluebot3:
          build:
            ref: refs/tags/v1.2.1
            repository: https://github.com/cluebotng/cluebot3.git
            use_latest_versions: true
          run:
            command: run-bot
            cpu: '3'
            health_check_script: health-check
            memory: 1Gi

Check the logs
______________

.. code-block:: bash

    toolforge jobs logs [--follow] cluebot3

For example:

.. code-block:: bash

    tools.cluebot3@tools-bastion-15:~$ toolforge jobs logs -f cluebot3
    2025-11-06T14:50:20Z [cluebot3-ffdc8f79c-l9k7m] [job] [2025-11-06 14:50:20] cluebot3.INFO: doarchive(Talk:CYP4F8,Talk:CYP4F8/Archive, %%i,17520,0,0,{{Talkarchive}},{{User:ClueBot III/ArchiveNow}},2,0,0,0,,0,1,) [] []
    2025-11-06T14:50:20Z [cluebot3-ffdc8f79c-l9k7m] [job] [2025-11-06 14:50:20] cluebot3.INFO: [Talk:CYP4F8] calculated sections: 0 old, 0 current, 0 keep, 0 archive [] []
    2025-11-06T14:50:20Z [cluebot3-ffdc8f79c-l9k7m] [job] [2025-11-06 14:50:20] cluebot3.INFO: [Talk:CYP4F8] generating index page [] []
    2025-11-06T14:50:22Z [cluebot3-ffdc8f79c-l9k7m] [job] [2025-11-06 14:50:22] cluebot3.INFO: doarchive(Talk:Eleanor of Castile (1307–1359),Talk:Eleanor of Castile (1307–1359)/Archive, %%i,2160,0,0,{{Talkarchive}},{{User:ClueBot III/ArchiveNow}},2,0,1,0,,150000,1,) [] []
    2025-11-06T14:50:22Z [cluebot3-ffdc8f79c-l9k7m] [job] [2025-11-06 14:50:22] cluebot3.INFO: [Talk:Eleanor of Castile (1307–1359)] calculated sections: 0 old, 0 current, 0 keep, 0 archive [] []
    2025-11-06T14:50:22Z [cluebot3-ffdc8f79c-l9k7m] [job] [2025-11-06 14:50:22] cluebot3.INFO: [Talk:Eleanor of Castile (1307–1359)] generating index page [] []
    2025-11-06T14:50:25Z [cluebot3-ffdc8f79c-l9k7m] [job] [2025-11-06 14:50:25] cluebot3.INFO: doarchive(Talk:United Way,Talk:United Way/Archive,,8760,0,0,{{Talkarchive}},{{User:ClueBot III/ArchiveNow}},2,0,0,0,,0,1,) [] []
    2025-11-06T14:50:25Z [cluebot3-ffdc8f79c-l9k7m] [job] [2025-11-06 14:50:25] cluebot3.INFO: [Talk:United Way] calculated sections: 0 old, 0 current, 0 keep, 0 archive [] []
    2025-11-06T14:50:25Z [cluebot3-ffdc8f79c-l9k7m] [job] PHP Warning:  Undefined array key "format" in /workspace/lib/bot.php on line 619
    2025-11-06T14:50:25Z [cluebot3-ffdc8f79c-l9k7m] [job] PHP Warning:  Undefined array key "format" in /workspace/lib/bot.php on line 640

Check the job status
____________________

.. code-block:: bash

    tools.cluebot3@tools-bastion-15:~$ toolforge jobs show cluebot3
    +---------------+------------------------------------------------------------------------+
    | Job name:     | cluebot3                                                               |
    +---------------+------------------------------------------------------------------------+
    | Command:      | run-bot                                                                |
    +---------------+------------------------------------------------------------------------+
    | Job type:     | continuous                                                             |
    +---------------+------------------------------------------------------------------------+
    | Image:        | tool-cluebot3/cluebot3:latest                                          |
    +---------------+------------------------------------------------------------------------+
    | Port:         | none                                                                   |
    +---------------+------------------------------------------------------------------------+
    | File log:     | no                                                                     |
    +---------------+------------------------------------------------------------------------+
    | Output log:   |                                                                        |
    +---------------+------------------------------------------------------------------------+
    | Error log:    |                                                                        |
    +---------------+------------------------------------------------------------------------+
    | Emails:       | none                                                                   |
    +---------------+------------------------------------------------------------------------+
    | Resources:    | mem: 1.0Gi, cpu: 3.0                                                   |
    +---------------+------------------------------------------------------------------------+
    | Replicas:     | 1                                                                      |
    +---------------+------------------------------------------------------------------------+
    | Mounts:       | none                                                                   |
    +---------------+------------------------------------------------------------------------+
    | Retry:        | no                                                                     |
    +---------------+------------------------------------------------------------------------+
    | Timeout:      | no                                                                     |
    +---------------+------------------------------------------------------------------------+
    | Health check: | script: health-check                                                   |
    +---------------+------------------------------------------------------------------------+
    | Status:       | Running                                                                |
    +---------------+------------------------------------------------------------------------+
    | Hints:        | Last run at 2025-10-29T10:32:03Z. Pod in 'Running' phase. Pod has been |
    |               | restarted 64 times. State 'running'. Started at                        |
    |               | '2025-11-06T14:43:35Z'.                                                |
    +---------------+------------------------------------------------------------------------+

Check the runtime (kubernetes)
______________________________

Sometimes jobs-api is not useful for debugging a failure within kubernetes (the runtime).

Kubernetes can be interrogated via the usual commands from the tool account e.g.:

- `kubectl get pod -l app.kubernetes.io/name=cluebot3`
- `kubectl describe pod -l app.kubernetes.io/name=cluebot3`
- `kubectl events`
