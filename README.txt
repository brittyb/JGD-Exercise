
# Kent County Water Monitoring Map

## Overview

This project creates a simple web map showing water monitoring locations in and around **Kent County, Maryland**, along with the most recent available monitoring readings.

The map is designed for a community watershed group whose board members may not have a technical or GIS background. The goal is to make it easy to see:

* Where monitoring stations are located
* Which stations currently have available readings
* What the most recent readings are
* Where Kent County is located

The project uses publicly available data from the **U.S. Geological Survey (USGS)** and the **Maryland Department of Information Technology / Maryland iMAP**.

The project is hosted using Vercel to make viewing content as accessible as possible.

---

## Project Contents

After extracting the ZIP file, the project should contain:

```text
Washington College Technical Interview/
│
├── DataRetrieval.py
├── config.py
├── requirements.txt
├── README.md
│
└── web/
    └── index.html
    └── kent_county.geojson
    └── usgs_stations.geojson
```

### Important files

**`web/index.html`**
The interactive map.

**`DataRetrieval.py`**
Downloads the latest data and creates the GeoJSON files used by the map.

**`config.py`**
Contains the USGS API key used by the data retrieval script.

**`kent_county.geojson`**
The Kent County geographic boundary.

**`usgs_stations.geojson`**
The monitoring stations and their latest available readings.

**`requirements.txt`**
Lists the Python package needed to run the data retrieval script.

---

# Requirements

To refresh the data, you will need:

* A Windows or Mac computer
* Python 3.14.3 or newer
* An internet connection
* A USGS API key
* The complete project folder


You do **not** need Python to simply view the existing map. Python is only needed when refreshing the data.

---

# Viewing the Map

No extra steps are required to view the map. Visit the URL:

---

# Refreshing the Data

The data should be refreshed before each quarterly board meeting so that the map reflects the latest available monitoring information.

Most of the process is automated. You do **not** need to edit `DataRetrieval.py`.

The only file you need to change is `config.py`, where you enter the new USGS API key.

## Step 1: code project folder

Extract the ZIP file if you have not already done so.

code project folder containing:

```text
DataRetrieval.py
config.py
requirements.txt
```

## Step 2: Open a terminal

### Windows

code project folder in File Explorer.

Click the address bar, type:

```text
cmd
```

and press **Enter**.

### Mac

Open Terminal.

Type:

```bash
cd 
```

Then drag the project folder into Terminal and press **Enter**.

---

## Step 3: Install the required Python package

Run:

### Windows

```bash
pip install -r requirements.txt
```

### Mac

```bash
pip3 install -r requirements.txt
```

The project uses the Python `requests` package to communicate with the public data APIs.

The `json` package does not need to be installed because it is included with Python.

---

# Step 4: Get a USGS API Key

The monitoring-location and reading data come from the USGS Water Data API.

You will need a valid USGS API key to refresh the data.

Keep the API key private. Do not post it publicly or commit it to a public Git repository.

If the API requires you to request a new key, follow the current instructions provided by USGS.


---

# Step 5: Add the API Key

Open:

```text
config.py
```

You should see a placeholder similar to:

```python
USGS_API_KEY = "YOUR_API_KEY"
```

Replace `YOUR_API_KEY` with the API key you received from USGS.

For example:

```python
USGS_API_KEY = "your-key-goes-here"
```

Save the file.

**Do not change the other files unless you know that the data sources or project requirements have changed.**

---

# Step 6: Run the Data Retrieval Script

From the project folder, run:

### Windows

```bash
python DataRetrieval.py
```

### Mac

```bash
python3 DataRetrieval.py
```

The script will:

1. Download the Kent County boundary.
2. Download monitoring locations in Kent County.
3. Collect the monitoring location IDs.
4. Request the latest available continuous observations in batches.
5. Match observations to their monitoring stations.
6. Keep stations that do not currently have readings.
7. Save the monitoring data to `usgs_stations.geojson`.

The script prints information about the number of monitoring locations, readings, and stations without current readings.

---

# Step 7: Review the Updated Map

After the script finishes, go on GitHub and replace the kent_county.geojson and usgs_stations.geojson files with the newly generated GeoJSON files. After publishing these changes they will be available on the website immediately. Do not publish these changes until you have confirmed that you want them to be public.

Check several locations on the map.

In particular, verify that:

* The Kent County boundary appears correctly.
* Monitoring stations appear on the map.
* Stations with available readings can be identified.
* Clicking a station displays its available information.
* Stations without current readings are still represented.
* The displayed reading includes its value, unit, and time.
* The map does not contain obvious misplaced points.

---

# Understanding the Monitoring Data

The project keeps **all monitoring stations returned by the USGS API**, including stations that do not currently have a reading.

This is intentional.

A station without a current reading still provides useful information because it shows where monitoring exists. The map can therefore distinguish between:

* A location where monitoring exists and current data is available
* A location where monitoring exists but no current reading is available

The project stores the latest available observations returned by the USGS `latest-continuous` dataset.

Each observation may include:

* Parameter code
* Value
* Unit of measurement
* Observation time
* Approval status
* Qualifier

Different stations may measure different things. For example, a station may report streamflow or gage height, so the map does not assume that every reading represents the same measurement.

