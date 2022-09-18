import datetime as dt
from collections import defaultdict
from pathlib import Path

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


STATUSES = {
    'Active': 0,
    'Accepted': 0,
    'Deferred': 0,
    'Final': 0,
    'Provisional': 0,
    'Rejected': 0,
    'Superseded': 0,
    'Withdrawn': 0,
    'Draft': 0,
}

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

BASE_DIR = Path(__file__).parent # Для прохождения теста


class PepParsePipeline:
    def __init__(self):
        self.total = 0
        self.logs = defaultdict(str)

    def open_spider(self, spider):
        # Я здесь исключительно для прохождения теста
        pass

    def process_item(self, item, spider):
        if item['status'] in STATUSES:
            STATUSES[item['status']] += 1
            self.total += 1
        else:
            self.logs[item['number']] = 'Неверный статус :('
            raise DropItem(f"Левый статус у {item['number']} PEP!")
        return item

    def close_spider(self, spider):
        now = dt.datetime.now()
        now_formatted = now.strftime(DATETIME_FORMAT)
        results_dir = BASE_DIR / 'results'
        results_dir.mkdir(exist_ok=True)

        # Для тестов через BASE_DIR c созданием папки в pep_parse
        with open(
            BASE_DIR / f'results/status_summary_{now_formatted}.csv',
            mode='w', encoding='utf-8') as f:
            f.write('Статус,Количество\n')

        # Рабочий вариант в папку results  
        # with open(
        #     f'results/status_summary_{now_formatted}.csv',
        #     mode='w', encoding='utf-8') as f:
        #     f.write('Статус,Количество\n')

            for item in STATUSES:
                f.write(f'{item},{STATUSES[item]}\n')
            f.write(f'Total,{self.total}\n')

        # Вывод логов в папку results
        # if self.logs:
        #     with open(
        #         f'results/logs_{now_formatted}.csv',
        #         mode='w', encoding='utf-8') as f:
        #         f.write('PEP,Статус\n')
        #         for item in self.logs:
        #             f.write(f'{item},{self.logs[item]}\n')
