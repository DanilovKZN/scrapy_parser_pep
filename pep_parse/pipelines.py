import csv
import datetime as dt
from collections import defaultdict
from pathlib import Path

from scrapy.exceptions import DropItem

from pep_parse.spiders.pep import PEP_STATUS


DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

# Для прохождения теста
BASE_DIR = Path(__file__).parent


class PepParsePipeline:
    def __init__(self):
        self.total = 0
        self.status_dict = defaultdict(int)

    def open_spider(self, spider):
        # Я здесь исключительно для прохождения теста
        pass

    def process_item(self, item, spider):
        if item['status'] in PEP_STATUS:
            self.status_dict[item['status']] += 1
        else:
            self.logs[item['number']] = 'Неверный статус :('
            raise DropItem(f"Левый статус у {item['number']} PEP!")
        return item

    def close_spider(self, spider):
        result_list = []
        now = dt.datetime.now()
        now_formatted = now.strftime(DATETIME_FORMAT)
        results_dir = BASE_DIR / 'results'
        results_dir.mkdir(exist_ok=True)
        self.status_dict['Total'] = sum(self.status_dict.values())
        for item in self.status_dict:
            result_list.append((item, self.status_dict[item]))

        # Для тестов через BASE_DIR c созданием папки в pep_parse
        with open(
            BASE_DIR / f'results/status_summary_{now_formatted}.csv',
            mode='w', encoding='utf-8', newline=''
        ) as f:
            column_names = ['Статус', 'Количество']
            writer = csv.writer(f, delimiter=',')
            writer.writerow(column_names)
            writer.writerows(result_list)
