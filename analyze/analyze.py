#!/usr/bin/env python3

import os
import sys
import logging.config
import argparse
import json
from pathlib import Path

class Analyze:
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

    def main(self):
        parser = argparse.ArgumentParser()
        default = ' (default: %(default)s)'
        parser.add_argument('-v', '--verbose', action='count', default=1, help="increase the verbosity level" + default)
        parser.add_argument('-l', '--logfile', help="log file")
        parser.add_argument('-i', '--input', type=argparse.FileType('r'), required=True, help="input file")
        parser.add_argument('-o', '--output', default="-", type=argparse.FileType('w', encoding='UTF-8'))
        args = parser.parse_args()

        self.start_logging(args.logfile, args.verbose)
        log = logging.getLogger(__name__)
        log.debug("### started ###")
        try:
            log.debug("read input file")
            for line in args.input:
                json_entries = json.loads(line)
                log_line = json_entries["log"]
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
    a = Analyze()
    sys.exit(a.main())
