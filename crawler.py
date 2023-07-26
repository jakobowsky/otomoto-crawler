import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass, asdict
from typing import List
import csv

@dataclass
class Vacancy:
    link: str
    company: str
    descript: str
    town: int
    payment: int

class GoworkScrapper: 
    def __init__(self, praca_make: str) -> None:
        self.headers = {
             "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
             "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34",
             "connection": "keep-alive",
        }
        self.praca_make = praca_make
        self.website = "https://www.gowork.pl/praca"

def scrape_pages(self, number_of_pages: int) -> List[Vacancy]:
   vacancies = []
   for i in range(1, number_of_pages + 1):
       current_page = f"{self.website}/{self.praca_make}/{i};pg"
       new_vacancies = self.scrape_vacancies_from(current_page)
       vacancies += new_vacancies
   return vacancies

def scrape_vacancies_from(self, current_page) -> List[Vacancy]:
    try: 
        response = requests.get(current_page, headers=self.headers).text
        soup = BeautifulSoup(response, "html.parser")
        vacancies = []
        for offer in soup.find_all('div', class_='job-listing__container container'):
            vacancy = Vacancy(
                link=offer.find('a', class_='job-listing__link').get('href'),
                company=offer.find('span', class_='job-listing__company').text,
                descript=offer.find('div', class_='job-listing__description').text,
                town=int(offer.find('span', class_='job-listing__location').text.split(',')[0]),
                payment=int(offer.find('span', class_='job-listing__salary').text.split('-')[0]),
            )
            vacancies.append(vacancy)
        return vacancies
    except Exception as e:
        print(f"Problems with {current_page}, reasons: {e}")
        return []

def scrape_gowork() -> None:
    praca_make = 'ua-friendly-offer;tag'
    scraper = GoworkScrapper(praca_make)
    vacancies = scraper.scrape_pages(3)
    print(vacancies)
 

if __name__ == '__main__':
    scrape_gowork()

