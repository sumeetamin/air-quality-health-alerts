# Air Quality Health Alerts

Convert public station AQI records into transparent daily categories, exceedance flags, and persistence summaries.

> **Portfolio prototype.** Source code is provided; no benchmark results are claimed until you run it on the cited data and record the output.

## Use case

Convert public station AQI records into transparent daily categories, exceedance flags, and persistence summaries. The CLI consumes local files, emits reproducible reports, and keeps data out of the repository.

## Data and provenance

[U.S. EPA Outdoor Air Quality Data](https://www.epa.gov/outdoor-air-quality-data). An EPA AQS/AirData daily file containing date, AQI, and an optional station/site name. Source files are not bundled. Respect source terms and cite the dataset when publishing results.

## Quick start

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
# Download/prepare the source data locally, then run:
python main.py --input data/aqi_daily.csv --date Date --aqi AQI --station SiteName --out outputs
```

## Outputs

Generated results are saved under `outputs/`; file names and metrics are printed or documented by the CLI. The repository excludes downloaded data and artifacts.

## Evaluation and operating notes

The AQI categories are descriptive and the alert threshold is a project setting. Follow local public-health guidance; this script is not a medical or emergency alert service.

For production use, add a frozen reference period, out-of-time evaluation, monitoring ownership, and a documented rollback or escalation path. This project is a local baseline, not a deployed service.

## License

No code license file is included yet. Third-party data remains subject to its source terms.
