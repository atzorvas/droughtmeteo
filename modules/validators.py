def noaurl(url):
    '''needed for stations/add'''
    if (not url.startswith("http://penteli.meteo.gr/meteosearch/data/")) or (not url.endswith('.txt')):
        return False
    else:
        return True