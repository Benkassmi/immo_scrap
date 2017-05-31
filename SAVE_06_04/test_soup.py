from bs4 import BeautifulSoup
import urllib

r = urllib.urlopen('http://www.pap.fr/annonce/locations-paris-14e-g37781g37787-2-pieces-jusqu-a-1250-euros-a-partir-de-40-m2').read()
soup = BeautifulSoup(r,'html.parser')
f = open('scarp.txt', 'w')
f.write(soup.prettify().encode('utf8'))


nbr_annonce = soup.body.find("div",attrs={'class': "compteur-annonces"})
print nbr_annonce
span = nbr_annonce.find('strong')
print([int(s) for s in span.contents[0].split() if s.isdigit()][0])



