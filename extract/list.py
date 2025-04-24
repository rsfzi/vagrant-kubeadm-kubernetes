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

        start_time, end_time = self._get_times(datetime.timedelta(hours=args.past))
        total, entries = self._request_entries(args, sql_query, field, start_time, end_time, count=1000)
        for entry in entries:
            yield entry


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
