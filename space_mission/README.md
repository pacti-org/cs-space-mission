# Space Mission Scheduling

## Performance

Current scenario generation performance:

```shell
(cs-space-mission-3.11) nfr@nfr-desktop:/opt/local/github.formalsystems/cs-space-mission$ /opt/local/github.formalsystems/cs-space-mission/.venv/bin/python /opt/local/github.formalsystems/cs-space-mission/space_mission/hyper_scenarios.py
Generating 200 hyperparameter variations of the 5-step scenario
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 200/200 [00:14<00:00, 13.71it/s]
All 200 hyperparameter variations of the 5-step scenario sequence generated
Total time 14.762425899505615 seconds with up to 32 CPUs.
Total count of Pacti operations for each 5-step scenario: 23 contracts, 12 compositions, and 10 merges
Generating 200 hyperparameter variations of the 5-step scenario
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 200/200 [02:58<00:00,  1.12it/s]
All 200 hyperparameter variations of the 20-step scenario sequence generated.
Total time 178.57544589042664 seconds with up to 32 CPUs.
Total count of Pacti operations for each 20-step scenario: 115 contracts, 63 compositions, and 50 merges
```

Current schedulability analysis performance:

```shell
(cs-space-mission-3.11) nfr@nfr-desktop:/opt/local/github.formalsystems/cs-space-mission$ /opt/local/github.formalsystems/cs-space-mission/.venv/bin/python /opt/local/github.formalsystems/cs-space-mission/space_mission/hyper_requirements.py
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 60000/60000 [04:54<00:00, 203.48it/s]
Found 1376 admissible and 58624 non-admissible schedules out of 60000 combinations generated from 300 variations of operational requirements for each of the 200 scenarios.
Total time 295.0339021682739 seconds with up to 32 CPUs.
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 60000/60000 [13:13<00:00, 75.61it/s]
Found 891 admissible and 59109 non-admissible schedules out of 60000 combinations generated from 300 variations of operational requirements for each of the 200 scenarios.
Total time 794.0496697425842 seconds with up to 32 CPUs.
(cs-space-mission-3.11) nfr@nfr-desktop:/opt/local/github.formalsystems/cs-space-mission$ 
```
