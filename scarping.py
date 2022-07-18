from selenium import webdriver
from bs4 import BeautifulSoup
import time 
import csv
import requests
import pandas as pd

start_url = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"
browser = webdriver.Chrome("C:\Users\91884\Desktop\WebScraping\Unconfirmed 954513.crdownload")
browser.get(start_url)
time.sleep(10)

planet_data = []
headers = ["name", "constelattion", "right ascension", "declination", 
"app mag", "distance", "spectral type", "brown dwarf",
 "mass", "radius", "orbital period", "semimajor", "ecc"]

def scrape():

    for i in range(0,428):
        soup = BeautifulSoup(browser.page_source, "html.parser")

        for ul_tag in soup.find_all("ul", atts={"class", "expo-planet"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []

            for index, li_tags in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tags.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tags.contents[0])
                    except:
                        temp_list.append("")
            planet_data.append(temp_list)

        browser.find_elements_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        print(f"Page {i} scarping complete")

scrape()

new_planet_data = []

def scrape_more_data(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content, "html.parser")
        temp_list = []

        for tr_tag in soup.find_all("tr", attrs={"class":"fact_row"}):
            td_tags = tr_tag.find_all("td")

            for td_tag in td_tags:
                try:
                    temp_list.append(td.tag.find_all("div", attrs={"class":"value"})[0].contents[0])
                except:
                    temp_list.append("")
        new_planet_data.append(temp_list)
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)

for index, data in enumerate(planet_data):
    scrape_more_data(data[5])
    print(f"scraping at hyperlink {index+1} is complete")

print(new_planet_data[0:10])

final_planet_data = []

for index, data in enumerate(planet_data):
    new_planet_data_elements = new_planet_data[index]
    new_planet_data_elements = [elem.replace("\n", "") for elem in new_planet_data_elements]
    new_planet_data_elements = new_planet_data_elements[:7]
    final_planet_data.append(data + new_planet_data_elements)

with open("final.csv", "w") as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(final_planet_data)