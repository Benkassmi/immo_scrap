from bs4 import BeautifulSoup
import urllib
import re
import math
import os
import json
import requests
import time

def parse_page(url, annonces):
    #OUVERTURE DE LA PAGE
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
    session = requests.Session()
    session.max_redirects = 20
    seloger_html = requests.get(url, headers=headers)
    time.sleep(1)
    soup = BeautifulSoup(seloger_html.text,'html.parser')
    
    #Parse les informations sur les appartements sous format JSON
    scripts = soup.find_all(lambda tag: tag.name == 'script' and len(tag.attrs) == 0 )
    for script in scripts:
        data_match = re.match(r'var ava_data = (.*);', script.string.strip().encode('utf8'), re.DOTALL)
        try:
            if data_match:
                data = re.sub(r'\s','', data_match.group(1))
                data = re.sub('logged', '\"logged\"',data)
                data = re.sub('products', '\"products\"',data)
                json_data = json.loads(data)
        except AttributeError:
            pass
    
    
    #PARSING DE LA PAGE
    for i in range(len(json_data["products"])):
        try:
            infos = []
            id_annonce = json_data["products"][i][u'idannonce'].encode('utf8')
            
            infos.append(id_annonce)		#REFERENCE DES ANNONCES
            infos.append(json_data["products"][i][u'prix'].encode('utf8'))	#PRIX DES ANNONCES
            infos.append(json_data["products"][i][u'surface'].encode('utf8'))		#SURFACE DES ANNONCES
            
            #LIEN DE L'ANNONCE
            article = soup.find('article', id=re.compile('^annonce-'+id_annonce))
            url_detail = article.find(lambda tag: tag.name == 'a' and tag.has_attr('href'))['href'].encode('utf8')
            infos.append(url_detail)
            
            #METRO ET MEUBLE
            infos = parse_page_detail(url_detail, infos)
            
            #CONTACT
            contact = article.find(lambda tag: tag.name == 'a' and tag.has_attr('data-phone'))['data-phone'].encode('utf8')
            infos.append(contact)
            
            annonces.append(infos)
        except KeyError:
            pass
    return annonces
    
def parse_page_detail(url, infos):
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
    session = requests.Session()
    session.max_redirects = 20
    seloger_html = requests.get(url, headers=headers)
    time.sleep(1)
    soup = BeautifulSoup(seloger_html.text,'html.parser')
    try:
        desc = soup.find(attrs={'name':'description'}).get('content')
        #Appartement vide ou pas ?
        if re.search(r'\s(m|M)eubl',desc):
            infos.append("Meuble")
        elif re.search(r'\s(v|V)ide',desc):
            infos.append("Vide")
        else:
            infos.append("Surement vide")
        
        #Metro proche 
        try:
            metro = re.search(r'(?<=m.tro\s)\w+(?=\s)', desc).group(0).encode('utf8')
        except (TypeError, AttributeError):
            metro = desc[:5].encode('utf8')
        infos.append(metro)
    except AttributeError:
        infos.append(['',''])
    
    return infos

def main():
    url = 'http://www.seloger.com/list.htm?idtt=1&idtypebien=1,2&ci=750120,750114&tri=initial&naturebien=1&nb_pieces=2&pxmax=1250&surfacemin=40&LISTING-LISTpg='
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
    session = requests.Session()
    session.max_redirects = 20
    seloger_html = requests.get(url, headers=headers)
    time.sleep(1)
    soup = BeautifulSoup(seloger_html.text,'html.parser')
    
    #Parse les informations sur les appartements sous format JSON
    scripts = soup.find_all(lambda tag: tag.name == 'script' and len(tag.attrs) == 0 )
    for script in scripts:
        data_match = re.match(r'var ava_data = (.*);', script.string.strip().encode('utf8'), re.DOTALL)
        try:
            #print(script.string.strip().encode('utf8'))
            if data_match:
                #data = re.sub(r'(^|\s)(?!\")(?=[a-zA-Z])|(?<=[a-zA-Z])(?<=[^\"])(?=:)|(?=[a-zA-Z])(?=[^\"])(?<=:)|(?=,)(?<!\")(?<=[a-zA-Z])', "\"", bool_test.group(1))
                data = re.sub(r'\s','', data_match.group(1))
                data = re.sub('logged', '\"logged\"',data)
                data = re.sub('products', '\"products\"',data)
                json_data = json.loads(data)
                print(json_data["products"][20])
                #print(json_data["products"][int(nb_annonces)-2])
        except AttributeError:
            pass
    
    #Nombre d'annonces et de pages
    nb_annonces = int(json_data["search"]["nbresults"])
    nb_pages = int(math.ceil(nb_annonces/20)+1)
    print(nb_annonces)
    print(len(json_data["products"]))
    
    print "Il y a " + str(nb_annonces) + " annonces dans " + str(nb_pages) + " pages"
        
    for i in range(1, nb_pages +1):
        if i == 1:
            print("Processing..." + url)
            print()
            annonces_tot = parse_page(url, [])
        else:
            url2 = url + str(i) 
            print("Processing..." + url2)
            annonces_tot = parse_page(url2, annonces_tot)
    
    print(annonces_tot)
    
# url = 'http://www.seloger.com/list.htm?idtt=1&idtypebien=1,2&ci=750120,750114&tri=initial&naturebien=1&nb_pieces=2&pxmax=1250&surfacemin=40'
# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
# session = requests.Session()
# session.max_redirects = 20
# seloger_html = requests.get(url, headers=headers)
# soup = BeautifulSoup(seloger_html.text,'html.parser')
# path = os.getcwd() + '/COMPLET/scrap_seloger.txt'
# f = open(path, 'w')
# f.write(soup.prettify().encode('utf8'))
# #print(soup)

# #Trouver la variable contenant toutes les informations sur les appartements
# #pattern = re.compile('var ava_data = ')
# scripts = soup.find_all(lambda tag: tag.name == 'script' and len(tag.attrs) == 0 )
# for script in scripts:
#     data_match = re.match(r'var ava_data = (.*);', script.string.strip().encode('utf8'), re.DOTALL)
#     try:
#         #print(script.string.strip().encode('utf8'))
#         if data_match:
#             #data = re.sub(r'(^|\s)(?!\")(?=[a-zA-Z])|(?<=[a-zA-Z])(?<=[^\"])(?=:)|(?=[a-zA-Z])(?=[^\"])(?<=:)|(?=,)(?<!\")(?<=[a-zA-Z])', "\"", bool_test.group(1))
#             data = re.sub(r'\s','', data_match.group(1))
#             data = re.sub('logged', '\"logged\"',data)
#             data = re.sub('products', '\"products\"',data)
#             json_data = json.loads(data)
#             nb_annonces = json_data["search"]["nbresults"]
#             print(nb_annonces)
#             print(len(json_data["products"]))
#             print(json_data["products"][0][u'idannonce'])
#             #print(json_data["products"][int(nb_annonces)-2])
#     except AttributeError:
#         pass

#main()
#parse_page_detail('http://www.seloger.com/annonces/locations/appartement/paris-14eme-75/didot-porte-de-vanves/119168749.htm?ci=750114,750120&idtt=1&idtypebien=1,2&naturebien=1&nb_pieces=2&pxmax=1250&surfacemin=40&tri=initial#anchorBar_detail', [])
print(parse_page('http://www.seloger.com/list.htm?idtt=1&idtypebien=1,2&ci=750120,750114&tri=initial&naturebien=1&nb_pieces=2&pxmax=1250&surfacemin=40&LISTING-LISTpg=', []))