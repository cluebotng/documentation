# ClueBot NG Review Interface Deployment

The interface runs as a [Toolforge](https://wikitech.wikimedia.org/wiki/Portal:Toolforge) job on Wikimedia Cloud Services.

There is currently only 1 (production) instance of the review interface.

There is currently a production (deployed from a `vN.N.N` tag) and staging (deployed from `main`) instance.

Toolforge user: `cluebotng-review-review`

## Setup

We handle secrets using `envvars`, which need to be created by hand prior to a deployment.

This should only be required if setting up a new account, or a secret needs to be rotated.

From within the tool account (see below):
```
toolforge envvars create TOOL_TOOLSDB_SCHEMA
Enter the value of your envvar (Hit Ctrl+C to cancel): <production password>
```

Note:
The `__update_jobs` fabric task creates the `service.template` file which `webservice` needs to find the correct image/commands.
If attempting to deploy by hand (e.g. by `webservice start` additional flags will need to be passed).

## Deployment

The code is packaged as a container using pack ([https://wikitech.wikimedia.org/wiki/Help:Toolforge/Building_container_images](https://wikitech.wikimedia.org/wiki/Help:Toolforge/Building_container_images)),
which is then deployed as a `webservice` job.

Any tagged release will be deployed via GitHub actions using [fabric](https://github.com/cluebotng-review/reviewer/blob/main/fabfile.py).

## IRC Relay
Until [T400024](https://phabricator.wikimedia.org/T400024) lands, anytime the `irc-relay` job is re-created the `Deployment` and `Service` objects need to be manually edited:

Run `kubectl edit service irc-relay` and change `TCP` to `UDP` in the port section.

Run `kubectl edit deployment irc-relay`, change `TCP` to `UDP` in the port section and remove the `startupProbe` and `readinessProbe` sections.

Without performing this steps, no messages will be received by the relay & it will be killed in a loop.

### Logs
The "component" fabric tasks will log to SAL via `dologmsg`, recent changes can be seen at [https://wikitech.wikimedia.org/wiki/Nova_Resource:Tools.cluebotng-review-review/SAL](https://wikitech.wikimedia.org/wiki/Nova_Resource:Tools.cluebotng-review-review/SAL).

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
$ become cluebotng-review
tools.cluebotng-review@tools-bastion-13:~$ 
```

## Check the interface is running
```
tools.cluebotng-review@tools-bastion-12:~$ webservice status
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
2025-08-08T10:45:30+00:00 [cluebotng-review-b65c6d95b-vqbpb] 2025-08-08 10:45:30,940 WARNING log.py log_response: Not Found: /favicon.ico
2025-08-08T12:21:58+00:00 [cluebotng-review-b65c6d95b-vqbpb] 2025-08-08 12:21:58,351 INFO irc.py send_message: Sending to IRC Relay: b'#wikipedia-en-cbngreview:\x0314[[\x0303 New User Account \x0314]]\x0301 ActivelyDisinterested\n'
```
