# ClueBot NG Report Interface Data Flows

There are primarily 3 parties interacting with the interface:

* Reporter - who can create `report` entries based on `vandalism` entries
* Admin - human who reviews the reports
* Review interface - imports `report` entries that are "Sent to Review" and exports `report` status for reviewed edits

Additionally, there are a number of "API" endpoints designed for more programmatic access and/or checking data without having to use the database directly.

## Authentication

* Admin users must be authenticated (via OAuth)
* Reporters can be authenticated or anonymous
* Review updates are pulled, so no authentication is required

## Granting admin rights

There are 2 primary methods for a user obtaining `admin` rights:

* A `superadmin` explicitly grants the rights to an account that has previously logged in
* On login the enwiki API reports the user as having `rollback`, `block`, `deleterevision` or `editprotected` rights (user has some level of trust)

## Data population

### Bot tables
* `vandalism` entries are created by the `bot` instance and read by the `report` interface

### Additional tables (created in bot schema)
* `users` entries are created by the `report` interface on user sign in and is used to track association with entries and store preferences
* `report`, `comment` entries are created by the `report` interface from interactions with Reporters, Admins or the Review Interface
* `edits_sent_for_review` is populated from a `report` being set to "Sent to Review Interface", it is consumed by the Review Interface to associate users

### Spam/vandalism measures

* Anonymous users can leave 1 comment during the process of create a `report`, no additional `comment` entries can be made
* Authenticated users can comment on any `report`.

## Review Interface Interactions

There are 3 `report` endpoints which support passing data between the `report` and `review` interface:

* API `review.import` - Called via cron to query the review interface API and change `report` statuses
* API `report.export` - Called from the review interface and returns all `report` entries in "Sent to Review Interface" (note: `review.import` will change the status from this, so this "new edits")
* API `report.export_user` - Called from the review interface and returns all `user` entries related to a `report` (note: used by the review interface to auto-create review entries for admins who are also a reviewer)
