''' Controller for MAL operations '''
import sys
import requests
import xml.etree.ElementTree as ET
from ..models import Poll

def check_mal_credentials(auth):
    ''' Using auth string, validate credentials '''
    try:
        response = requests.get('https://myanimelist.net/api/account/verify_credentials.xml', params={'Authorization': 'Basic {auth}'}).text
        if response == 'Invalid credentials' or response == 'Unable to connect to MAL':
            return False
        xml = ET.fromstring(response).text
        # 0=id, 1=username
        return xml[1].text
    except:
        return False

#def parse_xml(xml):
#    ''' Parse the MAL response '''
#    root = ET.fromstring(xml).text
#    if len(root) == 2:
        # what we get is a dictionary
        # root[i].text to get value, root[i].tag to get key

def get_mal_list(username):
    ''' Fetch the user's list and return the filtered plan to watch list '''
    try:
        list = requests.get('https://myanimelist.net/malappinfo.php?status=all&type=anime&u={username}')
        return ET.fromstring(list).text
    except:
        return {}

def get_list(auth):
    ''' Gets a Myanimelist plan to watch list given a HTTP basic auth string '''
    # Check credentials
    username = check_mal_credentials(auth)
    if username:
        # Get list
        list = get_mal_list(username)
        if list:
            # create poll in db
            # Poll.create
            return True
    return False
    # 
    # here the views render the template, just need to return the data

# r = requests.get('https://myanimelist.net/api/account/verify_credentials.xml', headers={'Authorization': 'Basic c29sZXZ1bDozM01hbDdnMw=='})