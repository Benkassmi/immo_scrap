import urllib
import re

htmlfile = urllib.urlopen("http://www.pap.fr/annonce/vente-appartement-maison-rouen-76-g43640-jusqu-a-150000-euros-a-partir-de-20-m2-40-annonces-par-page")

htmltext = htmlfile.read()
regex = '<span class="prix">(.+?)</span>'
pattern = re.compile(regex)
price= re.findall(pattern,htmltext)

print price

longu=len(price)

print longu
print price[1]
print price[1].split("&nbsp;&euro;")


regex1 = '<div class="nombre-annonce pull-right">(.*?)</div>'
pattern1 = re.compile(regex1)
nbrannonce= re.findall(pattern1,htmltext)
print nbrannonce

var = '<div class="nombre-annonce pull-right">'
