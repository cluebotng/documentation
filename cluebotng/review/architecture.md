# ClueBot NG Review Interface Architecture

## Runtime dependencies

- `TOOL_TOOLSDB_USER` / `TOOL_TOOLSDB_PASSWORD` populated via the jobs framework with credentials
- `TOOL_REPLICA_USER` / `TOOL_REPLICA_PASSWORD` populated via the jobs framework with credentials
- `TOOL_TOOLSDB_SCHEMA` environment variable containing the database schema we use
- `REDIS_PASSWORD` environment variable containing password required to access the REDIS instance
- `PYTHONUNBUFFERED` environment variable preventing any command output from being buffered
- `DJANGO_SECRET_KEY` environment variable containing the Django secret key, used for session protection
- `OAUTH_KEY` environment variable containing the OAuth application key for user logins
- `OAUTH_SECRET` environment variable containing the OAuth application secret for user logins
- `WIKIPEDIA_USERNAME` environment variable containing the Wiki username used for publishing statistics and emailing users
- `WIKIPEDIA_PASSWORD` environment variable containing the Wiki password used for publishing statistics and emailing users

### IRC Relay dependencies
- `CBNG_RELAY_IRC_NICK` environment variable containing the username to use for SASL on Libera.Chat
- `CBNG_RELAY_IRC_PASSWORD` environment variable containing the password to use for SASL on Libera.Chat
- `CBNG_RELAY_IRC_CHANNELS` environment variable containing the channels to join (CSV)

## Runtime configuration
- `CBNG_ENABLE_IRC_MESSAGING` setting which controls if messages are emitted to the IRC Relay (`== "true"`)
- `CBNG_ENABLE_IRC_MESSAGING` setting which controls if emails are sent to users (via Wiki) (`== "true"`)

## Health checking

The job framework uses `/internal/health/` which causes the pod (job) to be restarted if the web stack is not functional.
