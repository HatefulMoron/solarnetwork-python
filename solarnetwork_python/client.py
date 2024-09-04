from datetime import datetime
import json
import requests

from solarnetwork_python.authentication import generate_auth_header, get_x_sn_date

class Client:
    def __init__(self, token: str, secret: str) -> None:
        self.token = token
        self.secret = secret

    # Description is a dictionary that looks like this:
    # {
    #   "name": "Test Import",
    #   "stage": true,
    #   "inputConfiguration": {
    #     "name": "Test Input",
    #     "timeZoneId": "America/New_York",
    #     "serviceIdentifier": "net.solarnetwork.central.datum.imp.standard.BasicCsvDatumImportInputFormatService",
    #     "serviceProperties": {
    #       "headerRowCount": "0",
    #       "dateColumnsValue": "1",
    #       "dateFormat": "MM/dd/yyyy HH:mm:ss",
    #       "nodeIdColumn": "2",
    #       "sourceIdColumn": "3"
    #     }
    #   }
    # }
    # 
    # Data is the actual CSV data in string form.
    def import_data(self, description, data):
        # The time has to be in UTC
        now = datetime.utcnow()
        date = get_x_sn_date(now)
        path = "/solaruser/api/v1/sec/user/import/jobs"

        # These should be present for all API calls
        headers = {"content-type": "multipart/form-data; charset=utf-8; boundary=__X_PAW_BOUNDARY__", "host": "data.solarnetwork.net", "x-sn-date": date}

        description_data = json.dumps(description)

        body = (
            f'--__X_PAW_BOUNDARY__\r\n'
            f'Content-Disposition: form-data; name="config"\r\n'
            f'Content-Type: application/json\r\n'
            f'\r\n'
            f'{description_data}\r\n'
            f'--__X_PAW_BOUNDARY__\r\n'
            f'Content-Disposition: form-data; name="data"; filename="data.csv"\r\n'
            f'Content-Type: text/csv\r\n'
            f'\r\n'
            f'{data}\r\n'
            f'--__X_PAW_BOUNDARY__--\r\n'
        )

        auth = generate_auth_header(
            self.token, self.secret, "POST", path, "", headers, body, now
        )

        resp = requests.post(
            url="https://data.solarnetwork.net/solaruser/api/v1/sec/user/import/jobs",
            data=body,

            # Make sure to actually include the headers given by the previous
            # headers argument
            headers={
                "Content-Type": "multipart/form-data; charset=utf-8; boundary=__X_PAW_BOUNDARY__",
                "host": "data.solarnetwork.net",
                "x-sn-date": date,
                "Authorization": auth,
            },
        )

        v = resp.json()
        if v["success"] != True:
            raise Exception("Unsuccessful API call")

        return v["data"]

    def nodes(self) -> list[int]:
        # Documentation for this route is here:
        # https://github.com/SolarNetwork/solarnetwork/wiki/SolarQuery-API#reportable-nodes

        # The time has to be in UTC
        now = datetime.utcnow()
        date = get_x_sn_date(now)
        path = "/solarquery/api/v1/sec/nodes"

        # These should be present for all API calls
        headers = {"host": "data.solarnetwork.net", "x-sn-date": date}

        # Note that we don't include any query parameters, or anything in the
        # body. These should be added as needed
        auth = generate_auth_header(
            self.token, self.secret, "GET", path, "", headers, "", now
        )

        resp = requests.get(
            url="https://data.solarnetwork.net/solarquery/api/v1/sec/nodes",

            # Make sure to actually include the headers given by the previous
            # headers argument
            headers={
                "host": "data.solarnetwork.net",
                "x-sn-date": date,
                "Authorization": auth,
            },
        )

        v = resp.json()
        if v["success"] != True:
            raise Exception("Unsuccessful API call")

        return v["data"]
