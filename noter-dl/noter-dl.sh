#!/bin/bash

#Mi porto nella cartella dove è presente questo script
cd "${0%/*}"

#Scarico l'ultima versione dello script
wget -q https://github.com/TheFax/youtube-dl-utilities/raw/master/noter-dl/noter-dl.py -O noter-dl.py
wget -q https://github.com/TheFax/youtube-dl-utilities/raw/master/noter-dl/settings.py -O settings.py

#Aggiorno youtube-dl
youtube-dl -U

#Rendo eseguibile lo script
chmod a+rx ./noter-dl.py

#Avvio lo script
./noter-dl.py
