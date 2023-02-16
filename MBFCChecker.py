import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import tkinter as tk
from tkinter import simpledialog
from functools import lru_cache
import time

MBFC_RATING = "MBFC Credibility Rating:"
FACTUAL_RATING = "Factual Reporting:"
UNDEFINED = -1

MBFC_RATING_VALUES = {"HIGH CREDIBILITY" : 2,
                      "MEDIUM CREDIBILITY" : 1,
                      "LOW CREDIBILITY" : 0}

FACTUAL_RATING_VALUES = {"VERY HIGH": 4,
                          "HIGH": 3,
                          "MOSTLY FACTUAL": 2,
                          "MIXED": 1,
                          "LOW": 0 }

def getRatings(mbfcUrl):
    page = requests.get(mbfcUrl)
    soup = BeautifulSoup(page.content, "html5lib")
    dict_ratings = {}
    div_entries = soup.find_all('div', class_="entry-content")
    # p_entry = div_entry.p[0]
    for div_entry in div_entries:
        row = div_entry.text
        #print(div_entry.text)
        if MBFC_RATING in row:
            rating = row.split(MBFC_RATING)[1].split("\n")[0]
            dict_ratings[MBFC_RATING] = rating.strip()
            # print(rating.strip())
        if FACTUAL_RATING in row:
            rating = row.split(FACTUAL_RATING)[1].split("\n")[0]
            dict_ratings[FACTUAL_RATING] = rating.strip()
            # print(rating.strip())
            # print(len(dict_ratings))
        if len(dict_ratings) == 2:
            return dict_ratings

    return dict_ratings

def getRatings1(mbfcUrl):
    page = requests.get(mbfcUrl)
    soup = BeautifulSoup(page.content, "html5lib")
    dict_ratings = {}
    div_entries = soup.find_all('div', class_="entry-content")
    # p_entry = div_entry.p[0]
    for div_entry in div_entries:
        p_entries = div_entry.find_all('p')
        for p_entry in p_entries:
            span_enties = p_entry.find_all('span')
            for span_entry in span_enties:
                row = span_entry.text
                # print(span_entry.text)
                if MBFC_RATING in row:
                    # print(row)
                    # print("Splitting data...")
                    rating = row.split(MBFC_RATING)[1].split("\n")[0]
                    dict_ratings[MBFC_RATING] = rating.strip()
                    # print(rating.strip())
                if FACTUAL_RATING in row:
                    # print(row)
                    # print("Splitting data...")
                    rating = row.split(FACTUAL_RATING)[1].split("\n")[0]
                    dict_ratings[FACTUAL_RATING] = rating.strip()
                    # print(rating.strip())
                if len(dict_ratings) == 2 :
                    return dict_ratings
    return dict_ratings

def getMBFCUrl(domain):
    query_URL = "https://mediabiasfactcheck.com/?s=" + domain
    page = requests.get(query_URL)
    soup = BeautifulSoup(page.content, "html5lib")

    a_entries = soup.find_all('a', class_="button", href=True)
    for a_entry in a_entries:
        span = a_entry.find("span")
        if 'Read More' in span.text:
            print(span.text)
            href = a_entry.find("href")
            #print(a_entry['href'])
            return a_entry['href']

def isCredible(dict_ratings):
    mbfc_point = UNDEFINED
    factual_point = UNDEFINED
    if MBFC_RATING in dict_ratings:
        mbfc_point = MBFC_RATING_VALUES[dict_ratings[MBFC_RATING].upper()]
    if FACTUAL_RATING in dict_ratings:
        factual_point = FACTUAL_RATING_VALUES[dict_ratings[FACTUAL_RATING].upper()]
    print("MBFC_RATING points : ", mbfc_point)
    print("FACTUAL_RATING points : ", factual_point)
    if mbfc_point != UNDEFINED: #> MBFC_RATING_VALUES["LOW CREDIBILITY"]:
        return mbfc_point
    if factual_point != UNDEFINED: #> FACTUAL_RATING_VALUES["MIXED"]:
        if factual_point == FACTUAL_RATING_VALUES["LOW"] or \
            factual_point == FACTUAL_RATING_VALUES["MIXED"] :
            return 0
        if factual_point == FACTUAL_RATING_VALUES["MOSTLY FACTUAL"] :
            return 1
        if factual_point == FACTUAL_RATING_VALUES["HIGH"] or \
            factual_point == FACTUAL_RATING_VALUES["VERY HIGH"] :
            return 2
    return UNDEFINED

@lru_cache(maxsize=128, typed=False)
def execute(domain):
    mbfcUrl = getMBFCUrl(domain)
    print("MBFC URL : ", mbfcUrl)
    dict_ratings = getRatings(mbfcUrl)
    print("Dict Ratings : ", dict_ratings)
    site_label = isCredible(dict_ratings)
    print("Rating : ", site_label)
    return site_label

def getCredibility(base_url, displayPrompt = False):
    print("Base URL : ", base_url)
    #base_url = "https://www.foxnews.com/politics/pennsylvania-senate-fetterman-camp-sues-undated-absentee-ballots"
    #base_url = "https://www.cnn.com/2022/11/07/world/titanic-mystery-deep-sea-coral-reef-scn/index.html"
    domain = urlparse(base_url).netloc
    print("Domain : ",domain)
    server = domain.split('.')[-1]
    print("Server : ", server)
    if server == "onion":
        tk.messagebox.showinfo("Result \t\t\t", "Dark Net Site")
        return "DARK_WEB"
    # mbfcUrl = getMBFCUrl(domain)
    # print("MBFC URL : ", mbfcUrl)
    # dict_ratings = getRatings(mbfcUrl)
    # print("Dict Ratings : ", dict_ratings)
    # site_label = isCredible(dict_ratings)
    # print("Rating : ", site_label)

    site_label = execute(domain)

    if site_label == UNDEFINED:
        tk.messagebox.showinfo("Result \t\t\t", "Unable to classify source")
        return "UNKNOWN"
    elif site_label == 0:
        tk.messagebox.showinfo("Result \t\t\t", "LOW CREDIBILITY!!! Source")
        return "LOW_CREDIBILITY"
    elif site_label == 1:
        tk.messagebox.showinfo("Result \t\t\t", "MEDIUM CREDIBILITY!!! Source")
        return "MEDIUM_CREDIBILITY"
    elif site_label == 2:
        tk.messagebox.showinfo("Result \t\t\t", "HIGH CREDIBILITY!!! Source")
        return "HIGH_CREDIBILITY"

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    #default_url = "https://www.foxnews.com/politics/pennsylvania-senate-fetterman-camp-sues-undated-absentee-ballots"
    default_url = "https://www.foxnews.com/politics/pennsylvania-senate-fetterman-camp-sues-undated-absentee-ballots"
    #http://6nhmgdpnyoljh5uzr5kwlatx2u3diou4ldeommfxjz3wkhalzgjqxzqd.onion/

    while(True) :
        start_time = time.time()
        base_url = simpledialog.askstring("News site checker", "Enter News Article here \t\t\t\t\t\t", initialvalue=default_url)
        getCredibility(base_url, displayPrompt = True)
        print("--- %s seconds ---" % (time.time() - start_time))





