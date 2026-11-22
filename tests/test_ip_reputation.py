
import pytest
import requests

from Jamal_project.ip_reputation import check_ip_reputation


def test_check_ip_reputation(mocker):
    fake_response = mocker.Mock()

    fake_response.json.return_value = {
        "data": {
            "ipAddress": "8.8.8.8",
            "abuseConfidenceScore": 0,
            "countryCode": "US",
            "totalReports": 0,
        }
    }

    fake_response.raise_for_status.return_value = None

    mocker.patch(
        "Jamal_project.ip_reputation.requests.get",
        return_value=fake_response
    )

    mocker.patch(
        "Jamal_project.ip_reputation.API_KEY",
        "fake_api_key"
    )

    result = check_ip_reputation("8.8.8.8")

    assert result["abuse_score"] == 0
    assert result["country"] == "US"


def test_check_ip_reputation_timeout(mocker):
    mocker.patch(
        "Jamal_project.ip_reputation.API_KEY",
        "fake_api_key"
    )

    mocker.patch(
        "Jamal_project.ip_reputation.requests.get",
        side_effect=requests.exceptions.Timeout
    )

    with pytest.raises(RuntimeError, match="timed out"):
        check_ip_reputation("8.8.8.8")


def test_check_ip_reputation_http_error(mocker):
    mocker.patch(
        "Jamal_project.ip_reputation.API_KEY",
        "fake_api_key"
    )

    mocker.patch(
        "Jamal_project.ip_reputation.requests.get",
        side_effect=requests.exceptions.HTTPError("403 Forbidden")
    )

    with pytest.raises(RuntimeError, match="AbuseIPDB returned an error"):
        check_ip_reputation("8.8.8.8")


def test_check_ip_reputation_missing_api_key(mocker):
    mocker.patch(
        "Jamal_project.ip_reputation.API_KEY",
        None
    )

    with pytest.raises(RuntimeError, match="ABUSEIPDB_KEY is not set"):
        check_ip_reputation("8.8.8.8")
