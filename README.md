# NewsSiteCredibilityChecker
News Site Credibility Checker using MBFC rating. 

Finds the credibility of a news site by crawling https://www.mediabiasfactcheck.com and using the metrics.

Module 1 : Performs a search query on https://www.mediabiasfactcheck.com/ and retirves the correct link.

Module 2 : Crawels the contents of the link and retirves the relevant metrics and classifies the site under consideration. 

Module 3 : Perform any futher processing or additional methods for classifing the site under consideration. 

## Key Metrics returned
Bias Rating
Factual Reporting
Press Freedom Rating
Traffic/Popularity
MBFC Credibility Rating

## Basic UI
Done using tikner

## Class usage
Basic usage is as follows,

```python
from NewsSiteCred import NewsSiteCredibility

cred_checker = NewsSiteCredibility()
default_url = "https://www.cnn.com/2022/11/07/world/titanic-mystery-deep-sea-coral-reef-scn/index.html" // <-- add your url here
score = cred_checker.getSiteCredibility(default_url)
```
Use **enable_UI** to enable display prompt or **verbose** to display internal results. Additionally, **cache** is also enabled by default for faster processing. Specifically, Least Recently Used (LRU) cache is used with 128 maxsize.

The mapping of returned score to readable text is as follows,

```python
RETURN_SCORES = {"DARK_WEB": 4,
                 "HIGH_CREDIBILITY": 3,
                 "MEDIUM_CREDIBILITY": 2,
                 "LOW_CREDIBILITY": 1,
                 "UNKNOWN": 0 }
```

Note: The website mediabiasfactcheck.com may contain noise and discrepancies. To account for this, we use additional methods:
* We use regex to remove inconsistencies in the metric scores since the scores (strings) on the MBFC webpage may not follow a consistent format. By parsing the MBFC webpage and filtering the scores using regex, we can make the scores consistent.
* Occasionally, the corresponding MBFC webpage for a news site may be inaccurate due to errors in the search query from MBFC's built-in search module. To address this, we compare the URL provided and the source URL listed in the mediabiasfactcheck webpage.
* If the score is UNKNOWN, it is likely that the search query failed. Specifically, sometimes MBFC search fails and points to misleading news source (like who.int). This is where, the source comparison fails. Thus, to take care of this we first retrive the webpage title from the original website by parsing it. Then use the title to search MBFC to get the correct MBFC webpage.
* MBFC may not have information on websites that are not traditional news sources, even if they contain valuable news articles (e.g. government websites). To mark these credible websites, we check the Top-Level Domain (TLD) section of the website address against a manually curated list of TLDs (e.g. "edu", "gov")   that are backed by credible educational, government, or international organizations.
