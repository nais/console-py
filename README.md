# console

NAIS management console

This repo contains an effort to prototype and explore creation of a console based around REST APIs and GraphQL.
It was developed in parallel with a similar prototype in [Go](https://github.com/nais/console).

We have written a short summary of [lessons learned](https://github.com/navikt/pig/blob/master/kubeops/adr/010-console-nais-io.md#lessons-learned-from-prototyping-phase).

Development continues in [console](https://github.com/nais/console), this repo will be archived.


## Development

We use [`earthly`](https://earthly.dev) for building.
If you don't have earthly installed, you can use the wrapper [`earthlyw`](https://github.com/mortenlj/earthlyw) in the root of the repository.

Build docker image: `./earthlyw +docker`
Run prospector and pytest: `./earthlyw +test`
