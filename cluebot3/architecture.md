# ClueBot 3 Architecture

## Runtime dependencies

- `CLUEBOT3_BOT_PASSWORD` environment variable containing the Wiki account password

## Build dependencies

- https://github.com/cluebotng/wikipedia.git (managed via `composer.json`)

## Health checking

The job framework uses `health_check.php` which causes the pod (job) to be restarted if the bot hasn't edited within the last 24 hours.

A cron running on one of [https://en.wikipedia.org/wiki/User:DamianZaremba](Damian)'s servers checks the last contribution time,
updating [https://en.wikipedia.org/wiki/User:ClueBot_III/running](https://en.wikipedia.org/wiki/User:ClueBot_III/running) and emailing
[https://en.wikipedia.org/wiki/User:DamianZaremba](Damian) & [https://en.wikipedia.org/wiki/User:Rich_Smith](Rich) if the bot is not running.
