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

## Running the notebooks

### Individual viewpoint modeling

- [./space_mission/space_mission_power.ipynb](./space_mission/space_mission_power.ipynb)
- [./space_mission/space_mission_navigation.ipynb](./space_mission/space_mission_navigation.ipynb)
- [./space_mission/space_mission_science.ipynb](./space_mission/space_mission_science.ipynb)
- [./space_mission/space_mission_thermal.ipynb](./space_mission/space_mission_thermal.ipynb)

### Combining Power, Navigation, and Science

- [./space_mission/space_mission_3viewpoints.ipynb](./space_mission/space_mission_3viewpoints.ipynb)

## Performance results

### Scenario generation

```
(cs-space-mission1-3.11) nfr@nfr-desktop:/opt/local/github.pacti-org/cs-space-mission1$ /opt/local/github.pacti-org/cs-space-mission1/.venv/bin/python /opt/local/github.pacti-org/cs-space-mission1/space_mission/hyper_scenarios.py
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 200/200 [00:15<00:00, 12.82it/s]
<class 'list'>
<class 'pacti.terms.polyhedra.polyhedral_contract.PolyhedralContract'>
Generated 200 hyperparameter variations of the 5-step scenario in 15.751834154129028 seconds.
Running on AMD Ryzen Threadripper PRO 3955WX 16-Cores @ 3.8927 GHz with up to 32 threads.
Pacti compose,quotient,merge statistics:
compose invocation counts: (min: 0, max: 12, avg: 10.08, total: 2016)
min/max compose contract size: (constraints: 6, variables: 3)/(constraints: 22, variables: 12)
no quotient operations
merge invocation counts: (min: 0, max: 10, avg: 8.4, total: 1680)
min/max merge contract size: (constraints: 3, variables: 2)/(constraints: 45, variables: 23)
Pacti PolyhedralTermList statistics:
no contains_behavior operations
Pacti PolyhedralCompoundContract statistics:
no compound_merge operations

100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 200/200 [02:52<00:00,  1.16it/s]
Generated 200 hyperparameter variations of the 20-step scenario in 172.59228324890137 seconds.
Running on AMD Ryzen Threadripper PRO 3955WX 16-Cores @ 3.8927 GHz with up to 32 threads.
Pacti compose,quotient,merge statistics:
compose invocation counts: (min: 51, max: 51, avg: 51.0, total: 10200)
min/max compose contract size: (constraints: 6, variables: 3)/(constraints: 185, variables: 95)
no quotient operations
merge invocation counts: (min: 40, max: 40, avg: 40.0, total: 8000)
min/max merge contract size: (constraints: 3, variables: 2)/(constraints: 45, variables: 23)
Pacti PolyhedralTermList statistics:
no contains_behavior operations
Pacti PolyhedralCompoundContract statistics:
no compound_merge operations
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