"""Create transparent daily AQI alerts from public station observations."""
import argparse,json
from pathlib import Path
import pandas as pd
def category(x):
 if pd.isna(x):return "Unknown"
 for edge,label in [(50,"Good"),(100,"Moderate"),(150,"Unhealthy for sensitive groups"),(200,"Unhealthy"),(300,"Very unhealthy"),(500,"Hazardous")]:
  if x<=edge:return label
 return "Invalid"
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("--input",required=True);p.add_argument("--date",default="Date");p.add_argument("--aqi",default="AQI");p.add_argument("--station",default="SiteName");p.add_argument("--out",default="outputs");a=p.parse_args()
 d=pd.read_csv(a.input);d[a.date]=pd.to_datetime(d[a.date],errors="coerce");d[a.aqi]=pd.to_numeric(d[a.aqi],errors="coerce");d=d.dropna(subset=[a.date,a.aqi])
 keys=[c for c in [a.station] if c in d]
 daily=d.groupby(keys+[a.date],dropna=False)[a.aqi].max().rename("daily_peak_aqi").reset_index()
 daily["category"]=daily.daily_peak_aqi.map(category);daily["alert"]=daily.daily_peak_aqi>=101
 if keys:daily["consecutive_alert_days"]=daily.groupby(keys).alert.transform(lambda x:x.astype(int).rolling(3,min_periods=1).sum())
 out=Path(a.out);out.mkdir(parents=True,exist_ok=True);daily.to_csv(out/"daily_station_alerts.csv",index=False)
 summary={"records":len(daily),"days_over_100":int((daily.daily_peak_aqi>100).sum()),"source_rows":len(d),"grouping":keys or "all observations"}
 (out/"summary.json").write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
if __name__=="__main__":main()
