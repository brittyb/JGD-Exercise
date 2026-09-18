import requests
import json
from config import COUNTY_NAME, STATE_CODE, COUNTY_CODE, USGS_STATIONS_URL, USGS_READINGS_URL, IMAP_URL, USGS_API_KEY
BATCH_SIZE = 100

OUTPUT_FILE_STATIONS = "web/usgs_stations.geojson"
OUTPUT_FILE_GEO_CONTEXT = "web/geographical_context.geojson"
# Get the county boundaries from the IMAP service and save them to a GeoJSON file
def fetch_county_boundaries():
    params = {
        "where": "COUNTY='KENT'",
        "outFields": "*",
        "outSR": "4326",
        "f": "geojson"
        }

    response = requests.get(IMAP_URL, params=params)
    response.raise_for_status()
    data = response.json()

    if not data["features"]:
        print(f"No features found for county: {COUNTY_NAME}")
        return

    with open(OUTPUT_FILE_GEO_CONTEXT, "w") as file:
        json.dump(data, file)

    print(f"Saved {COUNTY_NAME} County boundary.")
    
def get_stations():

    # Build a request to the USGS API to get monitoring locations in a specified state and County
    params = {
        "f": "json",
        "state_code": STATE_CODE,
        "county_code": COUNTY_CODE,
        "limit": 10000,
        "api_key": USGS_API_KEY
    }

    response = requests.get(USGS_STATIONS_URL, params=params)

    print("Status:", response.status_code)
    print("Rate limit:", response.headers.get("X-RateLimit-Limit"))
    print("Remaining:", response.headers.get("X-RateLimit-Remaining"))

    response.raise_for_status()

    data = response.json()

    print("Number of stations returned:", len(data["features"]))

    station_features = []
    for station in data["features"]:
        properties = station["properties"]
        station_features.append({
                    "type": "Feature",
                    "properties": {
                        "id": properties.get("id"),
                        "name": properties.get("monitoring_location_name"),
                        "site_type": properties.get("site_type"),
                    },
                    "geometry": station["geometry"]
                })
    
    
    return station_features

def get_location_ids(data):
    """Get unique monitoring location IDs from the station features."""

    location_ids = []

    for feature in data:
        station_id = feature["properties"].get("id")

        if station_id and station_id not in location_ids:
            location_ids.append(station_id)

    return location_ids



def get_readings_for_batch(location_ids):
    """Get latest continuous observations for a batch of locations."""


    query = {
        "op": "in", # operation: in (check to see if monitoring_location_id is in the list of location_ids)
        "args": [
            {
                "property": "monitoring_location_id"
            },
            location_ids
        ]
    }

    headers = {
        "Content-Type": "application/query-cql-json" # Tells the server we are sending a query
    }

    params = {
        "f": "json",
        "limit": 50000,
        "api_key": USGS_API_KEY
    }

    response = requests.post(
        USGS_READINGS_URL,
        params=params,
        headers=headers,
        json=query
    )

    print("Status:", response.status_code)
    print("Remaining requests:",
          response.headers.get("X-RateLimit-Remaining"))

    response.raise_for_status()

    return response.json()

"""Organize the readings by putting each reading with its associated station ID"""
def organize_readings(data):
    readings_by_station = {}

    for feature in data.get("features", []):

        properties = feature["properties"]

        station_id = properties.get("monitoring_location_id")

        if not station_id:
            continue

        reading = {
            "parameter_code": properties.get("parameter_code"),
            "value": properties.get("value"),
            "unit": properties.get("unit_of_measure"),
            "time": properties.get("time"),
            "approval_status": properties.get("approval_status"),
            "qualifier": properties.get("qualifier")
        }

        if station_id not in readings_by_station: # station not already recorded
            readings_by_station[station_id] = []

        readings_by_station[station_id].append(reading)

    return readings_by_station









def main():
    fetch_county_boundaries()

    # --------------------------------------------------
    # Get all monitoring stations in specified state and county
    # --------------------------------------------------
    data = get_stations()

    # --------------------------------------------------
    # Get a list of all station IDs
    # --------------------------------------------------

    location_ids = get_location_ids(data)

    print("Total monitoring locations:", len(location_ids))


    # --------------------------------------------------
    # Retrieve readings for all station IDs in batches
    # --------------------------------------------------

    all_readings = {}
    """Get all of the readings for the monitoring locations in batches to avoid exceeding the API's request limits."""
    for start in range(0, len(location_ids), BATCH_SIZE):

        batch = location_ids[start:start + BATCH_SIZE]

        print(
            f"\nRequesting locations "
            f"{start + 1}-{start + len(batch)} "
            f"of {len(location_ids)}"
        )

        response_data = get_readings_for_batch(batch)

        batch_readings = organize_readings(response_data)

        # Add this batch to our master dictionary
        for station_id, readings in batch_readings.items():

            if station_id not in all_readings:
                all_readings[station_id] = []

            all_readings[station_id].extend(readings)


    # --------------------------------------------------
    # Match readings back to their stations
    # --------------------------------------------------

    stations_with_data = 0
    stations_without_data = 0

    for feature in data:

        properties = feature["properties"]

        station_id = properties.get("id")

        readings = all_readings.get(station_id, [])

        properties["latest_readings"] = readings

        if readings:
            stations_with_data += 1
        else:
            stations_without_data += 1


    # --------------------------------------------------
    # Save to output file
    # --------------------------------------------------

    output_data = {
        "type": "FeatureCollection",
        "features": data
    }

    with open(OUTPUT_FILE_STATIONS, "w") as file:
        json.dump(output_data, file, indent=2)

    print("\n--- RESULTS ---")
    print("Monitoring locations:", len(location_ids))
    print("Stations with readings:", stations_with_data)
    print("Stations without readings:", stations_without_data)
    print("Total observations:", sum(
        len(readings)
        for readings in all_readings.values()
    ))

    print("\nSaved:", OUTPUT_FILE_STATIONS)

if __name__ == "__main__":
    main()