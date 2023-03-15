#https://en.wikipedia.org/wiki/List_of_Internet_top-level_domains
CREDIBLE_SERVER_LIST = ['int', 'edu', 'gov', 'mil']


def runCustomCredilibityClassifier(domain, verbose = False):
    serversList = domain.split('.')
    server = serversList[-1]
    sub_server = domain.split('.')[-2]
    for i in range(0, len(serversList)):
        server = serversList[-(1 + i)]
        if server in CREDIBLE_SERVER_LIST:
            if verbose == True:
                print("Server in CREDIBLE_SERVER_LIST : ", server)
            return 2 #"HIGH_CREDIBILITY"
    else:
        return -1 #"UNKNOWN"
