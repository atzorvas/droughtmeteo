from datetime import date
import requests

class station:
    """ VARIABLES
    _name = ''
    _city = ''
    _state = ''
    _lat = ''
    _long = ''
    _elev = ''
    _url = ''
    _emy_file = ''
    _from = ''
    _to = ''
    _data = {'RAIN': {'sum': sum, 'dates_counted': cnt1, 'dates_real': cnt2}}
    """
    INFO_WORDS = ['NAME', 'ELEV', 'LAT', 'LONG', 'CITY', 'STATE']


    def __init__(self, url, data_from):
        self._info = {}
        self._values = {}

        self._info['urlbase'] = url
        self._urlbase = url
        self.get_avail_periods(data_from)
        self.get_data()
        self._data = self._values

    def get_avail_periods(self, data_from):
        year = date.today().year
        errors = 0
        tmp = []

        while year >= int(data_from.split("-")[0]):
            end = 12 if year != date.today().year else date.today().month
            for month in range(end, 0, -1):
                url = self._urlbase + str(year) + "-" + str(month).zfill(2) + ".txt"
                r = requests.get(url)
                if r.status_code == 200:
                    tmp.append(str(year) + "-" + str(month).zfill(2))
                else:
                    errors += 1
            year -= 1
            if errors > 12:
                break
        periods = {'to': tmp[0]}
        self._info['to'] = periods['to']
        self._info['from'] = data_from


    def get_data(self):
        months = {"01": 'jan', "02": 'feb', "03": 'mar', "04": 'apr', "05": 'may', "06": 'jun', "07": 'jul',
                  "08": 'aug', "09": 'sep', "10": 'oct', "11": 'nov', "12": 'dec'}
        tmp_year = {}
        allyears = []
        temp_allyears = []
        cnt = -1
        for year in self.get_noaperiod():
            allyears.append(tmp_year.copy())
            temp_allyears.append(tmp_year.copy())
            cnt += 1
            allyears[cnt]['year'] = year
            temp_allyears[cnt]['year'] = year
            for month in self.get_noamonths(year):
                url = self._urlbase + str(year) + "-" + str(month).zfill(2) + ".txt"
                r = requests.get(url)
                data = r.text.encode('utf-8').split("\n")
                o = [i for i, x in enumerate(data) if "-------" in x]
                if len(o) == 2:
                    t_rain = data[o[1] + 1].split()[7]
                    t_temp = data[o[1] + 1].split()[0]
                    try:
                        float(t_rain)
                        allyears[cnt][months[str(month).zfill(2)]] = t_rain #rainvalue['sum']
                    except:
                        allyears[cnt][months[str(month).zfill(2)]] = ""
                    try:
                        float(t_temp)
                        temp_allyears[cnt][months[str(month).zfill(2)]] = t_temp #tempvalue
                    except:
                        temp_allyears[cnt][months[str(month).zfill(2)]] = ""
                else:
                    allyears[cnt][months[str(month).zfill(2)]] = ""
                    temp_allyears[cnt][months[str(month).zfill(2)]] = ""
        self._values['RAIN'] = allyears
        self._values['TEMP'] = temp_allyears

    def get_noaperiod(self):
        return range(int(self._info['from'].split("-")[0]), int(self._info['to'].split("-")[0]) + 1)

    def get_noamonths(self, year):
        if year == int(self._info['from'].split("-")[0]):
            return range(int(self._info['from'].split("-")[1]), 13)
        elif year == int(self._info['to'].split("-")[0]):
            return range(1, int(self._info['to'].split("-")[1]) + 1)
        else:
            return range(1, 13)


#myst = station('http://penteli.meteo.gr/meteosearch/data/samos/2011-05.txt', "2013-03")
#print vars(myst)['_info']
#print vars(myst)['_values']['RAIN']