import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass, asdict
from typing import List
import csv


@dataclass
class Car:
    link: str
    full_name: str
    description: str
    year: int
    mileage_km: str
    engine_capacity: str
    fuel_type: str
    price_pln: int


class OtomotoScraper:
    def __init__(self, car_make: str) -> None:
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.11 (KHTML, like Gecko) "
            "Chrome/23.0.1271.64 Safari/537.11",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
            "Accept-Encoding": "none",
            "Accept-Language": "en-US,en;q=0.8",
            "Connection": "keep-alive",
        }
        self.car_make = car_make

        self.website = "https://www.otomoto.pl/osobowe"

    def scrape_pages(self, number_of_pages: int) -> List[Car]:
        cars = []
        for i in range(1, number_of_pages + 1):
            current_website = f"{self.website}/{self.car_make}/?page={i}"
            new_cars = self.scrape_cars_from_current_page(current_website)
            if new_cars:
                cars += new_cars
        return cars

    def scrape_cars_from_current_page(self, current_website: str) -> List[Car]:
        try:
            response = requests.get(current_website, headers=self.headers).text
            soup = BeautifulSoup(response, "html.parser")
            cars = self.extract_cars_from_page(soup)
            return cars
        except Exception as e:
            print(f"Problem with scraping website: {current_website}, reason: {e}")
            return []

    def extract_cars_from_page(self, soup: BeautifulSoup) -> List[Car]:
        offers_table = soup.find("div", class_="offers list")
        cars = offers_table.find_all("article")
        list_of_cars = []
        for car in cars:
            try:
                link = (
                    car.find("h2", class_="offer-title")
                    .find("a", href=True)
                    .get("href")
                )
                full_name = (
                    car.find("h2", class_="offer-title")
                    .find("a", href=True)
                    .get("title")
                )
                description = car.find(
                    "h3", class_="offer-item__subtitle ds-title-complement hidden-xs"
                ).text
                year = (
                    car.find("ul", class_="ds-params-block")
                    .find(attrs={"data-code": "year"})
                    .text.strip()
                )
                mileage_km = (
                    car.find("ul", class_="ds-params-block")
                    .find(attrs={"data-code": "mileage"})
                    .text.strip()
                )
                engine_capacity = (
                    car.find("ul", class_="ds-params-block")
                    .find(attrs={"data-code": "engine_capacity"})
                    .text.strip()
                )
                fuel_type = (
                    car.find("ul", class_="ds-params-block")
                    .find(attrs={"data-code": "fuel_type"})
                    .text.strip()
                )
                price_pln = car.find(
                    "span", class_="offer-price__number ds-price-number"
                ).span.text
                list_of_cars.append(
                    Car(
                        link=link,
                        full_name=full_name,
                        description=description,
                        year=year,
                        mileage_km=mileage_km,
                        engine_capacity=engine_capacity,
                        fuel_type=fuel_type,
                        price_pln=price_pln,
                    )
                )
            except Exception as e:
                print(f"Error msg: {e}")
        return list_of_cars


def write_to_csv(cars: List[Car]) -> None:
    with open("cars.csv", mode="w") as f:
        fieldnames = [
            "link",
            "full_name",
            "description",
            "year",
            "mileage_km",
            "engine_capacity",
            "fuel_type",
            "price_pln",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for car in cars:
            writer.writerow(asdict(car))


def scrape_otomoto() -> None:
    make = "bmw"
    scraper = OtomotoScraper(make)
    cars = scraper.scrape_pages(3)
    write_to_csv(cars)


if __name__ == "__main__":
    scrape_otomoto()
