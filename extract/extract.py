import logging
import json


class Extract:
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def get_entries(self, args):
        self._logger.debug("read input file")
        log_entries = []
        for line in args.input:
            json_entries = json.loads(line)
            log_line = json_entries["log"]
            log_entries.append(log_line)
        return log_entries
