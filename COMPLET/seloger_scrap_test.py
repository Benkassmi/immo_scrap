from bs4 import BeautifulSoup
import os
import requests
import re

url = 'http://www.seloger.com/list.htm?idtt=1&idtypebien=1,2&ci=750120,750114&tri=initial&naturebien=1&nb_pieces=2&pxmax=1250&surfacemin=40'
session = requests.Session()
session.max_redirects = 30
seloger_html = requests.get(url, stream=True)
lines = seloger_html.iter_lines()
content = ""
for line in lines:
    if re.compile('<script').match(line):
        print(line)
        print(next(lines))
    content = content + line

print(seloger_html.headers)
soup = BeautifulSoup(content,'html.parser')
path = os.getcwd() + '/COMPLET/scrap_seloger.txt'
f = open(path, 'w')
f.write(soup.prettify().encode('utf8'))