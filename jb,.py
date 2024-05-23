import requests
from bs4 import BeautifulSoup
import json

# URL для поиска вакансий Python в Москве и Санкт-Петербурге
url = "https://spb.hh.ru/search/vacancy?text=Python&area=1&area=2&order_by=publication_time"

# Заголовок User-Agent для запроса
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
}

# HTTP-запрос к сайту
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Список для сохранения информации о вакансиях
vacancies = []

# Поиск всех блоков с вакансиями
for vacancy in soup.find_all('div', class_='serp-item'):
    # Парсинг названия вакансии и ссылки
    title_tag = vacancy.find('a', class_='serp-item__title')
    if not title_tag:
        continue
    title = title_tag.text.strip()
    link = title_tag['href']

    # Парсинг названия компании
    company_tag = vacancy.find('a', class_='bloko-link bloko-link_kind-tertiary')
    company = company_tag.text.strip() if company_tag else 'Не указано'

    # Парсинг города
    city_tag = vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy-address'})
    city = city_tag.text.strip() if city_tag else 'Не указан'

    # Парсинг вилки зарплат
    salary_tag = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
    salary = salary_tag.text.strip() if salary_tag else 'Не указана'

    # Парсинг описания вакансии
    description_tag = vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'})
    description = description_tag.text.strip() if description_tag else ''

    # Проверка наличия ключевых слов в описании
    if 'Django' in description or 'Flask' in description:
        vacancies.append({
            'link': link,
            'salary': salary,
            'company': company,
            'city': city,
            'title': title
        })

# Сохранение в JSON файл
with open('vacancies.json', 'w', encoding='utf-8') as f:
    json.dump(vacancies, f, ensure_ascii=False, indent=4)

print(f'Найдено и сохранено {len(vacancies)} вакансий.')
