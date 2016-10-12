# -*- coding: utf-8 -*-
from lxml import etree
from nltk import SnowballStemmer
import re
from config import *

rutas = {"Telam": {"Politica": "politica.xml", "Ultimas":"ultimasnoticias.xml"}, "Clarin":{"Politica":
                                                                                               "politica_clarin.xml"}}
stemmer = SnowballStemmer("spanish")

def crear_dicc_stopwords():
    stop_words = set()
    for line in open("stopwords_es.txt","r",encoding="utf8"):
        palabra = line[0:-1]
        stop_words.add(palabra)
    return stop_words

stop_words = crear_dicc_stopwords()


def indice_invertido(consulta): #consulta == "title" o consulta =="description"
    inverted={}
    for diario in rutas:
        for seccion in rutas[diario]:
            tree = etree.parse(rutas[diario][seccion])
            nodos = tree.xpath("//item/" + consulta)
            for etiqueta in nodos:
                for palabra in re.split(". |\"| |; |, |\*|\n", etiqueta.text):
                    if palabra not in stop_words and len(palabra) >= 4:
                        palabra_stem = stemmer.stem(palabra)
                        dicc_palabra = inverted.setdefault(palabra_stem, {})
                        dicc_diario = dicc_palabra.setdefault(diario, {})
                        dicc_diario.setdefault(seccion, 0)
                        dicc_diario[seccion] += 1
    return inverted


def crear_ranking(cant_palabras, indice_inv, medio=None, seccion=None):
    lista = []
    for palabra in indice_inv.keys():
        frecuencia = 0
        for diario in indice_inv[palabra].keys():
            if medio == None or diario == medio:
                for sect in indice_inv[palabra][diario]:
                    if seccion == None or sect == seccion:
                        frecuencia += indice_inv[palabra][diario][sect]
        if frecuencia != 0:
            lista.append((palabra, frecuencia))
    ordenada = sorted(lista, key=lambda x: x[1], reverse=True)
    return ordenada[:cant_palabras]


if __name__ == '__main__':
    inv = indice_invertido("title")
    print(crear_ranking(3, inv, seccion="Politica"))