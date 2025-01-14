import logging

from loki.loki_urllib3_client import LokiClient


class Labels:
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

        response = loki_client.labels()
        labels = self._extract_data(response)
        label_content = []
        for label in labels:
            response = loki_client.label_values(label)
            label_values = self._extract_data(response)
            label_content.append("%-8s: %s" % (label, ",".join(label_values)))
        return label_content
