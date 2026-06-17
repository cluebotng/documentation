# ClueBot NG Report Interface Architecture

## Runtime dependencies

- `TOOL_TOOLSDB_USER` / `TOOL_TOOLSDB_PASSWORD` populated via the jobs framework with credentials
- `TOOL_TOOLSDB_SCHEMA` environment variable containing the database schema also configured on the bot
- `OAUTH_KEY` environment variable containing the OAuth application key for user logins
- `OAUTH_SECRET` environment variable containing the OAuth application secret for user logins

Note: It is implied that the `bot` and `report` run under the same account, at a minimum they need to share the database.

## Health checking

The job framework uses `/api/?action=health.check` which causes the pod (job) to be restarted if the web stack is not functional.
