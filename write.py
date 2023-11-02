import csv
import json

def write_to_csv(results, filename):
    """
    Write an iterable of `CloseApproach` objects to a CSV file.

    The output CSV file will have a header row, followed by a row for each
    CloseApproach object. Each row contains data on the close approach and
    its associated near-Earth object.

    Parameters:
    results: An iterable of `CloseApproach` objects.
    filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    )
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for approach in results:
            writer.writerow(approach.serialize())


def write_to_json(results, filename):
    """
    Write an iterable of `CloseApproach` objects to a JSON file.

    The output is a list of dictionaries, each representing a CloseApproach.
    The 'neo' key maps to a dictionary of the associated NEO's attributes.

    Parameters:
    results: An iterable of `CloseApproach` objects.
    filename: A Path-like object pointing to where the data should be saved.
    """
    with open(filename, 'w') as outfile:
        json.dump([approach.serialize() for approach in results], outfile, allow_nan=True)
