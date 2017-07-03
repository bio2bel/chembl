# -*- coding: utf-8 -*-

#import pandas as pd
#import requests
import ftplib

if __name__ == "__main__":
    dirname = '~/.pybel/data/bio2bel/chembl'
    url_dir_chembl = "/ftp.ebi.ac.uk/"

    ftp = ftplib.FTP(url_dir_chembl)
    ftp.login()
    chembldb_files = []
    try:
        chembldb_files = ftp.nlst()
    except ftplib.error_perm as resp:
        print("in error")
        print(str(resp))

    for f in chembldb_files:
        print(f)