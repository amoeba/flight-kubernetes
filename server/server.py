import pathlib
import random
import ctypes

import pyarrow as pa
import pyarrow.flight
import pyarrow.parquet as pq


def should_crash():
    return random.random() < 0.1


def segfault():
    print("Exiting...")

    p = ctypes.pointer(ctypes.c_char.from_address(5))
    p[0] = b'x'


def maybe_crash():
    if should_crash():
        segfault()


class FlightServer(pa.flight.FlightServerBase):

    def __init__(self, location="grpc://0.0.0.0:8815",
                 repo=pathlib.Path("./datasets"), **kwargs):
        super(FlightServer, self).__init__(location, **kwargs)
        self._location = location
        self._repo = repo

    def _make_flight_info(self, dataset):
        dataset_path = self._repo / dataset
        schema = pa.parquet.read_schema(dataset_path)
        metadata = pa.parquet.read_metadata(dataset_path)
        descriptor = pa.flight.FlightDescriptor.for_path(
            dataset.encode('utf-8')
        )
        endpoints = [pa.flight.FlightEndpoint(dataset, [self._location])]
        return pyarrow.flight.FlightInfo(schema,
                                         descriptor,
                                         endpoints,
                                         metadata.num_rows,
                                         metadata.serialized_size)

    def list_flights(self, context, criteria):
        print("list_flights")

        maybe_crash()

        for dataset in self._repo.iterdir():
            yield self._make_flight_info(dataset.name)

    def get_flight_info(self, context, descriptor):
        print("get_flight_info")

        maybe_crash()

        return self._make_flight_info(descriptor.path[0].decode('utf-8'))

    def do_put(self, context, descriptor, reader, writer):
        print("do_put")

        maybe_crash()

        dataset = descriptor.path[0].decode('utf-8')
        dataset_path = self._repo / dataset
        data_table = reader.read_all()

        # pa.parquet.write_table(data_table, dataset_path)

        with pq.ParquetWriter(dataset_path, data_table.schema) as writer:
            for _ in range(10):
                maybe_crash()
                writer.write_table(data_table)

        print(f"{descriptor} successfully written")


if __name__ == "__main__":
    server = FlightServer()
    server._repo.mkdir(exist_ok=True)
    server.serve()
