import requests
from bs4 import BeautifulSoup
import re
import os
import time
from datetime import datetime


domain = input("\n==> Name of the site: ")
tempHref = input("==> Category to scrape links from: ")
hrefInCode = (f"/collections/{tempHref}/products")
mainLink = (f"https://{domain}/collections/{tempHref}")
tempRan1 = f"==> Starting page of {mainLink}: "
ran1 = int(input(tempRan1))
tempRan2 = f"==> Ending page of {mainLink}: "
ran2 = int(input(tempRan2))
ran2 += 1

dir1 = "Files"
dir3 = tempHref.capitalize()
directories = [dir1, dir3]

file = f"{dir1}/temp.txt"
fileT = tempHref.capitalize()
fileToParse = f"{dir1}/{fileT}"

Link1 = (f"{mainLink}/products/meilleur-infrared-electric-bbq-grill-adc-15c19b")
Link2 = (f"{mainLink}/products/meilleur-disinfection-lamp-black-uvhg2036415")
Link3 = (f"{mainLink}/products/meilleur-disinfection-fog-machine-ir-difm-20900415")
Link4 = (f"{mainLink}/products/nivea-deodorant-protect-care-women-150ml")
Link5 = (f"{mainLink}/products/nivea-men-fresh-ocean-spray-150ml")
Link6 = (f"{mainLink}/products/nivea-deodorant-natural-fairness-150-ml")
LinksToNotWrite = [Link1, Link2, Link3, Link4, Link5]


def directoryCreation():
    currentDirectory = os.getcwd()
    for directo in directories:
        newDir = os.path.join(currentDirectory, directo)
        if not os.path.exists(newDir):
            print("==> Directory creation in progress ...")
            time.sleep(1)
            os.mkdir(newDir)
        else:
            print("\n==> Starting URL scraping!\n")


def downloading():
    for i in range(ran1, ran2):
        url = (f"{mainLink}?page={i}")
        print(f"{i} ==> Scraping URLs from page {i} ...")
        r = requests.get(url)
        htmlConverted = r.content
        createdSoup = BeautifulSoup(htmlConverted, "html.parser")
        imageAnchor = createdSoup.find_all(
            "a", attrs={"href": re.compile(f"^{hrefInCode}")})
        for link in imageAnchor:
            full_link = (f"https://{domain}{link.get('href')}")
            with open(file, "a") as writing:
                writing.write(full_link)
                writing.write("\n")
        print(f"URLs scraped from {url}")


def setMaking(filename):
    print("==> Reading URLs for set creation ...")
    time.sleep(2)
    with open(filename, "r") as reading:
        lines = reading.readlines()
        set_lines = set(lines)

    print("==> Set created. Writing URLs ...")
    time.sleep(2)
    with open(filename, 'w') as now_writing:
        for line in set_lines:
            now_writing.write(line)
        print(f"Written!\n")


def notToWrite(fileremove):
    print("\nChecking if the URLs are unique ...")
    time.sleep(1)
    with open(fileremove, "r") as readingRemove:
        lines = readingRemove.read()

    print("Removing non required URLs ...")
    time.sleep(1)
    for LinkToRemove in LinksToNotWrite:
        lines = lines.replace(LinkToRemove, Link6)
        with open(fileremove, "w") as writingRemove:
            writingRemove.write(lines)


def cleaning(fileToWrite, fileToRead):
    with open(fileToRead, "w") as cleaning:
        cleaning.write("")
    with open(f"{fileToWrite}_link.txt", "w") as cleaning:
        cleaning.write("")
    with open(f"{fileToWrite}_name.txt", "w") as cleaning:
        cleaning.write("")


