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
        WHERE kubernetes_pod_name = 'simexp-c6f6d95f4-ljb99'
        ORDER by _timestamp DESC 
        """

        now = datetime.datetime.now()
        start = now - datetime.timedelta(hours=48)
        end_time = int(now.timestamp() * 10 ** 6)
        start_time =int(start.timestamp() * 10 ** 6)

        start_entry = 0
        count = 20000
        total, entries = self._request_entries(args, sql_query, 'log', start_time, end_time, count, start_entry)
        while total >= count:
            start_entry += total
            total, new_entries = self._request_entries(args, sql_query, 'log', start_time, end_time, count, start_entry)
            entries.extend(new_entries)
        return entries
