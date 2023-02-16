import os
import time
import argparse

import pyarrow as pa
import pyarrow.flight


def list_flights(client, interval=1):
    while True:
        try:
            for flight in client.list_flights():
                print(flight.descriptor.path)
        except Exception as e:
            print(e)

        time.sleep(interval)


def get_flight_info_not_found(client, interval=1):
    print("get_flight_info_not_found")

    desc = pa.flight.FlightDescriptor.for_path("notfound.parquet")

    while True:
        try:
            print(client.get_flight_info(desc))
        except Exception as e:
            print(e)

        time.sleep(interval)


def example_put(client, interval=1):
    print("example_put")

    # Upload a new dataset
    data_table = pa.table(
        [["Mario", "Luigi", "Peach"]],
        names=["Character"]
    )

    while True:
        try:
            upload_descriptor = pa.flight.FlightDescriptor.for_path(
                "characters.parquet")
            writer, _ = client.do_put(upload_descriptor, data_table.schema)
            writer.write_table(data_table)
            writer.close()

            print(f"do_put on {upload_descriptor} finished")

        except Exception as e:
            print(e)

        time.sleep(interval)


if __name__ == "__main__":
    routine = os.getenv("ROUTINE", "get_flight_info_not_found")

    routines = {
        "example_put": example_put,
        "get_flight_info_not_found": get_flight_info_not_found,
        "list_flights": list_flights
    }

    if routine not in routines:
        raise ValueError(
            f"Routine '{routine}' not one of {list(routines.keys())}")

    client = pa.flight.connect(os.getenv("ENDPOINT", "grpc://localhost:8815"))

    print(f"Running routine {routine}")
    routines[routine](client)
