import requests
import pandas as pd
import xml.etree.ElementTree as ET
from zipfile import ZipFile
import os

def divvy_stations(url="https://gbfs.lyft.com/gbfs/2.3/chi/en/station_information.json"):
    response = requests.get(url)
    data = response.json()
    stations = data['data']['stations']
    return pd.DataFrame(stations)[['name', 'lat', 'lon']]

def cta_bus_stops(extract_path):

    kml_files = [os.path.join(extract_path, f) for f in os.listdir(extract_path) if f.endswith('.kml')]

    root = ET.parse(kml_files[0]).getroot()
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}

    bus_stops = []
    for p in root.findall('.//kml:Placemark', ns):
        name = p.find('kml:name', ns).text
        lon, lat, *_ = map(float, p.find('.//kml:coordinates', ns).text.strip().split(','))
        bus_stops.append((name, lat, lon))

    return pd.DataFrame(bus_stops, columns=['name', 'lat', 'lon'])

def get_all_stops():
    """Main function to create a combined DataFrame of Divvy and CTA stops."""
    base_dir = os.getcwd() 
    kmz_path = os.path.join(base_dir, 'CTA_BusStops.kmz')
    extract_path = os.path.join(base_dir, 'tmp')

    divvy_df = divvy_stations()
    divvy_df['type'] = 'bike'

    cta_df = cta_bus_stops(extract_path)
    cta_df['type'] = 'bus'

    combined_df = pd.concat([divvy_df, cta_df], ignore_index=True)
    combined_df = combined_df[['name', 'lat', 'lon', 'type']]

    return combined_df

if __name__ == "__main__":
    df = get_all_stops()
    df.to_csv("all_stops.csv", index=False)
    print("✅ all_stops.csv created successfully!")
