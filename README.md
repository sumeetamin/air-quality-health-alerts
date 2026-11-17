# Air Quality Health Alerts

A transparent aggregation tool for daily county AQI. It groups source records by state, county, and date, applies descriptive AQI bands, and writes county-level alerts locally plus a public aggregate report.

## Data and reproducibility

Uses [US EPA AirData's 2024 Daily AQI by County file](https://aqs.epa.gov/aqsweb/airdata/daily_aqi_by_county_2024.zip). EPA's download catalog documents annual county-day AQI files, with each record representing a county and day. The input CSV SHA-256 for this run is \`d2f6956102fb0557519806192f1d489fda821c5800e7d3d0f9c8324a7239f2a7\`.

\`\`\`powershell
Invoke-WebRequest -Uri 'https://aqs.epa.gov/aqsweb/airdata/daily_aqi_by_county_2024.zip' -OutFile aqi.zip
Expand-Archive aqi.zip -DestinationPath data
python -m pip install -r requirements.txt
python main.py --input data/daily_aqi_by_county_2024.csv --out outputs
\`\`\`

## 2024 aggregate run

The file contained 329,597 county-day rows across 997 counties from January 1 through December 31, 2024. The tool counted 4,003 county-days with AQI above 100, 730 above 150, and 105 above 200. Category counts are published in [\`reports/benchmark.json\`](reports/benchmark.json). Location-level output is excluded from the repository.

AQI bands follow [AirNow's AQI basics](https://smoke.airnow.gov/aqi/aqi-basics/): Good 0–50, Moderate 51–100, Unhealthy for Sensitive Groups 101–150, Unhealthy 151–200, Very Unhealthy 201–300, Hazardous 301–500. Values above 500 are reported separately as beyond the AQI scale. A value above 100 is a public-health communication threshold, not a personalized medical alert.

Coverage depends on monitoring and reporting. County summaries do not describe every neighborhood or individual exposure. This is descriptive aggregation, not a forecast, emergency alert service, or medical guidance. No raw county rows are redistributed here.
