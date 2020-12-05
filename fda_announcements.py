import requests
from bs4 import BeautifulSoup
import schedule
import time

def get_fdaacademy_announcements(nresults: int = 5):
    URL = "https://www.fda.gov.ph/category/academy-announcements/"

    response = requests.get(URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

    for announcement in soup.find_all(name="article", attrs={'class':"category-academy-announcements"})[:5]:
        print("\n".join(announcement.find(name="h2", attrs={'class':"entry-title"}).stripped_strings))
        link = announcement.find(name="a", href=True).attrs.get("href")
        if link is not None:
            print(f'link: {link}', end='')
        print("\t".join(announcement.find(name="div", attrs={'class':"entry-content"}).strings))

def run_schedule(t: str = '10:00', daily=True, job=get_fdaacademy_announcements):
    schedule.every().day.at(t).do(job,'Getting FDA Academy announcements')
    while True:
        schedule.run_pending()
        time.sleep(60) # wait one minute

if __name__ == "__main__":
    get_fdaacademy_announcements()
    run_schedule()

