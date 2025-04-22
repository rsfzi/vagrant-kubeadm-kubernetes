import logging
import datetime

from basequery import BaseQuery


class List(BaseQuery):
    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(__name__)

    def _get_field(self):
        return None

    def get_entries(self, args):
        field = self._get_field()
        sql_query = """
        SELECT DISTINCT {} 
        FROM "simexp" 
        """.format(field)

        now = datetime.datetime.now()
        start = now - datetime.timedelta(hours=48)
        end_time = int(now.timestamp() * 10 ** 6)
        start_time =int(start.timestamp() * 10 ** 6)

        total, entries = self._request_entries(args, sql_query, field, start_time, end_time, count=1000)
        return entries


class ListPods(List):
    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(__name__)

    def _get_field(self):
        return 'kubernetes_pod_name'


class ListNodes(List):
    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(__name__)

    def _get_field(self):
        return 'kubernetes_host'