def subDownload(fileToWrite, fileToRead):
    with open(fileToRead, 'r') as f:
        i = 1
        for line in f:
            for word in line.split():
                r = requests.get(word)
                convertHTML = r.content
                soup = BeautifulSoup(convertHTML, 'html.parser')
                imageAnchor = soup.find_all(
                    "a", attrs={"href": re.compile("^//cdn.shopify")})
                nameAnchor = soup.find_all("body")
                for link, name in zip(imageAnchor, nameAnchor):
                    with open(f"{fileToWrite}_link.txt", "a") as writeIt:
                        full_link = (f"https:{link.get('href')}")
                        writeIt.write(full_link)
                        writeIt.write("\n")

                    with open(f"{fileToWrite}_name.txt", "a") as writeI:
                        full_name = name.get('id')
                        writeI.write(f"{str(i)} {full_name}")
                        writeI.write("\n")
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    print(f"{i} ==> Scraped main image URL at {current_time}")
                    i += 1
        print("URLs written in text")


def fileGenerator():
    with open(f"{fileToParse}_link.txt", "r") as readlinks:
        contentLink = readlinks.readlines()

    with open(f"{fileToParse}_name.txt", "r") as readnames:
        contentName = readnames.readlines()

    number = 0
    with open(f"urlFile.py", 'w') as file:
        file.write('')
        for link in contentLink:
            number += 1
            link = link.replace("\n", "")
            file.write(f'L{number} = "{link}"\n')
    print("\n==> URL file generated <==")

    number = 0
    with open(f"nameFile.py", 'w') as file:
        file.write('')
        for name in contentName:
            number += 1
            name = name.replace("\n", "")
            file.write(f'N{number} = "{name}"\n')
    print("==> Name file generated <==\n")
    time.sleep(2)


def varGenerator():
    with open(f"{fileToParse}_link.txt", "r") as readLines:
        Counting = 0
        contentCount = readLines.read()
        Count = contentCount.split("\n")
        for i in Count:
            Counting = Counting + 1
        number = 1
        with open(f"urlVars.py", "w") as file:
            file.write('')
            file.write("import urlFile as l\n")
            file.write("\nList1 = (\n")
            while number < Counting:
                file.write(f"l.L{number},\n")
                number += 1
            file.write(")")
        print("\n===> List of LINKS is created <===")

        number = 1
        with open(f"nameVars.py", "w") as file:
            file.write('')
            file.write("import nameFile as n\n")
            file.write("\nName1 = (\n")
            while number < Counting:
                file.write(f"n.N{number},\n")
                number += 1
            file.write(")")
        number -= 1
        print("===> List of NAMES is created <===\n")
        print(f"Link and Names written = {number}\n")


def download_url(url, names, numbering):
    print(f"Downloading {numbering}: {url}")
    file_name = names

    r = requests.get(url, stream=True)
    if r.status_code == requests.codes.ok:
        dirNow = os.getcwd()
        dir = os.path.join(dirNow, dir3)
        with open(f'{dir}/{file_name}.jpg', 'wb') as f:
            for data in r:
                f.write(data)


if __name__ == "__main__":
    try:
        try:
            directoryCreation()
        except:
            pass

        try:
            cleaning(fileToParse, file)
        except KeyboardInterrupt:
            print("\nClearing done!")

        try:
            downloading()
            notToWrite(file)
        except KeyboardInterrupt:
            print("\n Links gathered from pages!")

        try:
            setMaking(file)
        except KeyboardInterrupt:
            print("\n Unique Links Created!")

        try:
            subDownload(fileToParse, file)
        except KeyboardInterrupt:
            print("\n Sublink scraping done!")

        try:
            fileGenerator()
        except KeyboardInterrupt:
            print("\n Files generated as variables!")

        try:
            varGenerator()
        except KeyboardInterrupt:
            print("\n List generation done!")

        downloadNumber = int(input("Enter number of links/names written: "))
        downloadNumber += 1
        import urlVars as lV
        import nameVars as nV
        links = lV.List1
        names = nV.Name1

        try:
            for listLinks, listNames, writtenLinks in zip(links, names, range(1, downloadNumber)):
                download_url(listLinks, listNames, writtenLinks)
        except(KeyboardInterrupt):
            print("\n\n===> Script ended by USER! <===")

    except(KeyboardInterrupt):
        print("Thanks You For Using me!")
