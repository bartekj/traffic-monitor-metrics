#!/usr/bin/python
import argparse
import datetime
import json
import time

import googlemaps
import responses

DISTANCE_MATRIX_URL = "https://maps.googleapis.com/maps/api/distancematrix/json"
API_KEY='API-KEY-FOR-MATRIX-API'


def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        description='Traffic description')
    parser.add_argument('--origin', type=str, required=True,
                        help='Origin address')
    parser.add_argument('--destination', type=str, required=True,
                        help='destination address')
    return parser.parse_args()


def main(orig, dest):
        client = googlemaps.Client(API_KEY)
        responses.add(responses.GET,
                      DISTANCE_MATRIX_URL,
                      body='{"status":"OK","rows":[]}',
                      status=200,
                      content_type='application/json')

        matrix = client.distance_matrix(orig, dest,
                                            language="pl-PL",
                                            mode="driving",
                                            traffic_model="best_guess",
                                            departure_time="now")

        rows = dict(matrix)['rows']
        duration = rows[0]['elements'][0]['duration']['value']
        distance = rows[0]['elements'][0]['distance']['value']
        duration_in_traffic = rows[0]['elements'][0]['duration_in_traffic']['value']
        json_body = { "duration": duration, "distance": distance, "duration_in_traffic": duration_in_traffic }
        print json.dumps(json_body)

if __name__ == '__main__':
    args = parse_args()
    main(orig=args.origin, dest=args.destination)
