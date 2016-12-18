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

filename = inspect.getframeinfo(inspect.currentframe()).filename
path = os.path.dirname(os.path.abspath(filename)) + '/'

Houses = []
page = 1
CityName = "Garden_Grove"
keepGoing = True
lastpageCheck = ""

while(keepGoing):
    try:
        URL = "https://www.trulia.com/CA/"+str(CityName)+"/" + str(page) + "_p/"

        r = requests.get(URL)
        soup = BeautifulSoup(r.content, "html.parser")
        allHouses = soup.find_all("div", {"class": "smlCol12 lrgCol8 ptm cardContainer"})  # class info

        try:
            lastpageCheck = soup.find_all("a", {"class": "backgroundBasic mrs bas pvs phm"}, text="Last")[0]['href']
        except IndexError:
            pass

        if lastpageCheck == URL[6:]:
            keepGoing = False

        print(lastpageCheck)
        print(URL[6:])

        print('Working on ' + URL)
        for house in allHouses:
            try:
                city = '"' + house.find_all("div", {"class": "typeTruncate typeLowlight cardFooter man ptn phm pbm"})[0].text +'"'
            except IndexError:
                city = '""'
            for item in house.find_all("div", {"class": "cardDetails man ptm phm"}):
                for x in item.find_all("ul"):
                    try:
                        if "sqft" in str(x.contents[2].text):
                            size = '"' + x.contents[2].text + '"'
                        else:
                            size = '""'
                    except IndexError:
                        size = '""'
                    try:
                        if "bd" in str(x.contents[0].text):
                            bed = '"' + x.contents[0].text + '"'
                        else:
                            bed = '""'
                    except IndexError:
                        bed = '""'
                    try:
                        if "ba" in str(x.contents[1].text):
                            bath = '"' + x.contents[1].text + '"'
                        else:
                            bath = '""'
                    except IndexError:
                        bath = '""'
                try:
                    price = '"' + item.find_all("span", {"class": "cardPrice h4 man pan typeEmphasize noWrap typeTruncate "})[0].text + '"'
                except IndexError:
                    price = '""'
                try:
                    address = '"' + item.find_all("p", {"class": "typeTruncate typeLowlight"})[0].text + '"'
                except IndexError:
                    address = '""'
            house = House(price, bed, bath, address, city, size)
            Houses.append(house)

        # for house in Houses:
        #     print("Price:" + house.Cost + "|" + "Bed:" + house.Bed + "|" + "Bath:" + house.Bath + "|" + "Address:" + house.Street + "|" + "City:" + house.City + "|" + "Size:" + house.Size + "|")

        page += 1
        time.sleep(3)

    except IndexError:
            break

print('Writing to csv')
with open(path + "Trulia_"+str(CityName)+".csv", mode="w") as writer:
    writer.write('Source,Cost,Bed,Bath,Address,City,Size\n')
    for house in Houses:
        writer.write('Trulia,' + house.Cost + ',' + house.Bed + ',' + house.Bath + ',' + house.Address + ',' + house.City + ',' + house.Size + '\n')

#
# for house in Houses:
#     print("Price:" + house.Cost + "|" + "Bed:" + house.Bed + "|" + "Bath:" + house.Bath + "|" + "Address:" + house.Street + "|" + "City:" + house.City + "|" + "Size:" + house.Size + "|")
#

