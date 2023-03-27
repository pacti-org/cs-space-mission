# Space Mission Scheduling

## Performance

Current schedulability analysis performance:

```shell
nfr@nfr-desktop:/opt/local/github.formalsystems/cs-space-mission$ pdm run space_mission/hyper_requirements.py
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 60000/60000 [04:47<00:00, 208.43it/s]Found 1366 admissible and 58634 non-admissible schedules out of 60000 combinations generated from 300 variations of operational requirements for each of the 200 scenarios.
Total time 288.0133466720581 seconds with up to 32 CPUs.
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 60000/60000 [12:30<00:00, 79.92it/s]Found 709 admissible and 59291 non-admissible schedules out of 60000 combinations generated from 300 variations of operational requirements for each of the 200 scenarios.
Total time 751.3804776668549 seconds with up to 32 CPUs.
nfr@nfr-desktop:/opt/local/github.formalsystems/cs-space-mission$
```
