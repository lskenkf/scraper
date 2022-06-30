import re
import requests
import string
from bs4 import BeautifulSoup

def keep_characters(value):
    allowed_characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ."
    allowed_characters = string.printable + 'öäüß'
    return ''.join(c for c in value if c in allowed_characters )


def keep_integers(value):
    allowed_characters = "0123456789"
    string = ''.join(c for c in value if c in allowed_characters )
    return int(string) if len(string)>0 else 0


def get_soup(url):
    r = requests.get(url, auth=('user', 'pass'))
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def refine_string(string):
    return re.sub('\n|\r|\xa0', '', string)