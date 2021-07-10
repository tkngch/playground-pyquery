from pyquery.data_frame import DataFrame
from pyquery.datasource.csv_data_source import CsvDataSource
from pyquery.datasource.parquet_data_source import ParquetDataSource
from pyquery.logical_plan.logical_scan import LogicalScan


class ExecutionContext:
    def __init__(self, batch_size: int = 1024):
        self.batch_size = batch_size

    def csv(self, filename: str) -> DataFrame:
        source = CsvDataSource(filename, schema=None, batch_size=self.batch_size)
        return DataFrame(LogicalScan(filename, source, ()))

    def parquet(self, filename: str) -> DataFrame:
        source = ParquetDataSource(filename, batch_size=self.batch_size)
        return DataFrame(LogicalScan(filename, source, ()))
