# Space Mission Case Study

There are two case studies:

- A simplified specification of the [Mars 2020 Entry-Descent Landing (EDL) scenario](./mars_entry_descent_landing/README.md)

- A simplified spacecraft-small body approach scenario (see below).

  This case study is based on the following paper:

  I. A. Nesnas, B. J. Hockman, S. Bandopadhyay, B. J. Morrell, D. P.
  Lubey, J. Villa, D. S. Bayard, A. Osmundson, B. Jarvis, M. Bersani,
  et al., “Autonomous exploration of small bodies toward greater autonomy
  for deep space missions,” Frontiers in Robotics and AI, p. 270, 2021.

## Specifications for the system-level tasks for the spacecraft-small body approach scenario

The specifications were developed in two phases.

### Phase 1: Exploration with notebooks

These notebooks focus on explaining the system task specifications and on analyzing their characteristics.

- Tasks from the power viewpoint perspective:

  See [./space_mission/space_mission_power.ipynb](./space_mission/space_mission_power.ipynb)

- Tasks from the science viewpoint perspective:

  See [./space_mission/space_mission_science.ipynb](./space_mission/space_mission_science.ipynb)

- Tasks from the navigation perspective:

  See [./space_mission/space_mission_navigation.ipynb](./space_mission/space_mission_navigation.ipynb)

- Tasks from the thermal perspective:

  See [./space_mission/space_mission_thermal.ipynb](./space_mission/space_mission_thermal.ipynb)

- Fusing viewpoints (power, science, navigation):

  See [./space_mission/space_mission_3viewpoints.ipynb](./space_mission/space_mission_3viewpoints.ipynb)

### Phase 2: Design and operational requirement exploration

Instead of specifying and analyzing a point design, the idea is to vary
the design and operational parameters.

#### Parametric design generation

The following Python functions use the Pacti contract algebra for  
generating task scenario designs from variable hyperparameters.

See [./space_mission/generators.py](./space_mission/generators.py)

The following notebooks demonstrate design generation with an interactive chart of CPU utilization
to assess the efficiency of parallelizing the algebraic operations involved.

There are two variants of these notebooks according to the length of the task scenarios generated (5 vs. 20 tasks).

See [./space_mission/analysis_results1-5steps.ipynb](./space_mission/analysis_results1-5steps.ipynb)

See [./space_mission/analysis_results1-20steps.ipynb](./space_mission/analysis_results1-20steps.ipynb)

Alternatively, one can parallelize design generation using a Python script:

See [./space_mission/hyper_scenarios.py](./space_mission/hyper_scenarios.py)

#### Parametric schedulability analysis

The following Python functions use the Pacti contract algebra for
analyzing a task scenario against operational requirements with variable hyperparameters.

See [./space_mission/schedulability.py](./space_mission/schedulability.py)

The following notebooks demonstrate the schedulability analysis of a task scenario design against
operational requirements with variable hyperparameters with an interactive chart of CPU utilization
to assess the efficiency of parallelizing the algebraic operations involved.

There are two variants of these notebooks according to the length of the task scenarios analyzed (5 vs. 20 tasks).

See [./space_mission/schedulability_analysis_5steps.ipynb](./space_mission/schedulability_analysis_5steps.ipynb)

See [./space_mission/schedulability_analysis_20steps.ipynb](./space_mission/schedulability_analysis_20steps.ipynb)

Alternatively, one can parallelize schedulability analysis using a Python script:

See [./space_mission/hyper_requirements.py](./space_mission/hyper_requirements.py)

#### Analyzing bounds on admissible solutions

Some of the 5-step task solutions:

See [./space_mission/analysis_results1-5steps.ipynb](./space_mission/analysis_results1-5steps.ipynb)

Some of the 20-step task solutions:

See [./space_mission/analysis_results1-20steps.ipynb](./space_mission/analysis_results1-20steps.ipynb)

Scatter plots of the 20-step task solutions:

See [./space_mission/analysis_results2.ipynb](./space_mission/analysis_results2.ipynb)

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
