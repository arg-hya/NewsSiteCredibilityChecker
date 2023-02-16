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

RETURN_SCORES = {"DARK_WEB": 4,
                          "HIGH_CREDIBILITY": 3,
                          "MEDIUM_CREDIBILITY": 2,
                          "LOW_CREDIBILITY": 1,
                          "UNKNOWN": 0 }

verbose = False

def resolveScore(result):
    if result in RETURN_SCORES.keys():
        return RETURN_SCORES[result]

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
            #print(span.text)
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

    if verbose == True:
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
    if verbose == True:
        print("MBFC URL : ", mbfcUrl)
    dict_ratings = getRatings(mbfcUrl)
    if verbose == True:
        print("Dict Ratings : ", dict_ratings)
    site_label = isCredible(dict_ratings)
    if verbose == True:
        print("Rating : ", site_label)
    return site_label

def getCredibility(base_url, displayPrompt = False):
    if verbose == True:
        print("Base URL : ", base_url)

    domain = urlparse(base_url).netloc
    if verbose == True:
        print("Domain : ",domain)
    server = domain.split('.')[-1]
    if verbose == True:
        print("Server : ", server)
    if server == "onion":
        if displayPrompt == True :
            tk.messagebox.showinfo("Result \t\t\t", "Dark Net Site")
        return "DARK_WEB"

    site_label = execute(domain)

    if site_label == UNDEFINED:
        if displayPrompt == True:
            tk.messagebox.showinfo("Result \t\t\t", "Unable to classify source")
        return "UNKNOWN"
    elif site_label == 0:
        if displayPrompt == True:
            tk.messagebox.showinfo("Result \t\t\t", "LOW CREDIBILITY!!! Source")
        return "LOW_CREDIBILITY"
    elif site_label == 1:
        if displayPrompt == True:
            tk.messagebox.showinfo("Result \t\t\t", "MEDIUM CREDIBILITY!!! Source")
        return "MEDIUM_CREDIBILITY"
    elif site_label == 2:
        if displayPrompt == True:
            tk.messagebox.showinfo("Result \t\t\t", "HIGH CREDIBILITY!!! Source")
        return "HIGH_CREDIBILITY"
