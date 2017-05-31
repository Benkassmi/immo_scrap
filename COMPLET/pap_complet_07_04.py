from bs4 import BeautifulSoup
import urllib
import re


#OUVERTURE DE LA PAGE
pap_html = urllib.urlopen('http://www.pap.fr/annonce/locations-paris-75-g439-2-pieces-a-partir-de-40-m2').read()
soup_pap_html = BeautifulSoup(pap_html,'html.parser') #parsing

#NOMBRE D'ANNONCES
div_nbr_annonce = soup_pap_html.body.find("div",attrs={'class': "compteur-annonces"})
span_nbr_annonce = div_nbr_annonce.find('strong')
nbr_annonce = [int(s) for s in span_nbr_annonce.contents[0].split() if s.isdigit()][0]

print "Il y a " + str(nbr_annonce) + " annonces"

#PARSING DE LA PAGE
spans_prix_annonce = soup_pap_html.body.find_all("span",attrs={'class': "price"}) 	#PRIX DES ANNONCES
li_surface_annonce = [int(s.find_all("li")[-1].find('strong').contents[0]) for s in soup_pap_html.body.find_all("ul",attrs={'class': 'item-summary'})]		#SURFACE DES ANNONCES
span_ref_annonce = soup_pap_html.body.find_all("p",attrs={'class': "date"})		#REFERENCE DES ANNONCES

#GET TEXT DU PARSING
lignes_prix_annonce = [span.get_text() for span in spans_prix_annonce]				#PRIX DES ANNONCES
#lignes_surface_annonce = [span.get_text() for span in li_surface_annonce]			#SURFACE DES ANNONCES
lignes_ref_annonce = [span.get_text() for span in span_ref_annonce]					#REFERENCE DES ANNONCES
print(len(lignes_ref_annonce))

#INITIALISATION DES VARIABLES "clear"
Longueur_chaine_safe = max(len(lignes_prix_annonce),len(li_surface_annonce)) + 5
prix_annonce_pap_clear= [u'a'] *  Longueur_chaine_safe							#PRIX DES ANNONCES
int_prix_annonce_pap_clear = [u'a'] *  Longueur_chaine_safe
lignes_surface_annonce_clear = [u'-2'] *  Longueur_chaine_safe				#SURFACE DES ANNONCES
int_lignes_surface_annonce_clear = [u'a'] *  Longueur_chaine_safe			
lignes_ref_annonce_clear = [u'a'] *  Longueur_chaine_safe			

 

#BOUCLE "CLEAR"
i = 0

while i < len(lignes_ref_annonce):
	print(lignes_prix_annonce[i])
	lignes_prix_annonce[i] = lignes_prix_annonce[i].replace(u'\xa0', u' ')
	print(lignes_prix_annonce[i])
	prix_annonce_pap_clear[i] = re.sub(r'[^\w]', ' ', lignes_prix_annonce[i]).replace(" ","")
	if prix_annonce_pap_clear[i] == '':
		prix_annonce_pap_clear[i] = "-1"
	int_prix_annonce_pap_clear[i] = int(prix_annonce_pap_clear[i])

	# lignes_surface_annonce_clear[i] = lignes_surface_annonce[i].replace(u'\n', u'').replace(" ", "").replace(u'\t', u'').replace("Surface",'').replace("m2",'').replace('Terrain-', "0")
	# if lignes_surface_annonce_clear[i] == ("Votrerecherche"):
	# 	lignes_surface_annonce_clear.remove("Votrerecherche")
	
		
	lignes_ref_annonce_clear[i] = lignes_ref_annonce[i].replace(u'\n', u'').replace(" ", "").replace(u'\t', u'')
	i += 1


		
lignes_surface_annonce_clear.remove(u'-2')
int_lignes_surface_annonce_clear = li_surface_annonce


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

