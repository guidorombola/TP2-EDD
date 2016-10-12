# coding: utf8
from lxml import etree
import urllib.request
import Stemmer
from config import *


def leer_rss(url):
    try:
        req=urllib.request.Request(url)
        with urllib.request.urlopen(req) as rss:
            datos=rss.read()
        return datos
    except:
        return None

def lematizar(palabra):
    stemmer = Stemmer.Stemmer('spanish')
    return stemmer.stemWord(palabra)

if __name__ == "__main__":
    telam_ultimas=leer_rss(telam_rss_url["ultimas"])
    telam_politica=leer_rss(telam_rss_url["politica"])
    telam_sociedad=leer_rss(telam_rss_url["sociedad"])
    telam_mundo=leer_rss(telam_rss_url["mundo"])
    telam_economia=leer_rss(telam_rss_url["economia"])

    dicc={"establecimiento": lematizar("establecimiento"),
          "establecido": lematizar("establecido"),
          "establecer": lematizar("establecer"),
          "establo": lematizar("establo")}

dicc = {"abarcar": {"Telam":{"Economia":4, "Politica": 2}, "Clarin":{"Economia":6, "Politica": 1}}}