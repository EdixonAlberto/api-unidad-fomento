from typing import Optional
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from src.modules.config import Config


class ScrapingSII(Config):
  _query_day: int
  _query_month: int

  def __init__(self, date: str) -> None:
    super().__init__()
    url_sii_chile = self.env('URL_SII_CHILE')

    if (not url_sii_chile):
      raise Exception("Environment variable 'URL_SII_CHILE' not found")

    self._query_day = int(date.split('-')[0])
    self._query_month = int(date.split('-')[1])
    query_year: str = date.split('-')[2]
    url: str = f"{url_sii_chile}/valores_y_fechas/uf/uf{query_year}.htm"

    try:
      html_response = requests.get(url)
      if (html_response.status_code == 404):
        raise Exception('not_found')
    except Exception as error:
      errors = str(error).split(':')
      error_message = errors[1].strip() if len(errors) > 1 else error

      if (error_message == 'Max retries exceeded with url'):
        raise Exception(f"Max retries exceeded with url '{url}'")
      else:
        raise error

    self.soup = BeautifulSoup(html_response.text, 'html.parser')

  def get_unit_fomento(self) -> Optional[str]:
    month_table_list = self.soup.find_all('div', class_="meses")

    month_spanish_english = {
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

    unit_fomento = None
    for month_table in month_table_list:
      if (month_table.get('id') != 'mes_all'):
        month_name: str = month_table.find('h2').text
        month_name_english: str = month_spanish_english[month_name.lower()]
        month_number: int = datetime.strptime(month_name_english, "%B").month

        if (month_number == self._query_month):
          field_list = month_table.find_all('tr')
          field_list.pop(0)

          for field in field_list:
            day_list = field.find_all('strong')
            index = 0

            for day in day_list:
              day_number: int = int(day.text)

              if (day_number == self._query_day):
                unit_fomento = field.find_all('td')[index].text
                break

              index = index + 1

    return unit_fomento
