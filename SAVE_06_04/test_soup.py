from bs4 import BeautifulSoup
import urllib

r = urllib.urlopen('http://www.pap.fr/annonce/vente-appartement-maison-rouen-76-g43640-jusqu-a-150000-euros-a-partir-de-20-m2-40-annonces-par-page').read()

soup = BeautifulSoup(r,'html.parser')



nbr_annonce = soup.body.find("div",attrs={'class': "nombre-annonce"})
print nbr_annonce
span = nbr_annonce.find('span')
pos = span.text.find('>')
print span.text[pos+1:1]


