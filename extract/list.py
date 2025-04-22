import logging
import json
import datetime
import http

import requests
from requests.auth import HTTPBasicAuth


class List:
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def _request_entries(self, url, auth, sql_query, start_time, end_time, start_entry, size):
        request = {
            "query": {
                "sql": sql_query,
                "start_time": start_time,
                "end_time": end_time,
                "from": start_entry,
                "size": size
            },
        }
        self._logger.info("request from {} count: {}".format(start_entry, size))
        response = requests.post(url, json=request, auth=auth)
        if response.status_code != http.HTTPStatus.OK:
            raise RuntimeError("Error ({}): {}".format(response.status_code, response.text))
        results = response.json()
        #print("result:\n%s" % json.dumps(results, indent=2))
        total = results["total"]
        self._logger.info("received {} entries".format(total))
        #scan_records =
        entries = [row['kubernetes_pod_name'] for row in results.get("hits", [])]
        return total, entries

    def get_entries(self, args):
        self._logger.debug("query openobserve")

        base_url = "http://localhost:32080"
        auth = HTTPBasicAuth("root@example.com", "admin")

        sql_query = """
        SELECT DISTINCT kubernetes_pod_name 
        FROM "simexp" 
        """

        now = datetime.datetime.now()
        start = now - datetime.timedelta(hours=48)
        end_time = int(now.timestamp() * 10 ** 6)
        start_time =int(start.timestamp() * 10 ** 6)

        url = "{}/api/default/_search".format(base_url)

        start_entry = 0
        request_size = 10000
        total, entries = self._request_entries(url, auth, sql_query, start_time, end_time, start_entry, request_size)
        return entries
