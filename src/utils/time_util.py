from typing import Optional, Union
from datetime import datetime


class Date():
  @staticmethod
  def validate_format_date(date: str) -> Optional[datetime]:
    """Method to validate format of date: 01-01-2013"""
    try:
      query_datetime = datetime.strptime(date, '%d-%m-%Y')
      return query_datetime
    except:
      return

  @staticmethod
  def get_timestamp_utc(date: datetime = datetime.utcnow()) -> str:
    """Method to get timestamp in format utc"""
    return str(date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))

  @staticmethod
  def translate_month_english(month: Union[str, int]) -> str:
    """Method to translate month of spanish to english"""
    month_dict = {
        'enero': 'january',
        'febrero': 'february',
        'marzo': 'march',
        'abril': 'april',
        'mayo': 'may',
        'junio': 'june',
        'julio': 'july',
        'agosto': 'august',
        'septiembre': 'september',
        'octubre': 'october',
        'noviembre': 'november',
        'diciembre': 'december'
    }
    if (isinstance(month, str)):
      return month_dict[month.lower()]
    else:
      return list(month_dict.values())[month - 1]
