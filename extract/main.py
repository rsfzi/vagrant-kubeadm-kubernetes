#!/usr/bin/env python3

import sys
import logging.config
import argparse
import json
from pathlib import Path

from list import ListPods, ListNodes
from extract import Extract

class Main:
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
                json_config['loggers']['']['handlers'].append("file")
        logging.config.dictConfig(json_config)

    def main(self):
        parser = argparse.ArgumentParser()
        default = ' (default: %(default)s)'
        parser.add_argument('-v', '--verbose', action='count', default=1, help="increase the verbosity level" + default)
        parser.add_argument('-l', '--logfile', help="log file")
        parser.add_argument('-o', '--output', default="-", type=argparse.FileType('w', encoding='UTF-8'))
        parser.add_argument( '--host', default="10.0.0.10", help="openobserve host" + default)
        parser.add_argument('--user', default="root@example.com", help="user" + default)
        parser.add_argument('--password', default="admin", help="admin")
        subparsers = parser.add_subparsers(help='subcommand help', required=True)
        parser_list = subparsers.add_parser('list', help='list log attributes')
        subparsers_list = parser_list.add_subparsers(help='list subcommands help', required=True)
        parser_list_pods = subparsers_list.add_parser('pods', help='list pods')
        parser_list_pods.set_defaults(func=ListPods)
        parser_list_nodes = subparsers_list.add_parser('nodes', help='list nodes')
        parser_list_nodes.set_defaults(func=ListNodes)
        parser_extract = subparsers.add_parser('extract', help='extract log data from openobserve')
        parser_extract.set_defaults(func=Extract)
        parser_extract.add_argument('--pod', help="pod name")
        parser_extract.add_argument('--limit', type=int,default=16384, help="request limit" + default)

        args = parser.parse_args()

        self.start_logging(args.logfile, args.verbose)
        log = logging.getLogger(__name__)
        log.debug("### extract started ###")
        try:
            processor = args.func()
            entries = processor.get_entries(args)
            for log_line in entries:
                args.output.write("%s\n" % log_line)
            return 0
        except KeyboardInterrupt:
            log.warning("extract aborted")
            return 2
        except:
            log.exception("exception:")
            return 1
        finally:
            log.debug("### extract finished ###")


if __name__ == "__main__":
    m = Main()
    sys.exit(m.main())
