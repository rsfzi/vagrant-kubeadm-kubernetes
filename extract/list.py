import logging
import datetime

from basequery import BaseQuery


class List(BaseQuery):
    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(__name__)

    def get_entries(self, args):
        sql_query = """
        SELECT DISTINCT kubernetes_pod_name 
        FROM "simexp" 
        """

        now = datetime.datetime.now()
        start = now - datetime.timedelta(hours=48)
        end_time = int(now.timestamp() * 10 ** 6)
        start_time =int(start.timestamp() * 10 ** 6)

        total, entries = self._request_entries(args, sql_query, 'kubernetes_pod_name', start_time, end_time, count=1000)
        return entries
