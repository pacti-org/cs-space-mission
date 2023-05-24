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

```text
(cs-space-mission1-3.11) nfr@nfr-desktop:/opt/local/github.pacti-org/cs-space-mission1$ /opt/local/github.pacti-org/cs-space-mission1/.venv/bin/python /opt/local/github.pacti-org/cs-space-mission1/space_mission/hyper_scenarios.py
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 100/100 [00:09<00:00, 10.84it/s]
Generated 100 hyperparameter variations of the 5-step scenario in 9.372139930725098 seconds.
Running on AMD Ryzen Threadripper PRO 3955WX 16-Cores @ 3.8927 GHz with up to 32 threads.
Pacti compose,quotient,merge statistics:
compose invocation counts: (min: 0, max: 12, avg: 8.16, total: 816)
min/max compose contract size: (constraints: 6, variables: 3)/(constraints: 22, variables: 12)
no quotient operations
merge invocation counts: (min: 0, max: 10, avg: 6.8, total: 680)
min/max merge contract size: (constraints: 3, variables: 2)/(constraints: 44, variables: 23)
Pacti PolyhedralTermList statistics:
no contains_behavior operations
Pacti PolyhedralCompoundContract statistics:
no compound_merge operations

100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 100/100 [01:37<00:00,  1.02it/s]
Generated 100 hyperparameter variations of the 20-step scenario in 97.78417682647705 seconds.
Running on AMD Ryzen Threadripper PRO 3955WX 16-Cores @ 3.8927 GHz with up to 32 threads.
Pacti compose,quotient,merge statistics:
compose invocation counts: (min: 51, max: 51, avg: 51.0, total: 5100)
min/max compose contract size: (constraints: 6, variables: 3)/(constraints: 187, variables: 95)
no quotient operations
merge invocation counts: (min: 40, max: 40, avg: 40.0, total: 4000)
min/max merge contract size: (constraints: 3, variables: 2)/(constraints: 44, variables: 23)
Pacti PolyhedralTermList statistics:
no contains_behavior operations
Pacti PolyhedralCompoundContract statistics:
no compound_merge operations
```

### Operational Requirement Verification

```text
(cs-space-mission1-3.11) nfr@nfr-desktop:/opt/local/github.pacti-org/cs-space-mission1$ /opt/local/github.pacti-org/cs-space-mission1/.venv/bin/python /opt/local/github.pacti-org/cs-space-mission1/space_mission/hyper_requirements.py
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2000/2000 [00:22<00:00, 87.49it/s]
Found 70 admissible and 9930 non-admissible schedules out of 10000 combinations generated from 100 variations of operational requirements for each of the 100 scenarios.
Total time 23.014519691467285 seconds running on AMD Ryzen Threadripper PRO 3955WX 16-Cores @ 3.8927 GHz with up to 32 threads.
Pacti compose,quotient,merge statistics:
no compose operations
no quotient operations
merge invocation counts: (min: 9, max: 11, avg: 9.0543, total: 90543)
min/max merge contract size: (constraints: 1, variables: 1)/(constraints: 80, variables: 35)
Pacti PolyhedralTermList statistics:
no contains_behavior operations
Pacti PolyhedralCompoundContract statistics:
no compound_merge operations

100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2000/2000 [01:11<00:00, 27.83it/s]
Found 56 admissible and 9944 non-admissible schedules out of 10000 combinations generated from 100 variations of operational requirements for each of the 100 scenarios.
Total time 72.22614121437073 seconds running on AMD Ryzen Threadripper PRO 3955WX 16-Cores @ 3.8927 GHz with up to 32 threads.
Pacti compose,quotient,merge statistics:
no compose operations
no quotient operations
merge invocation counts: (min: 9, max: 11, avg: 9.0548, total: 90548)
min/max merge contract size: (constraints: 1, variables: 1)/(constraints: 255, variables: 125)
Pacti PolyhedralTermList statistics:
no contains_behavior operations
Pacti PolyhedralCompoundContract statistics:
no compound_merge operations
```
