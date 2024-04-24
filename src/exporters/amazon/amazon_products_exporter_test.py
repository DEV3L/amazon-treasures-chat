from unittest.mock import MagicMock, Mock, patch

import pytest
from pandas import DataFrame

from src.exporters.amazon.amazon_products_exporter import AmazonProductsExporter
from src.exporters.exporter import BIN_DIR, DATA_DIR, DATA_FILE_PREFIX


@pytest.fixture(name="exporter")
def build_exporter():
    return AmazonProductsExporter()


@patch("src.exporters.amazon.amazon_products_exporter.create_dir")
@patch("src.exporters.amazon.amazon_products_exporter.does_data_exist")
def test_export_data_exists(mock_does_data_exist, mock_create_dir, exporter):
    mock_does_data_exist.return_value = True

    exporter.export()

    mock_create_dir.assert_not_called()


@patch("src.exporters.amazon.amazon_products_exporter.create_dir")
@patch("src.exporters.amazon.amazon_products_exporter.does_data_exist")
def test_export_data_does_not_exist(mock_does_data_exist, mock_create_dir, exporter):
    mock_does_data_exist.return_value = False

    exporter.write_data = Mock()

    exporter.export()

    mock_create_dir.assert_called_once()
    exporter.write_data.assert_called_once()


def test_write_data():
    exporter = AmazonProductsExporter()
    exporter.get_file_path = MagicMock(return_value="test_path")

    with patch.object(DataFrame, "to_json") as mock_to_json:
        exporter.write_data()

    assert mock_to_json.call_count == 10
    mock_to_json.assert_any_call("test_path_part_0.json", orient="records")


def test_get_dir_path(exporter):
    result = exporter.get_dir_path()

    assert result == f"{BIN_DIR}/amazon"


def test_data_dir_path(exporter):
    result = exporter.get_data_path()

    assert result == f"{DATA_DIR}/amazon"


def test_get_file_path(exporter):
    result = exporter.get_file_path()

    assert result == f"{BIN_DIR}/amazon/{DATA_FILE_PREFIX}_products"
