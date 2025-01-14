import logging
import json
import datetime

from loki.loki_urllib3_client import LokiClient


class Query:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        #import http.client
        #http.client.HTTPConnection.debuglevel = 1

    def _extract_data(self, response):
        if not response[0]:
            raise RuntimeError("error response: %s" % str(response[1]))
        json_response = response[1]
        status = json_response["status"]
        if status != "success":
            raise RuntimeError("failure: %s" % status)
        return json_response["data"]

    def _get_entries(self, stats):
        current = stats["summary"]["totalEntriesReturned"]
        total = stats["summary"]["totalPostFilterLines"]
        return total, current

    def _request_entries(self, args, loki_client, start_time=None):
        response = loki_client.query_range(args.query, start=start_time, limit=5)
        self._logger.debug("response:\n%s" % str(response))
        data = self._extract_data(response)
        #self._logger.debug("data:\n{}s".format(json.dumps(data, indent=4)))
        self._logger.debug("stats:\n{}s".format(json.dumps(data["stats"]["summary"], indent=4)))
        self._logger.debug("logs:\n{}s".format(json.dumps(data["result"], indent=4)))
        total, current = self._get_entries(data["stats"])
        #self._logger.info("received entries %s/%s" % (current, total))
        results = data["result"]

        logs = {}
        last_time_stamp = None
        for result in results:
            host, pod = result['stream']["host"], result['stream']["pod_name"]
            #self._logger.info("received entries %s/%s" % (current, total))
            #self._logger.info("logs for: %s:%s" % (host, pod))
            if not (host, pod) in logs:
                logs[(host, pod)] = []
            for time_stamp, raw_value in result['values']:
                json_value = json.loads(raw_value)
                entry = {
                    "time": time_stamp,
                    "log": json_value['log'],
                }
                logs[(host, pod)].append(entry)
                last_time_stamp = time_stamp
            #self._logger.info("last timestamp: %s" % last_time_stamp)
        return total, current, results, last_time_stamp, logs

    def _remove_duplicates(self, existing_logs, new_logs):
        result = []
        for new_entry in new_logs:
            if new_entry not in existing_logs:
                result.append(new_entry)
            else:
                self._logger.debug("exclude: %s" % new_entry["log"])
        return result

    def get_entries(self, args):
        self._logger.debug("query loki")
        loki_client = LokiClient(url=args.url)
        if not loki_client.ready():
            raise RuntimeError("loki not ready")

        logs = {}
        processed = 0
        last_time_stamp = datetime.datetime.combine(datetime.date.today(), datetime.time(8))
        while True:
            total, current, results, last_time_stamp, received_logs = self._request_entries(args, loki_client, start_time=last_time_stamp)
            processed += current
            self._logger.debug("received entries %s (%s) / %s" % (processed, current, total))

            added = 0
            for key, log_entries in received_logs.items():
                self._logger.info("received logs for: %s:%s" % key)
                if key in logs:
                    old_entries = logs[key]
                    new_logs = self._remove_duplicates(old_entries, log_entries)
                    logs[key].extend(new_logs)
                    added += len(new_logs)
                else:
                    logs[key] = log_entries
                    added += len(log_entries)
            self._logger.debug("last timestamp: %s" % last_time_stamp)
            if not added:
                break
        result_entries = []
        for key, log_entries in logs.items():
            result_entries.append("#"*50)
            result_entries.append("Pod %s:%s" % key)
            for entry in log_entries:
                result_entries.append(entry["log"])
        return result_entries
