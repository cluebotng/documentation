# ClueBot NG Report Interface Deployment

The interface runs as a [Toolforge](https://wikitech.wikimedia.org/wiki/Portal:Toolforge) job on Wikimedia Cloud Services.

There is currently a production (deployed from a `vN.N.N` tag) and staging (deployed from `main`) instance.

## Toolforge users

Production: `cluebot`
Staging: `cluebot-staging`

## Setup

We handle secrets using `envvars`, which need to be created by hand prior to a deployment.

This should only be required if setting up a new account, or a secret needs to be rotated.

From within the tool account (see below):
```
toolforge envvars create TOOL_TOOLSDB_SCHEMA
Enter the value of your envvar (Hit Ctrl+C to cancel): <production password>
```

Note:
The `_update_report` fabric task creates the `service.template` file which `webservice` needs to find the correct image/commands.
If attempting to deploy by hand (e.g. by `webservice start` additional flags will need to be passed).

## Deployment

The code is packaged as a container using pack ([https://wikitech.wikimedia.org/wiki/Help:Toolforge/Building_container_images](https://wikitech.wikimedia.org/wiki/Help:Toolforge/Building_container_images)),
which is then deployed as a `webservice` job.

Any tagged release will be deployed via GitHub actions using [fabric](https://github.com/cluebotng/utilities/blob/main/fabfile.py).

### Logs
The "component" fabric tasks will log to SAL via `dologmsg`, recent changes can be seen at [https://wikitech.wikimedia.org/wiki/Nova_Resource:Tools.cluebot/SAL](https://wikitech.wikimedia.org/wiki/Nova_Resource:Tools.cluebot/SAL).

## Manual deployment

It can be useful to manually execute a deployment, for example when adjusting the `jobs.yaml` or `fabric.py` logic.

Assuming `fabric` is installed locally, within the root of the `utilities` repo you can directly execute tasks.
* `fab deploy-report` - build a new container image and restart the web service

To target the staging account you can specify `TARGET_USER=cluebotng-staging`.

Note: This requires SSH access to the tool user account.

## Troubleshooting

First login to the tool account:
```
$ ssh login.toolforge.org
$ become cluebotng
tools.cluebotng@tools-bastion-13:~$ 
```

## Check the job is running
```
tools.cluebotng@tools-bastion-12:~$ webservice status
Your webservice of type buildservice is running on backend kubernetes
```

If the webservice is not running, check the logs, or investigate the pod status (`kubectl get pod <pod name>`, `kubectl logs <pod name>`, `kubectl events`).

## Check the logs
```
webservice logs [--follow]
```

For example:
```
$ webservice logs | tail -n 2
2025-08-08T14:04:23+00:00 [cluebotng-6944f9cf8-7lqf7] 192.168.254.255 - - [08/Aug/2025:14:04:23 +0000] "GET /?id=3350067&page=View HTTP/1.1" 302 - "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.2210.137 Safari/537.36
2025-08-08T14:04:24+00:00 [cluebotng-6944f9cf8-7lqf7] 192.168.36.101 - - [08/Aug/2025:14:04:24 +0000] "GET /?page=Report&id=3350067 HTTP/1.1" 200 10563 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.2210.137 Safari/537.36
```
