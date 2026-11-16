# Deployment Tooling

General ideas:

* We try and use the support configuration on Wikimedia Cloud Services.
* Account configuration should be scripted, allowing easy re-creation
* Secrets are managed by a human and stored securely (envars or permissions)

Current limitations:

* No supported API client for toolforge [T356261 / T356377 / T321919]
* No supported authentication outside of tool certificates [T363983]
* Missing language support in container builds [T401075]
* No support for web services in components [T362077]
* No support for specifying refs in deployment triggers [T401388]
* No support for latest build packs in components [T380127]
* Quotas

Tooling:

* Use language specific tools within repo (`composer`, `poetry`)
* Wrap shell executions with `fabric` to provide "composable actions"
* Prefer to deploy from CI