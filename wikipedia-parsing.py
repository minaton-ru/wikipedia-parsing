import sys
from collections import Counter
import requests
from bs4 import BeautifulSoup

# Стартовый URL для парсинга
URL = 'https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту'
# Список для сбора букв
alphabet = []

def wikiAnimalsParsing(URL):
    # Скачиваем HTML содержимое
    contents = requests.get(URL).text
    # Парсим содержимое
    soup = BeautifulSoup(contents, 'html.parser')
    # Берем основной div, в котором находится нужный список
    content_div = soup.find('div', attrs = {'class':'mw-category-columns'})

    # Итерируемся по каждому нужному нам элементу li
    for raw in content_div.select('li'):
        # Берем первую букву из текста ссылки в каждом нужном нам элементе
        first_letter = raw.a.text[0]
        # Указываем когда нужно остановиться - когда увидим английскую букву A
        if first_letter == 'A':
            # Методом счетчика получаем количество каждой буквы в нашем списке для сбора букв
            count = Counter(alphabet)
            # Сортируем элементы и кладем их как список в новый список
            sorted_alphabet = dict(sorted(count.items()))
            # Выводим на экран элементы - каждая буква и ее количество
            for letter, v in sorted_alphabet.items():
                print(f'{letter}: {v}')
            # Выходим из программы, если выполнено условие останова
            sys.exit()
        else:
            # Если условие останова не выполнено, то первую букву из текста ссылки добавляем в список для сбора букв
            alphabet.append(first_letter)
    # Берем со страницы URl, который находится в элементе с текстом Следующая страница
    next_url = soup.find('a', text='Следующая страница')
    # Запускаем эту же функцию со следующим URL
    wikiAnimalsParsing("https://ru.wikipedia.org" + next_url.get('href'))

wikiAnimalsParsing(URL)
