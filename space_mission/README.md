To insert *local* figures (PNG or JPG), follow the conversion to Base64 technique described here: 
https://mljar.com/blog/jupyter-notebook-insert-image/

Note: Inserting *.SVG as Base64 figures will render locally with `make docs-serve` only.
Github's ipynb rendering will show only an icon, not the SVG image.

For SVG to PDF conversion, use this free service:
https://cloudconvert.com/svg-to-pdf

5,20 step analysis runs with up to 3 failures:

```shell
(pacti-3.9) nfr@nfr-desktop:/opt/local/github.formalsystems/pacti$ /opt/local/github.formalsystems/pacti/.venv/bin/python /opt/local/github.formalsystems/pacti/case_studies/space_mission/hyper_requirements.py
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 6000/6000 [00:52<00:00, 114.81it/s]
Found 162 admissible and 17514 non-admissible schedules out of 6000 combinations generated from 30 variations of operational requirements for each of the 200 scenarios.
Total time 52.663562059402466 seconds.
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 6000/6000 [02:55<00:00, 34.18it/s]
Found 106 admissible and 17682 non-admissible schedules out of 6000 combinations generated from 30 variations of operational requirements for each of the 200 scenarios.
Total time 176.06474328041077 seconds.
```

5,20 step analysis runs with up to 1 failure:

```shell
(pacti-3.9) nfr@nfr-desktop:/opt/local/github.formalsystems/pacti$ /opt/local/github.formalsystems/pacti/.venv/bin/python /opt/local/github.formalsystems/pacti/case_studies/space_mission/hyper_requirements.py
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 6000/6000 [00:42<00:00, 140.31it/s]
Found 128 admissible and 5872 non-admissible schedules out of 6000 combinations generated from 30 variations of operational requirements for each of the 200 scenarios.
Total time 42.92044806480408 seconds.
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 6000/6000 [01:58<00:00, 50.80it/s]
Found 73 admissible and 5927 non-admissible schedules out of 6000 combinations generated from 30 variations of operational requirements for each of the 200 scenarios.
Total time 118.37994575500488 seconds.
```

Since the result files can exceed the 100Mb limit of github's lfs, they are excluded from git.

