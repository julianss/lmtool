#-*- coding: utf-8 -*-
import requests
import sys
import re      
import shutil
import os

def get_dict(path):
    #Mandar petición
    files = {'corpus': open(path, 'rb')}
    params = {'formtype': 'simple'}
    url = "http://www.speech.cs.cmu.edu/cgi-bin/tools/lmtool/run"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 Chrome/41.0'}
    r = requests.post(url, files=files, params=params)
    
    #Lo que regresa tiene un redirect, seguirlo
    match = re.search("Location: (.*)", r.text)
    if match:
        url = match.group(1).strip()
        r = requests.get(url)
        
        #Encontrar el nombre del archivo que hay que bajar
        match = re.search('(TAR(.*?)\.tgz)', r.text)
        if match:
            fname = match.group(1)
            
            #Bajar el archivo y guardarlo como  result.tgz y descomprimirlo
            r = requests.get(url + "/" + fname, stream=True)
            outfname = "result.tgz"
            with open(outfname, "wb") as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
            os.system("tar xvzf " + outfname)
            
            #Abrir el .dic y guardarlo en un diccionario
            d = {}
            with open(match.group(2)+".dic") as f:
                for line in f:
                    values = line.strip().split("\t")
                    d[values[0]] = values[1]
            os.unlink("result.tgz")
            os.system("rm %s.*"%match.group(2))
            return d
    return {}
    
if __name__ == "__main__":
    path = sys.argv[1]
    for k,v in get_dict(path).iteritems():
        print k,v
