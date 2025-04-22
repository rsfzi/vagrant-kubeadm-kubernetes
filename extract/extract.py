import logging
import datetime

from basequery import BaseQuery

class Extract(BaseQuery):
    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(__name__)

    def get_entries(self, args):
        sql_query = """
        SELECT log 
        FROM 'simexp'
        WHERE kubernetes_pod_name = '{}'
        ORDER by _timestamp ASC 
        """.format(args.pod)

        now = datetime.datetime.now()
        start = now - datetime.timedelta(hours=48)
        end_time = int(now.timestamp() * 10 ** 6)
        start_time =int(start.timestamp() * 10 ** 6)

        self._logger.debug("log download start")
        start_entry = 0
        count = args.limit
        total, entries = self._request_entries(args, sql_query, 'log', start_time, end_time, count, start_entry)
        while total >= count:
            start_entry += total
            total, new_entries = self._request_entries(args, sql_query, 'log', start_time, end_time, count, start_entry)
            entries.extend(new_entries)
        self._logger.debug("log download complete")
        return entries
