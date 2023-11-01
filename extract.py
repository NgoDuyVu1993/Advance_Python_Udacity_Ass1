"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach
from helpers import cd_to_datetime


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    # TODO: Load NEO data from the given CSV file.
    neo_objs = []
    with open(neo_csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
          ## print(f"Row Data: {row}")  # Debugging line
          info = {
                'designation': row["pdes"],
                'name': row['name'] or None,
                'diameter': float(row['diameter']) if row["diameter"] else None,
                'hazardous': row['pha'] == 'Y'  # Convert to boolean
          }
          ## print(info)  # Debugging line
          neo = NearEarthObject(**info) 
          neo_objs.append(neo)
    return neo_objs


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    approach_objs = []
    with open(cad_json_path, 'r') as file:
        content = file.read()
        data = json.loads(content)
        
        approaches_list = data.get('data', [])
        
        for approach_data in approaches_list:
            try:
                approach_dict = {
                    'designation': approach_data[0],
                    'datetime': approach_data[3],
                    'distance': float(approach_data[4]),
                    'velocity': float(approach_data[7]),
                }
                approach_objs.append(CloseApproach(**approach_dict))
            except Exception as e:
                print(f"Skipping approach_data {approach_data} due to error: {e}")
    return approach_objs
