import requests 
from bs4 import BeautifulSoup as soup

def get_languages(ID):

   url = f"http://video.google.com/timedtext?type=list&{ID}"
   Soup = soup(requests.get(url).content,"html.parser")
   Languages = Soup.findAll("track")

   return {Language["lang_original"] : Language["lang_code"] for Language in Languages}

get_languages("v=6LD30ChPsSs")