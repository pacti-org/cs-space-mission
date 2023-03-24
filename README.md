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

  Note: Make sure the python requirement is compatible with those of [pacti](https://github.com/formalsystems/pacti). This case study requires Python 3.11 given that there are [significant performance improvements in Python 3.11 compared to earlier versions](https://stackify.com/20-simple-python-performance-tuning-tips/).

  ```toml
  requires-python = ">=3.11,<3.12"
  ```

- Add a dependency on pacti:

  ```shell
  pdm add "git+https://github.com/formalsystems/pacti.git"
  ```

- Leave the `name`, `version`, and `description` empty so that pdm will not treat this project as a package.

## Performance results

```
(cs-space-mission-3.9) nfr@nfr-desktop:/opt/local/github.formalsystems/cs-space-mission$ /opt/local/github.formalsystems/cs-space-mission/.venv/bin/python /opt/local/github.formalsystems/cs-space-mission/space_mission/hyper_requirements.py
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 6000/6000 [00:29<00:00, 201.72it/s]
Found 93 admissible and 5907 non-admissible schedules out of 6000 combinations generated from 30 variations of operational requirements for each of the 200 scenarios.
Total time 29.885207891464233 seconds.
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 6000/6000 [01:21<00:00, 73.88it/s]
Found 62 admissible and 5938 non-admissible schedules out of 6000 combinations generated from 30 variations of operational requirements for each of the 200 scenarios.
Total time 81.38886523246765 seconds.
```
