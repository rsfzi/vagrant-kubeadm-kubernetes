import logging
import json
import datetime
import http

import requests
from requests.auth import HTTPBasicAuth

class Extract:
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
        #self._logger.info("result:\n%s" % json.dumps(results, indent=2))
        total = results["total"]
        self._logger.info("received {} entries".format(total))
        entries = [row['log'] for row in results.get("hits", [])]
        return total, entries

    def get_entries(self, args):
        self._logger.debug("query openobserve")

        base_url = "http://localhost:32080"
        auth = HTTPBasicAuth("root@example.com", "admin")

        sql_query = """
        SELECT log 
        FROM 'simexp'
        WHERE kubernetes_pod_name = 'simexp-c6f6d95f4-ljb99'
        ORDER by _timestamp DESC 
        """

        now = datetime.datetime.now()
        start = now - datetime.timedelta(hours=48)
        end_time = int(now.timestamp() * 10 ** 6)
        start_time =int(start.timestamp() * 10 ** 6)

        url = "{}/api/default/_search".format(base_url)

        start_entry = 0
        request_size = 20000
        total, entries = self._request_entries(url, auth, sql_query, start_time, end_time, start_entry, request_size)
        while total >= request_size:
            start_entry += total
            total, new_entries = self._request_entries(url, auth, sql_query, start_time, end_time, start_entry, request_size)
            entries.extend(new_entries)
        return entries
