from bs4 import BeautifulSoup
import requests
import re
import math
import time

def parse_page(url, annonces):
    #OUVERTURE DE LA PAGE
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    session = requests.Session()
    session.max_redirects = 20
    pap_html = requests.get(url, headers=headers)
    time.sleep(1)
    soup_pap_html = BeautifulSoup(pap_html.text,'html.parser')
    
    #PARSING DE LA PAGE
    annonces[0].extend(str(re.search(r'\w{3}\/\w{1,4}', s.get_text()).group()) for s in soup_pap_html.body.find_all("p",attrs={'class': "date"}))		#REFERENCE DES ANNONCES
    annonces[1].extend(int(re.sub(r'[^\w]', ' ', s.get_text().replace(u'\xa0', u' ')).replace(" ","")) for s in soup_pap_html.body.find_all("span",attrs={'class': "price"}))	#PRIX DES ANNONCES
    annonces[2].extend([int(s.find_all("li")[-1].find('strong').contents[0]) for s in soup_pap_html.body.find_all("ul",attrs={'class': 'item-summary'})])		#SURFACE DES ANNONCES
    
    return annonces

def main():
    url = 'http://www.pap.fr/annonce/locations-paris-14e-g37781g37787-2-pieces-jusqu-a-1250-euros-a-partir-de-40-m2'

    #OUVERTURE DE LA PAGE
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    session = requests.Session()
    session.max_redirects = 20
    pap_html = requests.get(url, headers=headers)
    time.sleep(1)
    soup_pap_html = BeautifulSoup(pap_html.text,'html.parser')
    
    #NOMBRE D'ANNONCES
    div_nbr_annonce = soup_pap_html.body.find("div",attrs={'class': "compteur-annonces"})
    span_nbr_annonce = div_nbr_annonce.find('strong')
    nbr_annonce = [int(s) for s in span_nbr_annonce.contents[0].split() if s.isdigit()][0]
    nbr_pages = int(math.ceil(nbr_annonce/10) + 1)
    
    print "Il y a " + str(nbr_annonce) + " annonces dans " + str(nbr_pages) + " pages"
        
    for i in range(1, nbr_pages +1):
        if i == 1:
            print("Processing..." + url)
            annonces_tot = parse_page(url, [[],[],[]])
        else:
            url2 = url + "-" + str(i) 
            print("Processing..." + url2)
            annonces_tot = parse_page(url2, annonces_tot)
    
    print(annonces_tot)
    
main()