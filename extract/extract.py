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

        self._logger.debug("log download start")
        start_time, end_time = self._get_times(datetime.timedelta(hours=48))
        start_entry = 0
        count = args.limit
        total, entries = self._request_entries(args, sql_query, 'log', start_time, end_time, count, start_entry)
        while total >= count:
            for entry in entries:
                yield entry
            start_entry += total
            total, entries = self._request_entries(args, sql_query, 'log', start_time, end_time, count, start_entry)
        self._logger.debug("log download complete")
