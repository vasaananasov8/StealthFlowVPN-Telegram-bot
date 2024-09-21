from datetime import datetime

from dateutil.relativedelta import relativedelta


def add_mount(dt: datetime, month: int) -> datetime:
    return datetime.now() + relativedelta(months=month)
