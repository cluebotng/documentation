# ClueBot NG Review Interface Data Flows

The data is the most important asset in the review interface.

General aims:
* Minimise bias for reviewers (e.g. do not show other user classifications)
* Establish a clear positive signal for edit classification
* Persist metadata and revisions for training (even in the case that the edit is later deleted)

The "heavy lifting" such as update an Edit's classification is done as a background task.

## Async support

We are utilising `Celery` to trigger async task execution from the web interface.

Any tasks are messaged via a `redis` instance running under the tool account (`redis` job).

A single worker instance is run under the `celery-worker` job and is restarted on each deploy.

### Backfill jobs

In addition to 'real time' tasks, we also process the edits via scheduled commands, ensuring they are not missed via the async workflow.

## Scheduled tasks

There are a number of scheduled tasks, defined in [configs/jobs.yaml](https://github.com/cluebotng/reviewer/blob/main/configs/jobs.yaml).

They can be broadly broken down into 3 groups:

### Core jobs
* add_edits_to_queue
* add_reported_edits
* add_reviews_from_huggle
* add_reviews_from_report
* export_statistics

### Edit maintenance
* mark_edits_as_deleted
* update_edit_classification (run async)
* import_training_data (run async)


### Cleanup jobs
* add_dangling_edits_to_group
* grant_review_access_from_rights
* mark_edits_with_training_data
* cleanup_user_records

## Management commands

There are some helper commands for management actions, especially useful during development.

* make_user_admin [--super]
* make_user_reviewer
* setup_with_historical_data

These can be run in production from the tool user:
Via the `jobs` framework:
```
toolforge jobs run --wait --image tool-cluebotng-review/tool-cluebotng-review:latest --command "./manage.py make_user_admin DamianZaremba" --wait some-random-admin-task
```

Or interactively via `kubectl`:
```
kubectl exec -ti $(kubectl get pods | grep cluebotng-review- | grep Running | head -n1 | awk '{print $1}') -- launcher ./manage.py
```

Note: The standard Django tools such as `shell` exist, be very careful as it is easy to mess up the data.
It is preferable prefer to write a management command with test cover, even for a temp/migration job.
