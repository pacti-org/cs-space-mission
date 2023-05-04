# Pacti Space Mission Case Study

Note: this repository is included in the [pacti doc](https://github.com/pacti-org/pacti-docs).


## How was this project created?

- Make sure that [pdm](https://pdm.fming.dev/latest/usage/dependency/) is installed.

- Make sure that [gh](https://cli.github.com/manual/installation) is installed.

  This CLI handles authentication for github repositories, e.g.:

  ```shell
  gh repo clone pacti-org/cs-space-mission
  ```

- Setup the `pdm` repo:

  ```shell
  pdm init
  ```

  Note: Make sure the python requirement is compatible with those of [pacti](https://github.com/pacti-org/pacti). This case study requires Python 3.11 given that there are [significant performance improvements in Python 3.11 compared to earlier versions](https://stackify.com/20-simple-python-performance-tuning-tips/).

  ```toml
  requires-python = ">=3.11,<3.12"
  ```

- Add a dependency on pacti:

  ```shell
  pdm add "git+https://github.com/pacti-org/pacti.git"
  ```

- Leave the `name`, `version`, and `description` empty so that pdm will not treat this project as a package.

## Performance results

### Scenario generation

```
(cs-space-mission1-3.11) nfr@nfr-desktop:/opt/local/github.pacti-org/cs-space-mission1$ /opt/local/github.pacti-org/cs-space-mission1/.venv/bin/python /opt/local/github.pacti-org/cs-space-mission1/space_mission/hyper_scenarios.py
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 200/200 [00:17<00:00, 11.38it/s]
Generated 200 hyperparameter variations of the 5-step scenario in 17.717931509017944 seconds.
Running on AMD Ryzen Threadripper PRO 3955WX 16-Cores @ 3.8927 GHz with up to 32 threads.
Total count of Pacti operations for each 5-step scenario: 23 contracts, 12 compositions, and 10 merges.
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 200/200 [03:04<00:00,  1.08it/s]
Generated 200 hyperparameter variations of the 20-step scenario in 184.4959750175476 seconds.
Running on AMD Ryzen Threadripper PRO 3955WX 16-Cores @ 3.8927 GHz with up to 32 threads.
Total count of Pacti operations for each 5-step scenario: 115 contracts, 63 compositions, and 50 merges.
```

### Operational Requirement Verification


With 30 operational requirement variations:

```
(cs-space-mission-3.11) nfr@nfr-desktop:/opt/local/github.pacti-org/cs-space-mission$ /opt/local/github.pacti-org/cs-space-mission/.venv/bin/python /opt/local/github.pacti-org/cs-space-mission/space_mission/hyper_requirements.py100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 6000/6000 [00:28<00:00, 213.60it/s]
Found 141 admissible and 5859 non-admissible schedules out of 6000 combinations generated from 30 variations of operational requirements for each of the 200 scenarios.
Total time 28.221071243286133 seconds.
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 6000/6000 [01:12<00:00, 82.63it/s]
Found 72 admissible and 5928 non-admissible schedules out of 6000 combinations generated from 30 variations of operational requirements for each of the 200 scenarios.
Total time 72.75603914260864 seconds.
```

With 300 operational requirement variations:

```
(cs-space-mission1-3.11) nfr@nfr-desktop:/opt/local/github.pacti-org/cs-space-mission1$ /opt/local/github.pacti-org/cs-space-mission1/.venv/bin/python /opt/local/github.pacti-org/cs-space-mission1/space_mission/hyper_requirements.py
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 60000/60000 [05:00<00:00, 199.90it/s]
Found 0 admissible and 60000 non-admissible schedules out of 60000 combinations generated from 300 variations of operational requirements for each of the 200 scenarios.
Total time 300.2783877849579 seconds running on AMD Ryzen Threadripper PRO 3955WX 16-Cores @ 3.8927 GHz with up to 32 threads.

100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 60000/60000 [14:08<00:00, 70.71it/s]
Found 0 admissible and 60000 non-admissible schedules out of 60000 combinations generated from 300 variations of operational requirements for each of the 200 scenarios.
Total time 849.0543026924133 seconds running on AMD Ryzen Threadripper PRO 3955WX 16-Cores @ 3.8927 GHz with up to 32 threads.
```