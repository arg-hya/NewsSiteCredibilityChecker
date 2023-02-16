from MBFC_Utils import getCredibility, resolveScore


class NewsSiteCredibility:
    # The init method or constructor
    def __init__(self, enable_UI = False, verbose = False):
        # Instance Variable
        self._enableUI = enable_UI
        self._verbose = verbose

    def getSiteCredibility(self, base_url):
        self._result = getCredibility(base_url, displayPrompt = self._enableUI)
        self._score = resolveScore(self._result)
        if self._verbose == True :
            print("The result is : ",self._result, " score : ", self._score)
        return self._score

