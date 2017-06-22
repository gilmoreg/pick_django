''' Controller for MAL operations '''
from xml.etree import cElementTree as ET
from bs4 import BeautifulSoup
from ..models import Poll, Anime
import sys
import requests
from datetime import date, datetime

def check_mal_credentials(auth):
    ''' Using auth string, validate credentials '''
    try:
        response = requests.get('https://myanimelist.net/api/account/verify_credentials.xml', headers={'Authorization': 'Basic ' + auth}).text
        if response == 'Invalid credentials' or response == 'Unable to connect to MAL':
            print('Invalid credentials')
            return False
        # 0=id, 1=username
        return ET.fromstring(response)[1].text
    except:
        print('Something went wrong')
        raise
        return False

def save_poll_options(poll, username):
    ''' Gets a Myanimelist plan to watch list given a HTTP basic auth string '''
    # A lot of this code comes from https://searchcode.com/codesearch/view/76919603/
    try:
        raw_mal_list = requests.get('https://myanimelist.net/malappinfo.php?status=all&type=anime&u={username}').text
        # Malappinfo has some bad xml, this helps clean it up
        uni_list = unicode(raw_mal_list.content, 'utf-8', 'replace')
        xmldata = BeautifulSoup(uni_list)
        # Status 6 = plan to watch
        filtered_list = xmldata.myanimelist.findAll('anime', 'my_status'==6, recursive = True)
        for node in filtered_list:
            # Filter out if hasn't aired yet
            (year, month, day) = node.find('series_start').text.split('-')
            start = datetime(int(year), int(month), int(day))
            if start > datetime.now():
                continue
            # Set up the dictionary
            anime_id = node.find('series_animedb_id').text
            anime_title = node.find('series_title').text
            anime_image = node.find('series_image').text
            a = Anime(id=anime_id, title=anime_title, image=anime_image, poll=poll)
            if not a:
                print('Error creating anime {anime_title}')
    except:
        return []
