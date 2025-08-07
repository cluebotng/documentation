# ClueBot 3 Deployment

The bot runs as a [https://wikitech.wikimedia.org/wiki/Portal:Toolforge](Toolforge) job on Wikimedia Cloud Services.

There is currently only 1 (production) instance of the bot.

## Production

Toolforge user: `cluebot3`
Toolforge job: `cluebot3`

## Setup

We handle secrets using `envvars`, which need to be created by hand prior to a deployment.

This should only be required if setting up a new account, or a secret needs to be rotated.

From within the tool account (see below):
```
toolforge envvars create CLUEBOT3_BOT_PASSWORD
Enter the value of your envvar (Hit Ctrl+C to cancel): <production password>
```

## Deployment

The code is packaged as a container using pack (https://wikitech.wikimedia.org/wiki/Help:Toolforge/Building_container_images),
which is then deployed as a `continuous` job.

Any tagged release will be deployed via GitHub actions using (`https://github.com/cluebotng/cluebot3/blob/main/fabfile.py`)(fabric).

## Manual deployment

It can be useful to manually execute a deployment, for example when adjusting the `jobs.yaml` or `fabric.py` logic.

Assuming `fabric` is installed locally, within the root of the `cluebot3` repo you can directly execute:
* `fab deploy` - everything
* `fab deploy-jobs` - update only the `jobs` config

Note: This requires SSH access to the tool user account.

## Troubleshooting

First login to the tool account:
```
$ ssh login.toolforge.org
$ become cluebot3
tools.cluebot3@tools-bastion-13:~$ 
```

## Check the job is running
```
tools.cluebot3@tools-bastion-12:~$ toolforge jobs list
+-----------+------------+---------+
| Job name: | Job type:  | Status: |
+-----------+------------+---------+
| cluebot3  | continuous | Running |
+-----------+------------+---------+
```

If the job is not running, check the logs, or investigate the pod status (`kubectl get pod <pod name>`, `kubectl logs <pod name>`, `kubectl events`).

## Check the logs
```
toolforge jobs logs [--follow] cluebot3
```

For example:
```
tools.cluebot3@tools-bastion-12:~$ toolforge jobs logs cluebot3 | tail -n 10
2025-08-07T14:36:32+00:00 [cluebot3-7c774d569b-ndhsz] [job] Stack trace:
2025-08-07T14:36:32+00:00 [cluebot3-7c774d569b-ndhsz] [job] #0 /workspace/vendor/monolog/monolog/src/Monolog/Handler/StreamHandler.php(104): Monolog\Handler\StreamHandler->createDir()
2025-08-07T14:36:32+00:00 [cluebot3-7c774d569b-ndhsz] [job] #1 /workspace/vendor/monolog/monolog/src/Monolog/Handler/RotatingFileHandler.php(120): Monolog\Handler\StreamHandler->write()
2025-08-07T14:36:32+00:00 [cluebot3-7c774d569b-ndhsz] [job] #2 /workspace/vendor/monolog/monolog/src/Monolog/Handler/AbstractProcessingHandler.php(39): Monolog\Handler\RotatingFileHandler->write()
2025-08-07T14:36:32+00:00 [cluebot3-7c774d569b-ndhsz] [job] #3 /workspace/vendor/monolog/monolog/src/Monolog/Logger.php(344): Monolog\Handler\AbstractProcessingHandler->handle()
2025-08-07T14:36:32+00:00 [cluebot3-7c774d569b-ndhsz] [job] #4 /workspace/vendor/monolog/monolog/src/Monolog/Logger.php(422): Monolog\Logger->addRecord()
2025-08-07T14:36:32+00:00 [cluebot3-7c774d569b-ndhsz] [job] #5 /workspace/lib/bot.php(610): Monolog\Logger->addInfo()
2025-08-07T14:36:32+00:00 [cluebot3-7c774d569b-ndhsz] [job] #6 /workspace/cluebot3.php(69): ClueBot3\parsetemplate()
2025-08-07T14:36:32+00:00 [cluebot3-7c774d569b-ndhsz] [job] #7 {main}
2025-08-07T14:36:32+00:00 [cluebot3-7c774d569b-ndhsz] [job]   thrown in /workspace/vendor/monolog/monolog/src/Monolog/Handler/StreamHandler.php on line 189
```
