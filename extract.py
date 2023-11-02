import csv
import json

from models import NearEarthObject, CloseApproach
from helpers import cd_to_datetime


def load_neos(neo_csv_path):
    """
    Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    neo_objs = []
    with open(neo_csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Assemble a dictionary of the row data.
            info = {
                'designation': row["pdes"],
                'name': row['name'] or None,
                'diameter': float(row['diameter']) if row["diameter"] else None,
                'hazardous': row['pha'] == 'Y',  # Convert to boolean
            }
            neo = NearEarthObject(**info)
            neo_objs.append(neo)
    return neo_objs


def load_approaches(cad_json_path):
    """
    Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    approach_objs = []
    with open(cad_json_path, 'r') as file:
        data = json.load(file)  # Directly use json.load to read from file
        
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
            except ValueError as e:  # Catch a more specific exception
                print(f"Skipping approach_data {approach_data} due to error: {e}")
    return approach_objs
