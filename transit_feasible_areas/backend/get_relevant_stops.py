import pandas as pd 
import os
import numpy as np
import geopandas as pgd


df_stops = pd.read_csv(os.path.join(os.path.dirname(__file__), 'all_stops.csv'))


def haversine(lat1, lon1, lat2, lon2):
    """Calculate distance between two (lat, lon) points in miles."""
    R = 3958.8  # Earth radius in miles

    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    delta_phi = np.radians(lat2 - lat1)
    delta_lambda = np.radians(lon2 - lon1)

    a = np.sin(delta_phi/2.0)*2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda/2.0)*2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

    return R * c

def relevant_stops(center_lat, center_lon, radius_miles=3, save_geojson_path=None):
    lat1 = np.radians(center_lat)
    lon1 = np.radians(center_lon)
    lat2 = np.radians(df_stops['lat'])
    lon2 = np.radians(df_stops['lon'])

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = np.sin(delta_lat/2)*2 + np.cos(lat1) * np.cos(lat2) * np.sin(delta_lon/2)*2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    distances = 3958.8 * c

    nearby = df_stops[distances <= radius_miles].copy()
    nearby = nearby[['name', 'lat', 'lon', 'type']]
    nearby = nearby.drop_duplicates(subset='name').reset_index(drop=True)  # Keep first occurrence if name repeats

    # If user asked to save as GeoJSON
    if save_geojson_path:
        # Convert to GeoDataFrame and save
        import geopandas as gpd
        gdf = gpd.GeoDataFrame(
            nearby,
            geometry=gpd.points_from_xy(nearby.lon, nearby.lat),
            crs="EPSG:4326"
        )
        gdf.to_file(save_geojson_path, driver='GeoJSON')
        print(f"✅ Saved to {save_geojson_path}")

    return nearby