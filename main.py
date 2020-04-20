import os
import csv
import requests
from bs4 import BeautifulSoup

os.system("clear")
alba_url = "http://www.alba.co.kr"

def print_company(company):
  file = open(f"{company['name']}.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["place", "title", "time", "pay", "date"])
  
  for job in company["jobs"]:
    writer.writerow(list(job.values()))

def extract_company(company):
  print(company["url"] + "/?pagesize=500000")
  result = requests.get(company["url"] + "/?pagesize=500000")
  soup = BeautifulSoup(result.text, "html.parser")

  results = soup.find_all("tbody")[-1].find_all("tr")
  jobs = []
  for result in results:
    tds = result.find_all("td", recursive=False)
    if (len(tds) != 5):
      continue

    place, title, time, pay, date = tds
    place = place.text.strip().replace('\\xa0', ' ')
    title = title.find("span", {"class": "company"}).text.strip().replace(u'\xa0', u' ')
    time = time.text
    payinfo = pay.find_all("span")
    pay = payinfo[0].text + " " + payinfo[1].text
    date = date.text

    jobs.append({
      "place" : place,
      "title" : title,
      "time"  : time,
      "pay"   : pay,
      "date"  : date
    })

  company["jobs"] = jobs

def main():
  result = requests.get(alba_url)
  soup = BeautifulSoup(result.text, "html.parser")
  results = soup.find("div", {"id": "MainSuperBrand"}).find("ul", {"class": "goodsBox"}).find_all("li", {"class": "impact"})

  for result in results:
    company_url = result.find("a", {"class": "goodsBox-info"})['href']
    company_url = company_url if "job/brand" in company_url else f"{company_url}job/brand"
    company_name = result.find("span", {"class": "company"}).text
    company = {
      "url" : company_url,
      "name": company_name
    }
    extract_company(company)
    print_company(company)

main()