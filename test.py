from bs4 import BeautifulSoup
import requests
import time
import os
import csv
import inspect
import datetime

class House:
    def __init__(self, cost, bed, bath, address, city, size):
        self.Cost = cost
        self.Bed = bed
        self.Bath = bath
        self.Address = address
        self.City = city
        self.Size = size
    Cost = ""
    Bed = ""
    Bath = ""
    Street = ""
    City = ""
    Size = ""




page = 8
Houses = []
URL = "https://www.trulia.com/CA/Gardena/" + str(page) + "_p/"

r = requests.get(URL)
soup = BeautifulSoup(r.content, "html.parser")
allHouses = soup.find_all("div", {"class": "smlCol12 lrgCol8 ptm cardContainer"})  # class info




# lastpage = soup.find_all("a", {"class": "backgroundBasic mrs bas pvs phm"}, text="Last")

# print(lastpage[0]['href'])
# print(URL[6:])

print('Working on ' + URL)
for house in allHouses:
    try:
        city = house.find_all("div", {"class": "typeTruncate typeLowlight cardFooter man ptn phm pbm"})[0].text
    except:
        city = ""
    for item in house.find_all("div", {"class": "cardDetails man ptm phm"}):
        for x in item.find_all("ul"):
            try:
                if "sqft" in str(x.contents[2].text):
                    size = x.contents[2].text
                else:
                    size = ""
            except IndexError:
                size = ""
            try:
                if "bd" in str(x.contents[0].text):
                    bed = x.contents[0].text
                else:
                    bed = ""
            except IndexError:
                bed = ""
            try:
                if "ba" in str(x.contents[1].text):
                    bath = x.contents[1].text
                else:
                    bath = ""
            except IndexError:
                bath = ""
        try:
            price = item.find_all("span", {"class": "cardPrice h4 man pan typeEmphasize noWrap typeTruncate "})[0].text
        except IndexError:
            price = ""
        try:
            address = item.find_all("p", {"class": "typeTruncate typeLowlight"})[0].text
        except IndexError:
            address = ""
    house = House(price, bed, bath, address, city, size)
    Houses.append(house)

for house in Houses:
    print(
        "Price:" + house.Cost + "|" + "Bed:" + house.Bed + "|" + "Bath:" + house.Bath + "|" + "Address:" + house.Street + "|" + "City:" + house.City + "|" + "Size:" + house.Size + "|")