---

# Data Sources

## USGS Water Data

The monitoring locations and current observations come from the U.S. Geological Survey Water Data API.

The project uses:

* Monitoring locations
* Latest continuous observations


## Maryland iMAP

The Kent County boundary comes from Maryland's iMAP geographic data services.

The boundary is downloaded as GeoJSON and stored locally in:

```text
kent_county.geojson
```

## Basemap

The web map uses OpenStreetMap tiles through Leaflet.

The basemap is used only as geographic context; the monitoring data itself comes from the sources described above.

---

# Why These Data Sources Were Chosen

USGS was selected for the monitoring data because it data through an API. This makes it possible to automate the quarterly refresh instead of manually downloading and processing data.

Maryland iMAP was selected for the county boundary because it provides Maryland geographic boundary data directly from a state government source and can return the data in GeoJSON format.

Other publicly available water-quality resources, MDOT SHA County Boundaries and Eyes on the Bay, were considered as potential sources. The USGS API was used because it provided the monitoring-location that could be retrieved programmatically. Maryland iMap was chosen because of its more precise boundaries.

---

# Data Download Date

The included GeoJSON files represent the data retrieved when this project was last refreshed.

When the project is refreshed for a future meeting, the new download date should be recorded here or in the project's data notes.

For a production version of this project, each refresh should record:

* Date the data was downloaded
* Data source
* API or service used
* Number of monitoring locations retrieved
* Number of locations with current readings
* Number of locations without current readings
* Any notable data issues

---

# Data Quality Checks

Before using the map for a board meeting, review the updated data for obvious problems.

The following should be checked:

### Number of stations

Confirm that the number of returned monitoring locations is reasonable compared with the previous refresh.

A large unexpected change may indicate a source or API problem.

### Coordinates

Monitoring locations should appear in the expected geographic area.

The GeoJSON data uses longitude and latitude coordinates in WGS 84 / EPSG:4326.

### Missing values

Some stations may not have current readings. These stations are not automatically removed because their location is still useful.

### Duplicate stations

Monitoring location IDs should normally uniquely identify stations. Unexpected duplicates should be investigated before publishing an updated map.

### Units

Do not assume that every station measures the same quantity.

The map should display the unit provided by the source.

### Old or missing observations

A station may exist but have no current observation available through the selected USGS dataset.

This does not necessarily mean the station has permanently stopped operating. It means that no observation was returned by the dataset used by this project.

---

# Troubleshooting

## "python is not recognized"

Python may not be installed or may not be available from the command line.

Install Python 3.14.3 or newer and make sure Python is added to the system PATH during installation.

On Mac, try:

```bash
python3 --version
```

instead of:

```bash
python --version
```

---

## "No module named requests"

Run:

### Windows

```bash
pip install -r requirements.txt
```

### Mac

```bash
pip3 install -r requirements.txt
```

---

## The USGS request returns an error

Check that:

1. Your API key is correct.
2. The API key is entered in `config.py`.
3. You have an internet connection.
4. The USGS API is available.
5. You have not exceeded the API's request limit.

If the API is temporarily rate-limited, wait before trying the refresh again.

---

## The map is blank

Go to vercel to make sure the server is online and there were no build failures.

Make sure the GeoJSON files are in the web folder and are not blank or malformed.

If the problem continues, code browser's developer console and look for errors related to loading the GeoJSON files.

---

# Quarterly Maintenance

The expected quarterly workflow is:

```text
1. Download/extract the project
        ↓
2. Obtain a valid USGS API key
        ↓
3. Enter the key in config.py
        ↓
4. Run DataRetrieval.py
        ↓
5. Review the generated data
        ↓
6. code map
        ↓
7. Check several stations and readings
        ↓
8. Use the updated map for the board meeting
```

The repetitive data retrieval and processing are automated.

A person should still review the results because external APIs and monitoring networks can change. Stations can stop reporting, data fields can change, API services can change, and observations can be missing or delayed.

---

# Maintenance and Handoff

This project is intended to be simple enough for a future GIS staff member or student intern to maintain.

A future maintainer should receive:

* This README
* `DataRetrieval.py`
* `config.py`
* `requirements.txt`
* The current GeoJSON files
* The web map
* Documentation of the data sources
* Information about the most recent refresh

The USGS API key should **not** be included in a distributed ZIP file or GitHub Repository. It should be provided separately to the person responsible for maintaining the project.

---

# Project Limitations

This is a prototype designed for a quarterly board meeting rather than a full production monitoring system.

In particular:

* The map is distributed as a local web application rather than hosted publicly.
* The project displays the latest observations selected from the USGS continuous-observation dataset rather than a complete historical record.
* A station without a current reading is still shown on the map.
* Data availability depends on the external USGS API.
* The project does not automatically send notifications when a station stops reporting.
* The project does not replace the source agency's official data systems.

For a future production deployment, these areas could be expanded with scheduled data updates, historical charts, automated data-quality checks, and more detailed documentation.

---

# Contact / Handoff Notes

The person maintaining this project should review this README before each quarterly refresh and update the data-download information after each successful refresh.

If the data retrieval process stops working, the first things to check are the USGS API key, internet connection, API availability, request limits, and whether the USGS API has changed.
