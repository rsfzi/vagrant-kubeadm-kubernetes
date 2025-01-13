import logging
import json

from loki.loki_urllib3_client import LokiClient


class Query:
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def _extract_data(self, response):
        json_response = response[1]
        status = json_response["status"]
        if status != "success":
            raise RuntimeError("failure: %s" % status)
        return json_response["data"]

    def get_entries(self, args):
        self._logger.debug("query loki")
        loki_client = LokiClient(url=args.url)
        if not loki_client.ready():
            raise RuntimeError("loki not ready")

        response = loki_client.query_range(args.query, limit=1000)
        data = self._extract_data(response)
        results = data["result"]
        log_entries = []
        for result in results:
            for _id, raw_value in result['values']:
                json_value = json.loads(raw_value)
                log_entries.append(json_value['log'])
        return log_entries
