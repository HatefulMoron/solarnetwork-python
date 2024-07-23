from datetime import datetime
import requests

from solarnetwork_python.authentication import generate_auth_header, get_x_sn_date


class Client:
    def __init__(self, token: str, secret: str) -> None:
        self.token = token
        self.secret = secret

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
