# Pacti Space Mission Case Study

Note: this repository is included in the [pacti doc](https://github.com/FormalSystems/pacti-docs).


## How was this project created?

- Make sure that [pdm](https://pdm.fming.dev/latest/usage/dependency/) is installed.

- Make sure that [gh](https://cli.github.com/manual/installation) is installed.

  This CLI handles authentication for github repositories, e.g.:

  ```shell
  gh repo clone FormalSystems/cs-space-mission
  ```

- Setup the `pdm` repo:

  ```shell
  pdm init
  ```

  Note: Make sure the python requirement is compatible with those of [pacti](https://github.com/formalsystems/pacti).

  ```toml
  requires-python = ">=3.8, <=3.11.1"
  ```

- Add a dependency on pacti:

  ```shell
  pdm add "git+https://github.com/formalsystems/pacti.git"
  ```

- Leave the `name`, `version`, and `description` empty so that pdm will not treat this project as a package.
