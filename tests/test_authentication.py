import datetime

from solarnetwork_python.authentication import (
    generate_canonical_request_message,
    generate_signing_key_hex,
    generate_signing_message,
    get_x_sn_date,
)


def test_x_sn_date():
    dt = datetime.datetime.strptime(
        "Fri, 03 Mar 2017 04:36:28", "%a, %d %b %Y %H:%M:%S"
    )
    out = get_x_sn_date(dt)
    assert out == "Fri, 03 Mar 2017 04:36:28 GMT"


def test_generate_signing_key():
    dt = datetime.datetime.strptime("2017 01 01", "%Y %m %d")
    secret = "ABC123"
    request = "snws2_request"
    output = generate_signing_key_hex(secret, dt, request)

    assert output == "1f96b28b651285e49d06989aebaee169fa67a5f6a07fb72a8325fce83b425ad6"


def test_generate_signing_message():
    dt = datetime.datetime.strptime("2017 03 03 04:36:28", "%Y %m %d %H:%M:%S")
    append = "8f732085380ed6dc18d8556a96c58c820b0148852a61b3c828cb9cfd233ae05f"
    output = generate_signing_message(dt, append)

    assert (
        output
        == "SNWS2-HMAC-SHA256\n20170303T043628Z\n638e239e66bbc12eeba45f7bb812042ba233033a3550f42f03ce50962fba9845"
    )


def test_generate_canonical_request_message():
    verb = "GET"
    uri = "/solarquery/api/v1/sec/datum/mostRecent"
    header_list = {
        "host": "data.solarnetwork.net",
        "x-sn-date": "Thu, 01 Jun 2023 13:15:50 GMT",
    }
    body = ""
    output = generate_canonical_request_message(
        verb, uri, "nodeId=2&sourceIds=3", header_list, body
    )
    assert (
        output
        == "GET\n/solarquery/api/v1/sec/datum/mostRecent\nnodeId=2&sourceIds=3\nhost:data.solarnetwork.net\nx-sn-date:Thu, 01 Jun 2023 13:15:50 GMT\nhost;x-sn-date\ne3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )
