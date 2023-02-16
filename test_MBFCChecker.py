import tkinter as tk
import time
from tkinter import simpledialog

from MBFC_Utils import getCredibility
from NewsSiteCred import NewsSiteCredibility


def test_UI():
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


def test_Class():
    obj = NewsSiteCredibility(verbose = True)

    start_time = time.time()
    default_url = "https://www.foxnews.com/politics/pennsylvania-senate-fetterman-camp-sues-undated-absentee-ballots"
    obj.getSiteCredibility(default_url)
    print("--- %s seconds ---" % (time.time() - start_time))

    start_time = time.time()
    default_url = "https://www.cnn.com/2022/11/07/world/titanic-mystery-deep-sea-coral-reef-scn/index.html"
    obj.getSiteCredibility(default_url)
    print("--- %s seconds ---" % (time.time() - start_time))

    start_time = time.time()
    default_url = "https://www.foxnews.com/reef/pennsylvania-senate-fetterman"
    obj.getSiteCredibility(default_url)
    print("--- %s seconds ---" % (time.time() - start_time))

    start_time = time.time()
    default_url = "http://6nhmgdpnyoljh5uzr5kwlatx2u3diou4ldeommfxjz3wkhalzgjqxzqd.onion/"
    obj.getSiteCredibility(default_url)
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    test_Class()





