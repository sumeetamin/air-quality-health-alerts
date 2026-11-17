"""Create transparent county-day AQI categories and aggregate summaries."""
import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd


def category(value):
    if pd.isna(value):
        return "Unknown"
    for edge, label in [
        (50, "Good"),
        (100, "Moderate"),
        (150, "Unhealthy for Sensitive Groups"),
        (200, "Unhealthy"),
        (300, "Very Unhealthy"),
        (500, "Hazardous"),
    ]:
        if value <= edge:
            return label
    return "Above AQI scale"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    parser.add_argument("--date", default="Date")
    parser.add_argument("--aqi", default="AQI")
    parser.add_argument("--state", default="State Name")
    parser.add_argument("--county", default="county Name")
    parser.add_argument("--out", default="outputs")
    args = parser.parse_args()

    source = Path(args.input)
    data = pd.read_csv(source)
    data[args.date] = pd.to_datetime(data[args.date], errors="coerce")
    data[args.aqi] = pd.to_numeric(data[args.aqi], errors="coerce")
    data = data.dropna(subset=[args.date, args.aqi])
    groups = [column for column in [args.state, args.county] if column in data]
    keys = groups + [args.date]
    daily = data.groupby(keys, dropna=False)[args.aqi].max().rename("daily_peak_aqi").reset_index()
    daily["category"] = daily["daily_peak_aqi"].map(category)
    daily["unhealthy_for_sensitive_groups_or_worse"] = daily["daily_peak_aqi"] > 100

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    # Location-level alert rows stay local. Public benchmark output is aggregate only.
    daily.to_csv(out / "daily_county_aqi.csv", index=False)
    report = {
        "dataset": "US EPA AirData Daily AQI by County 2024",
        "source_url": "https://aqs.epa.gov/aqsweb/airdata/daily_aqi_by_county_2024.zip",
        "input_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "source_rows": int(len(data)),
        "county_day_records": int(len(daily)),
        "counties": int(daily[groups].drop_duplicates().shape[0]) if groups else None,
        "date_range": [daily[args.date].min().date().isoformat(), daily[args.date].max().date().isoformat()],
        "category_counts": {str(k): int(v) for k, v in daily["category"].value_counts().sort_index().items()},
        "county_days_aqi_over_100": int((daily["daily_peak_aqi"] > 100).sum()),
        "county_days_aqi_over_150": int((daily["daily_peak_aqi"] > 150).sum()),
        "county_days_aqi_over_200": int((daily["daily_peak_aqi"] > 200).sum()),
        "rule": "Use the maximum AQI reported for each county and date; categories are descriptive AQI bands. A county-day above 100 is flagged for public-health context, not as a personalized medical alert.",
        "method": "Group by state, county, and date; retain the maximum supplied county-day AQI; apply explicit AQI category boundaries.",
        "limitations": "Coverage depends on monitoring and reporting. County-level values do not describe every neighborhood or individual exposure. This is descriptive aggregation, not a forecast or emergency alert service.",
    }
    (out / "benchmark.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
