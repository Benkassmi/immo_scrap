from bs4 import BeautifulSoup
import urllib
import re


#OUVERTURE DE LA PAGE
pap_html = urllib.urlopen('http://www.pap.fr/annonce/vente-appartement-immeuble-loft-atelier-maison-rouen-76-g43640-entre-40000-et-180000-euros-entre-70-et-200-m2-40-annonces-par-page').read()
soup_pap_html = BeautifulSoup(pap_html,'html.parser') #parsing

#NOMBRE D'ANNONCES
div_nbr_annonce = soup_pap_html.body.find("div",attrs={'class': "nombre-annonce"})
span_nbr_annonce = div_nbr_annonce.find('span')
pos = span_nbr_annonce.text.find('>')
nbr_annonce = int(span_nbr_annonce.text[pos+1:1])

print "Il y a " + str(nbr_annonce) + " annonces"

#PARSING DE LA PAGE
spans_prix_annonce = soup_pap_html.body.find_all("span",attrs={'class': "prix"}) 	#PRIX DES ANNONCES
li_surface_annonce = soup_pap_html.body.find_all("li",attrs={'class': "last"})		#SURFACE DES ANNONCES
span_ref_annonce = soup_pap_html.body.find_all("span",attrs={'class': "date"})		#REFERENCE DES ANNONCES


#GET TEXT DU PARSING
lignes_prix_annonce = [span.get_text() for span in spans_prix_annonce]				#PRIX DES ANNONCES
lignes_surface_annonce = [span.get_text() for span in li_surface_annonce]			#SURFACE DES ANNONCES
lignes_ref_annonce = [span.get_text() for span in span_ref_annonce]					#REFERENCE DES ANNONCES

#INITIALISATION DES VARIABLES "clear"
Longueur_chaine_safe = max(len(lignes_prix_annonce),len(lignes_surface_annonce)) + 5
prix_annonce_pap_clear= [u'a'] *  Longueur_chaine_safe							#PRIX DES ANNONCES
int_prix_annonce_pap_clear = [u'a'] *  Longueur_chaine_safe
lignes_surface_annonce_clear = [u'-2'] *  Longueur_chaine_safe				#SURFACE DES ANNONCES
int_lignes_surface_annonce_clear = [u'a'] *  Longueur_chaine_safe			
lignes_ref_annonce_clear = [u'a'] *  Longueur_chaine_safe			

 

#BOUCLE "CLEAR"
i = 0

while i < len(lignes_ref_annonce):

	lignes_prix_annonce[i] = lignes_prix_annonce[i].replace(u'\xa0', u' ')
	prix_annonce_pap_clear[i] = re.sub(r'[^\w]', ' ', lignes_prix_annonce[i]).replace(" ","")
	if prix_annonce_pap_clear[i] == '':
		prix_annonce_pap_clear[i] = "-1"
	int_prix_annonce_pap_clear[i] = int(prix_annonce_pap_clear[i])

	lignes_surface_annonce_clear[i] = lignes_surface_annonce[i].replace(u'\n', u'').replace(" ", "").replace(u'\t', u'').replace("Surface",'').replace("m2",'').replace('Terrain-', "0")
	if lignes_surface_annonce_clear[i] == ("Votrerecherche"):
		lignes_surface_annonce_clear.remove("Votrerecherche")
	
		
	lignes_ref_annonce_clear[i] = lignes_ref_annonce[i].replace(u'\n', u'').replace(" ", "").replace(u'\t', u'')
	i += 1


		
lignes_surface_annonce_clear.remove(u'-2')
int_lignes_surface_annonce_clear = [int(surface) for surface in lignes_surface_annonce_clear ]


j=0
while j < nbr_annonce:
	try:
		del int_prix_annonce_pap_clear[int_lignes_surface_annonce_clear.index(0)]
		del lignes_ref_annonce_clear[int_lignes_surface_annonce_clear.index(0)]
		del int_lignes_surface_annonce_clear[int_lignes_surface_annonce_clear.index(0)]

	except ValueError:
		j += 1
	j += 1


print ""
print int_prix_annonce_pap_clear[0: nbr_annonce]
print int_lignes_surface_annonce_clear[0:nbr_annonce]
print lignes_ref_annonce_clear [0:nbr_annonce]

