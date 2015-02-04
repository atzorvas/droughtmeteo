from datetime import date
import requests
import calendar

class station:
    """ VARIABLES
    name, city, state, elev, long, lat
    url, urlbase, data-from, data-to
    data
    """
    INFO_WORDS = ['NAME', 'ELEV', 'LAT', 'LONG', 'CITY', 'STATE']


    def __init__(self, url):
        self._info = {}
        self._info['url'] = url
        self._info['urlbase'] = url[:-11]

        self.run() #get station info
        self.get_avail_periods() #get available periods
        self.get_data() #get MEAN TEMP & RAIN data

    def run(self):
        ''' Find the INFO_WORDS, parse next word if it's a "value"
        '''
        data = requests.get(self._info['url']).text.encode('utf-8').split('\n')

        for line in data:
            for word in self.INFO_WORDS:
                if word in line:
                    for item in line.split(" "):
                        if item.startswith(word):
                            next = line.split().index(item) + 1
                            value = ''
                            while (True):
                                if len(line.split()) >= next + 1:
                                    if not line.split()[next].endswith(":"):
                                        value += line.split()[next] + " "
                                        next += 1
                                    else:
                                        break;
                                    if len(line.split()) - 1 < next:
                                        break;
                                else:
                                    break;
                            self._info[word] = value[:-1]

    def get_avail_periods(self):
        year = date.today().year
        errors = 0
        tmp = []

        while errors < 12:
            end = 12 if year != date.today().year else date.today().month
            for month in range(end, 0, -1):
                url = self._info['urlbase'] + str(year) + "-" + str(month).zfill(2) + ".txt"
                r = requests.get(url)
                if r.status_code == 200:
                    tmp.append(str(year) + "-" + str(month).zfill(2))
                else:
                    errors += 1
            year -= 1
        self._info['to'] = tmp[0] #periods['to']
        self._info['from'] = tmp[-1] #periods['from']


    def get_data(self):
        tmp_year = {}
        self._data = {}
        self._data['TEMP'] = []
        self._data['RAIN'] = []
        for pos, year in enumerate(self.get_noaperiod()):
            self._data['RAIN'].append(tmp_year.copy())
            self._data['TEMP'].append(tmp_year.copy())
            self._data['RAIN'][pos]['year'] = year
            self._data['TEMP'][pos]['year'] = year
            for month in self.get_noamonths(year):
                data = self.get(year, month)
                o = [i for i, x in enumerate(data) if "-------" in x]
                if len(o) == 2: #if no rain/temp data, None will be returned with rain.get(month)
                    t_rain = data[o[1] + 1].split()[7]
                    t_temp = data[o[1] + 1].split()[0]
                    self._data['RAIN'][pos][calendar.month_name[month].lower()[0:3]] = self.get_value(t_rain)
                    self._data['TEMP'][pos][calendar.month_name[month].lower()[0:3]] = self.get_value(t_temp)


    def get_noaperiod(self):
        return range(int(self._info['from'].split("-")[0]), int(self._info['to'].split("-")[0]) + 1)


    def get_noamonths(self, year):
        if year == int(self._info['from'].split("-")[0]):
            return range(int(self._info['from'].split("-")[1]), 13)
        elif year == int(self._info['to'].split("-")[0]):
            return range(1, int(self._info['to'].split("-")[1]) + 1)
        else:
            return range(1, 13)


    def get(self, year, month):
        url = self._info['urlbase'] + str(year) + "-" + str(month).zfill(2) + ".txt"
        r = requests.get(url)
        return r.text.encode('utf-8').split("\n")


    def get_value(self, data):
        try:
            float(data) #test if it's a float
            return data
        except:
            return ""


def test(data):
    if data == {'TEMP': [{'aug': '26.2', 'sep': '24.8', 'may': '18.7', 'jun': '23.8', 'jul': '27.0', 'year': 2011, 'nov': '13.0', 'dec': '13.4', 'oct': '17.6'}, {'mar': '12.9', 'feb': '10.1', 'aug': '28.5', 'sep': '24.5', 'apr': '16.9', 'jun': '25.5', 'jul': '29.0', 'jan': '9.0', 'may': '20.6', 'year': 2012, 'nov': '17.5', 'dec': '12.8', 'oct': '22.3'}, {'mar': '14.4', 'feb': '13.0', 'aug': '26.9', 'apr': '17.4', 'jun': '24.6', 'jul': '26.7', 'jan': '12.1', 'may': '21.7', 'year': 2013}], 'RAIN': [{'aug': '0.2', 'sep': '12.6', 'may': '8.0', 'jun': '59.2', 'jul': '0.0', 'year': 2011, 'nov': '4.4', 'dec': '57.8', 'oct': '41.4'}, {'mar': '52.4', 'feb': '144.6', 'aug': '0.0', 'sep': '0.0', 'apr': '78.0', 'jun': '0.0', 'jul': '0.0', 'jan': '112.0', 'may': '10.6', 'year': 2012, 'nov': '66.2', 'dec': '236.4', 'oct': '18.4'}, {'mar': '34.2', 'feb': '104.8', 'aug': '0.0', 'apr': '25.2', 'jun': '6.0', 'jul': '0.0', 'jan': '118.4', 'may': '48.6', 'year': 2013}]}:
        print "Test... OK"
    else:
        print "Test... FAILED"