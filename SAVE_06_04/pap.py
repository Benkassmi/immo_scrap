from bs4 import BeautifulSoup
import urllib
import re


#OUVERTURE DE LA PAGE
pap_html = urllib.urlopen('http://www.pap.fr/annonce/vente-appartement-immeuble-loft-atelier-maison-rouen-76-g43640-entre-40000-et-150000-euros-entre-20-et-100-m2-40-annonces-par-page').read()
soup_pap_html = BeautifulSoup(pap_html,'html.parser') #parsing

#NOMBRE D'ANNONCES
div_nbr_annonce = soup_pap_html.body.find("div",attrs={'class': "nombre-annonce"})
span_nbr_annonce = div_nbr_annonce.find('span')
pos = span_nbr_annonce.text.find('>')
nbr_annonce = int(span_nbr_annonce.text[pos+1:1])



#PRIX DES ANNONCES
spans_prix_annonce = soup_pap_html.body.find_all("span",attrs={'class': "prix"})
lignes_prix_annonce = [span.get_text() for span in spans_prix_annonce]


prix_annonce_pap_clear= lignes_prix_annonce


#BOUCLE CLEAN PRIX
i = 0
while i < nbr_annonce:
    lignes_prix_annonce[i] = lignes_prix_annonce[i].replace(u'\xa0', u' ')
    prix_annonce_pap_clear[i] = int(re.sub(r'[^\w]', ' ', lignes_prix_annonce[i]).replace(" ",""))
    i += 1




#PRIX DES ANNONCES
li_surface_annonce = soup_pap_html.body.find_all("li",attrs={'class': "last"})
lignes_surface_annonce = [span.get_text() for span in li_surface_annonce]

lignes_surface_annonce_clear = lignes_surface_annonce


#BOUCLES CLEAN SURFACE
i = 0
while i < len(lignes_surface_annonce):
    lignes_surface_annonce[i] = lignes_surface_annonce[i].replace(u'\n', u'').replace(" ", "").replace(u'\t', u'').replace("Surface",'').replace("m2",'').replace('Terrain-', "0")
    i += 1


lignes_surface_annonce_clear[0:len(lignes_surface_annonce)] = lignes_surface_annonce[1:len(lignes_surface_annonce)]

i=0
lignes_surface_annonce_clear = [int(surface) for surface in lignes_surface_annonce_clear ]



#REFERENCE DES ANNONCES
span_ref_annonce = soup_pap_html.body.find_all("span",attrs={'class': "date"})
lignes_ref_annonce = [span.get_text() for span in span_ref_annonce]



#BOUCLES CLEAN  REFERENCE
i = 0
while i < len(lignes_surface_annonce):
    lignes_ref_annonce[i] = lignes_ref_annonce[i].replace(u'\n', u'').replace(" ", "").replace(u'\t', u'')
    i += 1


print "Il y a " + str(nbr_annonce) + " annonces"
print prix_annonce_pap_clear[0: nbr_annonce]
print lignes_surface_annonce_clear [0:nbr_annonce]
print lignes_ref_annonce [0:nbr_annonce]
