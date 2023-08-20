import sys
from mock import patch
import os
import json
import pytest
import requests_mock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from constants import MOCK_SERVER_FILENAME_BASE, EXPECTED_CLIENT_FILENAME_BASE, MOCK_RATES_FILENAME, \
    TESTS_DATA_FOLDER_NAME, RATES_JSON_SECTION

from app import get_payments_with_quality_check


TESTS_DATA_FOLDER_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), TESTS_DATA_FOLDER_NAME)

f = open(os.path.join(TESTS_DATA_FOLDER_PATH, MOCK_RATES_FILENAME))
MOCK_RATES = json.load(f)[RATES_JSON_SECTION]


@pytest.fixture(params=[1, 2, 4])
def mock_index_fixture_200(request):
    return request.param


@pytest.fixture(params=[3])
def mock_index_fixture_500(request):
    return request.param


def get_file_path(filename_base, mock_index):
    prefix, suffix = os.path.splitext(filename_base)
    file_name = prefix + "_" + str(mock_index) + suffix
    return os.path.join(TESTS_DATA_FOLDER_PATH, file_name)


@patch('app.RATES', MOCK_RATES)
def test_assert_200(mock_index_fixture_200):
    with requests_mock.Mocker() as requests_mocker:
        f = open(get_file_path(MOCK_SERVER_FILENAME_BASE, mock_index_fixture_200))
        mock_server_response = json.load(f)
        requests_mocker.get(
            'http://localhost:9292/api/bookings',
            status_code=200,
            json=mock_server_response,
        )

        actual_client_response = get_payments_with_quality_check()

        expected_client_response = json.load(open(get_file_path(EXPECTED_CLIENT_FILENAME_BASE, mock_index_fixture_200)))
        assert actual_client_response == (expected_client_response, 200)


@patch('app.RATES', MOCK_RATES)
def test_assert_500(mock_index_fixture_500):
    with requests_mock.Mocker() as requests_mocker:
        f = open(get_file_path(MOCK_SERVER_FILENAME_BASE, mock_index_fixture_500))
        mock_server_response = json.load(f)
        requests_mocker.get(
            'http://localhost:9292/api/bookings',
            status_code=200,
            json=mock_server_response,
        )

        actual_client_response = get_payments_with_quality_check()

        response_code = actual_client_response[1]

        assert 500 <= response_code <= 511
