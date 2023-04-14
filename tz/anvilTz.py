from datetime import datetime, timedelta, timezone, tzinfo

UTC = timezone.utc


class tzoffset(tzinfo):
    def __init__(self, seconds=0, minutes=0, hours=0):
        self._offset = timedelta(hours=hours, minutes=minutes, seconds=0)

    def utcoffset(self, dt):
        return self._offset

    def tzname(self, dt):
        return f"UTC{self._offset:+}"

    def dst(self, dt):
        return timedelta(0)


class tzlocal(tzoffset):
    """Use the local timezone of the browser"""

    def __init__(self):
        super().__init__(datetime.now().second, datetime.now().minute, datetime.now().hour)


class tzutc(tzoffset):
    def __init__(self):
        super().__init__(datetime.utcnow().second, datetime.utcnow().minute, datetime.utcnow().hour)
