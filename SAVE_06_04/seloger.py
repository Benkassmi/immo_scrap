from bs4 import BeautifulSoup
import urllib
import re


#OUVERTURE DE LA PAGE
pap_html = urllib.urlopen('http://www.pap.fr/annonce/vente-appartement-maison-rouen-76-g43640-jusqu-a-150000-euros-a-partir-de-20-m2-40-annonces-par-page').read()
soup_pap_html = BeautifulSoup(pap_html,'html.parser') #parsing

#NOMBRE D'ANNONCES
div_nbr_annonce = soup_pap_html.body.find("div",attrs={'class': "nombre-annonce"})
span_nbr_annonce = div_nbr_annonce.find('span')
pos = span_nbr_annonce.text.find('>')
nbr_annonce = int(span_nbr_annonce.text[pos+1:1])
print "Il y a " + str(nbr_annonce) + " annonces"


#PRIX DES ANNONCES
spans_prix_annonce = soup_pap_html.body.find_all("span",attrs={'class': "prix"})
lignes_prix_annonce = [span.get_text() for span in spans_prix_annonce]


prix_annonce_pap_clear= lignes_prix_annonce


#BOUCLE CLEAN PRIX
i = 0
while i < nbr_annonce:
    lignes_prix_annonce[i] = lignes_prix_annonce[i].replace(u'\xa0', u' ')
    print lignes_prix_annonce[i]
    prix_annonce_pap_clear[i] = int(re.sub(r'[^\w]', ' ', lignes_prix_annonce[i]).replace(" ",""))
    i += 1

print prix_annonce_pap_clear[0: nbr_annonce]



