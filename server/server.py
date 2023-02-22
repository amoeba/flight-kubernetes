import pathlib
import random
import ctypes

import logging

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)

import pyarrow as pa
import pyarrow.flight
import pyarrow.parquet as pq


def should_crash(threshold=0.1):
    return random.random() < threshold


def segfault():
    print("Causing segfault...")

    p = ctypes.pointer(ctypes.c_char.from_address(5))
    p[0] = b"x"


def maybe_crash():
    if should_crash():
        segfault()


def generate_test_data():
    # Upload a new dataset
    data_table = pa.table([["Mario", "Luigi", "Peach"]], names=["Character"])

    pq.write_table(data_table, "./datasets/characters.parquet")
    pq.read_table("./datasets/characters.parquet")


class FlightServer(pa.flight.FlightServerBase):
    def __init__(
        self, location="grpc://0.0.0.0:8815", repo=pathlib.Path("./datasets"), **kwargs
    ):
        super(FlightServer, self).__init__(location, **kwargs)
        self._location = location
        self._repo = repo

        logging.info(f"Flight now serving on {location}")

    def _make_flight_info(self, dataset):
        dataset_path = self._repo / dataset
        schema = pa.parquet.read_schema(dataset_path)
        metadata = pa.parquet.read_metadata(dataset_path)
        descriptor = pa.flight.FlightDescriptor.for_path(dataset.encode("utf-8"))
        endpoints = [pa.flight.FlightEndpoint(dataset, [self._location])]
        return pyarrow.flight.FlightInfo(
            schema, descriptor, endpoints, metadata.num_rows, metadata.serialized_size
        )

    def list_flights(self, context, criteria):
        logging.info("list_flights")

        for dataset in self._repo.iterdir():
            yield self._make_flight_info(dataset.name)

    def get_flight_info(self, context, descriptor):
        logging.info("get_flight_info")

        return self._make_flight_info(descriptor.path[0].decode("utf-8"))

    def do_put(self, context, descriptor, reader, writer):
        logging.info("do_put")

        dataset = descriptor.path[0].decode("utf-8")
        dataset_path = self._repo / dataset
        data_table = reader.read_all()

        with pq.ParquetWriter(dataset_path, data_table.schema) as writer:
            for _ in range(10):
                writer.write_table(data_table)

        logging.info(f"{descriptor} successfully written")


if __name__ == "__main__":
    server = FlightServer()
    server._repo.mkdir(exist_ok=True)
    generate_test_data()
    server.serve()
