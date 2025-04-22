import logging
import http

import requests
from requests.auth import HTTPBasicAuth

class BaseQuery:
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def _request_entries(self, args, sql_query, field, start_time, end_time, count, start_entry=0):
        url = "http://{}:32080/api/default/_search".format(args.host)
        auth = HTTPBasicAuth(args.user, args.password)
        request = {
            "query": {
                "sql": sql_query,
                "start_time": start_time,
                "end_time": end_time,
                "from": start_entry,
                "size": count
            },
        }
        self._logger.debug("request from {} count: {}".format(start_entry, count))
        response = requests.post(url, json=request, auth=auth)
        if response.status_code != http.HTTPStatus.OK:
            raise RuntimeError("Error ({}): {}".format(response.status_code, response.text))
        results = response.json()
        total = results["total"]
        self._logger.debug("received {} entries".format(total))
        entries = [row[field] for row in results.get("hits", [])]
        return total, entries
