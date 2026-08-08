# TRACER

Tri-Action Risk Assessment and Calibration for Execution Routing of Small Language Model Responses.

Final risk-focused Master's research proposal — three-person research group, three-month implementation scope.

## Summary

TRACER learns a calibrated, action-specific risk estimator that decides whether to ACCEPT, REPAIR, or REGENERATE a Small Language Model's response, based on predicted residual failure risk rather than raw confidence. The primary experiments use code debugging and numerical reasoning tasks, since these allow responses to be labelled correct or incorrect without relying on an LLM-as-a-judge.

## Team

- Sulakna
- Lithma
- Sayuru

## Structure

- `benchmarking/` — benchmarking scripts and results
- `code/` — main implementation
- `configs/` — config files
- `results/` — experiment outputs
- `ethics/` — ethics analysis
- `literature/` — reading log and papers
- `members/` — individual workspaces
- `methodology/` — methodology docs
- `presentation/` — slides
- `progress/` — progress logs
- `report/` — final report
- `resources/` — shared resources (paper trackers etc.)

## Status

Work has not yet been divided among team members — this will be updated once roles are assigned.

## Contributing

Pull the latest changes before starting work each session:

```
git pull
```

Commit and push regularly with clear messages describing what changed.
