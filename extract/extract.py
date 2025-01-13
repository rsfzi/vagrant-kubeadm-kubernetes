#!/usr/bin/env python3

import os
import sys
import logging.config
import argparse
import json
from builtins import RuntimeError
from pathlib import Path

from loki.loki_urllib3_client import LokiClient

class Extract:
    def __init__(self):
        pass

    def start_logging(self, log_file_name, arg_log_level):
        num_log_level = 50 - min(4, 2 + arg_log_level) * 10
        log_level = logging.getLevelName(num_log_level)
        script = Path(__file__).resolve()
        folder = script.parent
        config = folder / 'logging.json'

        with open(config, "rt", encoding="UTF_8") as f:
            json_config = json.load(f)
            json_config['handlers']['console']['level'] = log_level
            if log_file_name:
                json_config['handlers']['file']['filename'] = log_file_name
                json_config['loggers']['root']['handlers'].append("file")
        logging.config.dictConfig(json_config)

    def _extract_data(self, response):
        json_response = response[1]
        status = json_response["status"]
        if status != "success":
            raise RuntimeError("failure: %s" % status)
        return json_response["data"]

    def _extract(self, args):
        log = logging.getLogger(__name__)
        log.debug("read input file")
        log_entries = []
        for line in args.input:
            json_entries = json.loads(line)
            log_line = json_entries["log"]
            log_entries.append(log_line)
        return log_entries

    def _labels(self, args):
        log = logging.getLogger(__name__)
        log.debug("query loki")
        loki_client = LokiClient(url=args.url)
        if not loki_client.ready():
            raise RuntimeError("loki not ready")

        response = loki_client.labels()
        labels = self._extract_data(response)
        return labels

    def _query(self, args):
        log = logging.getLogger(__name__)
        log.debug("query loki")
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

    def main(self):
        parser = argparse.ArgumentParser()
        default = ' (default: %(default)s)'
        parser.add_argument('-v', '--verbose', action='count', default=1, help="increase the verbosity level" + default)
        parser.add_argument('-l', '--logfile', help="log file")
        parser.add_argument('-o', '--output', default="-", type=argparse.FileType('w', encoding='UTF-8'))
        subparsers = parser.add_subparsers(help='subcommand help')
        parser_extract = subparsers.add_parser('extract', help='extract log data from stream')
        parser_extract.add_argument('-i', '--input', type=argparse.FileType('r'), required=True, help="input file")
        parser_extract.set_defaults(func=self._extract)
        parser_labels = subparsers.add_parser('labels', help='query loki for labels')
        parser_labels.add_argument('--url', default='http://10.0.0.10:32031', help="loki URL" + default)
        parser_labels.set_defaults(func=self._labels)
        parser_query = subparsers.add_parser('query', help='query loki for log data')
        parser_query.add_argument('--url', default='http://10.0.0.10:32031', help="loki URL" + default)
        parser_query.add_argument('--query', required=True, help="query string")
        parser_query.set_defaults(func=self._query)

        args = parser.parse_args()

        self.start_logging(args.logfile, args.verbose)
        log = logging.getLogger(__name__)
        log.debug("### started ###")
        try:
            entries = args.func(args)
            for log_line in entries:
                args.output.write("%s\n" % log_line)
            return 0
        except KeyboardInterrupt:
            log.warning("aborted")
            return 2
        except:
            log.exception("exception:")
            return 1
        finally:
            log.debug("### finished ###")


if __name__ == "__main__":
    a = Extract()
    sys.exit(a.main())
