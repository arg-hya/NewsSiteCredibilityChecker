# NewsSiteCredibilityChecker
News Site Credibility Checker using MBFC rating

Finds the credibility of a news site by crawling https://www.mediabiasfactcheck.com and using the metrics.

Module 1 : Performs a search query on https://www.mediabiasfactcheck.com/ and retirves the correct link.
Module 2 : Crawels the contents of the link and retirves the relevant metrics and classifies the site under consideration.

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
default_url = "Site url to check" //add your url here
cred_checker.getSiteCredibility(default_url)
```

Use **enable_UI** to enable display prompt. Additionally, **cache** is also enabled by default for faster processing. Specifically, Least Recently Used (LRU) cache is used with 128 maxsize.


