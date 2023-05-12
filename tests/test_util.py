from src.utils.time_util import Date, datetime


def test_format_date():
  query_date: str = '01-01-2013'
  query_datetime = Date.validate_format_date(query_date)
  assert query_datetime == datetime(2013, 1, 1, 0, 0)


def test_timestamp():
  query_datetime: datetime = datetime(2023, 5, 11, 18, 8, 53, 11418)
  timestamp: str = Date.get_timestamp_utc(query_datetime)
  assert timestamp == '2023-05-11T18:08:53.011418Z'


def test_month_english():
  datenow: datetime = datetime.now()
  month_number: int = datenow.month
  month_english: str = Date.translate_month_english(month_number)
  assert month_english == datenow.strftime('%b').lower()
