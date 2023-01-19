import requests, json, subprocess

class GeoIP():
    _errCheck: bool
    _status: str
    _country: str
    _countryCode: str
    _region: str
    _regionName: str
    _city: str
    _zip: str
    _lat: str
    _lon: str
    _timezone: str
    _isp: str
    _org: str
    _as: str
    _query: str
    def __init__(self, ip: str) -> None:
        if len(ip) < 1: return

        geo_json = json.loads(requests.get(f"http://ip-api.com/json/{ip}").text)
        if geo_json['status'] == "fail": 
            self._errCheck = True
            return

        self._status = geo_json['status']
        self._country = geo_json['country']
        self._countryCode = geo_json['countryCode']
        self._region = geo_json['region']
        self._regionName = geo_json['regionName']
        self._city = geo_json['city']
        self._zip = geo_json['zip']
        self._lat = geo_json['lat']
        self._lon = geo_json['lon']
        self._timezone = geo_json['timezone']
        self._isp = geo_json['isp']
        self._org = geo_json['org']
        self._as = geo_json['as']
        self._query = geo_json['query']
        self._errCheck = False

"""
{
    '22/tcp': [['open', 'ssh']], 
    '25/tcp': [['filtered', 'smtp']], 
    '80/tcp': [['open', 'http']], 
    '135/tcp': [['filtered', 'msrpc']], 
    '139/tcp': [['filtered', 'netbios-ssn']], 
    '445/tcp': [['filtered', 'microsoft-ds']], 
    '465/tcp': [['filtered', 'smtps']], 
    '587/tcp': [['filtered', 'submission']], 
    '646/tcp': [['filtered', 'ldp']]}
"""
def pScan(ip: str) -> dict:
    if not validateIP(ip): return {}
    print("[ + ] Processing....")

    results = subprocess.getoutput(f"nmap {ip} -Pn")
    lines = results.split("\n")

    print("[ + ] Finished nmap, filtering response....")

    nmap = {}
    
    for line in lines:
        if not "Not" in line:
            if "open" in line: nmap[line.split(" ")[0]] = [line.split()[1:]]
            if "filtered" in line: nmap[line.split(" ")[0]] = [line.split()[1:]]
            if "close" in line: nmap[line.split(" ")[0]] = [line.split()[1:]]

    print("[ + ] Returning response....")
    return nmap

def validateIP(ip: str): 
    for i in ip.split("."): 
        if int(i) < 1 | int(i) > 255: return False
    return True
