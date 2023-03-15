import urllib

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import tkinter as tk
from tkinter import simpledialog
from functools import lru_cache
import time
import re

from CustomClassifier import runCustomCredilibityClassifier

MBFC_RATING = "MBFC Credibility Rating:"
FACTUAL_RATING = "Factual Reporting:"
SOURCE = "Source:"
UNDEFINED = -1
DARK_WEB = -2

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
TIMEOUT = 5

def compareURLs(url_a, url_b):
    if verbose == True:
        print("compareURLs ", url_a, " ", url_b)
    domain_a = re.split('//|\.', url_a)
    domain_b = re.split('//|\.', url_b)
    ##Note : Comparing urls using negative index. Thus, comparing from the back as
    ##the front of the url might have discrepancies (https://www. vs www. vs http://). However, the
    ##ending i.e the server is disambiguous (.org or .org/)
    #print("Domain : ", domain_a[-2], " : ",domain_b[-2])
    if domain_a[-2] != domain_b[-2]:
        return False
    return True


def resolveScore(result):
    if result in RETURN_SCORES.keys():
        return RETURN_SCORES[result]

def getRatings(mbfcUrl, source_ori):
    page = requests.get(mbfcUrl, timeout=TIMEOUT)
    soup = BeautifulSoup(page.content, "html5lib")
    dict_ratings = {}
    div_entries = soup.find_all('div', class_="entry-content")
    # p_entry = div_entry.p[0]
    for div_entry in div_entries:
        row = div_entry.text
        # if verbose == True:
        #     print(div_entry.text)
        if SOURCE in row:
            source = row.split(SOURCE)[1].split("\n")[0]
            if verbose == True:
                print("Source :", source)
            if compareURLs(source, source_ori) == False:
                return dict_ratings

        if MBFC_RATING in row:
            rating = row.split(MBFC_RATING)[1].split("\n")[0]
            rating = re.sub('[^0-9a-zA-Z]+', ' ', rating)
            if verbose == True:
                print("rating :", rating)
            dict_ratings[MBFC_RATING] = rating.strip()

        if FACTUAL_RATING in row:
            rating = row.split(FACTUAL_RATING)[1].split("\n")[0]
            rating = re.sub('[^0-9a-zA-Z]+', ' ', rating)
            if verbose == True:
                print("rating :", rating)
            dict_ratings[FACTUAL_RATING] = rating.strip()

        if len(dict_ratings) == 2:
            return dict_ratings

    return dict_ratings

def getRatings1(mbfcUrl):
    page = requests.get(mbfcUrl, timeout=TIMEOUT)
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
    #print("getMBFCUrl : ",query_URL)
    page = requests.get(query_URL, timeout=TIMEOUT)
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


def getSiteLabel(mbfcUrl, domain):
    dict_ratings = getRatings(mbfcUrl, domain)
    if verbose == True:
        print("Dict Ratings : ", dict_ratings)
    site_label = isCredible(dict_ratings)
    if verbose == True:
        print("Rating : ", site_label)
    return site_label

@lru_cache(maxsize=128, typed=False)
def execute(domain):
    mbfcUrl = getMBFCUrl(domain)
    if verbose == True:
        print("MBFC URL : ", mbfcUrl)
    return getSiteLabel(mbfcUrl, domain)

def returnResult(site_label, displayPrompt = False):
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
    elif site_label == DARK_WEB:
        if displayPrompt == True:
            tk.messagebox.showinfo("Result \t\t\t", "DARK_WEB!!! Source")
        return "DARK_WEB"

def reExecuteUsingTitle(domain):
    domain = "https://" + domain
    if verbose:
        print("Re-executing for : ", domain)
    # making requests instance
    try:
        reqs = requests.get(domain, timeout=TIMEOUT)
        if verbose:
            print("Get Request Response : ", reqs)
        # using the BeautifulSoup module
        soup = BeautifulSoup(reqs.text, 'html.parser')
        # displaying the title
        for title in soup.find_all('title'):
            title_text = title.get_text()
            res = re.split('\(|\||\.|\:|\-', title_text)[0]
            res = res.strip() #Contains the stripped title
            res = res.replace(" ", "+")
            if verbose:
                print("Title of the website is : ", res)
            #Get the mbfc webpage by searching the title
            mbfc_url = getMBFCUrl(res)
            if verbose:
                print("mbfc_url : ", mbfc_url)
            return getSiteLabel(mbfc_url, domain)
    except Exception as e:
        if verbose == True:
            print("Exception caught during re-execution : ", e)
        raise e

def getCredibility(base_url, displayPrompt = False):
    site_label = UNDEFINED
    try:
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
            site_label = DARK_WEB

        if site_label == UNDEFINED:
            site_label = execute(domain)
        ##Sometimes MBFC search fails and points to misleading news source (like who.int).
        ##This is where, the source comparison fails. Thus, as a fail safe we first retrive the webpage title
        ##from the original domain then use the title to search MBFC to get the correct MBFC webpage.
        if site_label == UNDEFINED:
            site_label = reExecuteUsingTitle(domain)
    except Exception as e:
        if verbose == True:
            print("Exception caught : ", e)

    finally:
        ##Now if it is still UNDEFINED then MBFC does not contain the information.
        ##Thus, falling back to propabilistic logic.
        ##NOTE: For now we just use a list of domains
        if site_label == UNDEFINED:
            if verbose == True:
                print("Running custom classifier")
            site_label = runCustomCredilibityClassifier(domain, verbose)
        return returnResult(site_label, displayPrompt)


