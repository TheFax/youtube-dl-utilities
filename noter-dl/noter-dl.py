#!/usr/bin/python3

import settings
import web_settings
import requests
import subprocess

GOOD=0
FAIL=-1

def main():
    #Richiedo al server la lista
    r = requests.get(web_settings.web_config['JSON_LINK'])
    if r.status_code != 200:
        #r.status_code conterrà 200 se la richiesta è andata a buon fine
        print("[ERR] impossibile contattare il server contenente la lista json")
        exit(-1)

    #Converto la risposta json in un array multidimensionale
    values=r.json()
    #print(values)

    #Analizzo riga per riga tutto l'array
    for x in range(len(values)):
        print("\n")

        #print("ID {} - Analisi della nota".format(values[x]['ID']))

        #Audio
        if values[x]['title'] == "a":
            print("ID {} - Sarà scaricato l'audio alla massima qualità".format(values[x]['ID']))
            status = download(values[x]['content'], settings.config['COMMAND_BEST_AUDIO'])
            feedbackNote(values[x]['ID'], status)
        
        #Video
        elif values[x]['title'] == "v":
            print("ID {} - Audio e video saranno scaricati e muxati insieme alla massima qualità".format(values[x]['ID']))
            status = download(values[x]['content'], settings.config['COMMAND_BEST_VIDEO'])
            feedbackNote(values[x]['ID'], status)

        #Both
        elif values[x]['title'] == "b":
            print("ID {} - Sarà scaricato l'audio (massima qualità) e anche il video (massima qualità)".format(values[x]['ID']))
            status = download(values[x]['content'], settings.config['COMMAND_BEST_AUDIO'])
            status = status + download(values[x]['content'], settings.config['COMMAND_BEST_VIDEO'])
            feedbackNote(values[x]['ID'], status)

        #Normal
        elif values[x]['title'] == "n":
            print("ID {} - Sarà scaricato il video in formato standard".format(values[x]['ID']))
            status = download(values[x]['content'], settings.config['COMMAND_STANDARD'])
            feedbackNote(values[x]['ID'], status)
        
        #Lista
        elif values[x]['title'] == "l":
            print("ID {} - Sarà scaricata l'intera playlist".format(values[x]['ID']))
            status = download(values[x]['content'], settings.config['COMMAND_PLAYLIST'])
            feedbackNote(values[x]['ID'], status)

        else:
            print("ID {} - La nota sarà ignorata poichè non sembra diretta a questo script".format(values[x]['ID']))

    #Fine dello script senza errori
    exit(0)

def feedbackNote(identifier, status):
    #Questa funzione raccoglie il feedback e decide cosa fare

    #Se è andato tutto bene, elimino la nota
    if status == GOOD:
        print("[INFO] Elimino la nota ID {}".format(identifier))
        deleteNote(identifier)

def deleteNote(identifier):
    #Questa funzione elimina la nota con ID dato come argomento
    link = web_settings.web_config['DEL_LINK'] + str(identifier)
    r = requests.get(link)

def download(youtubeLink, command):
    #Questa funzione si occupa di scaricare materialmente il video YouTube
    #Argomento 1: youtubeLink - Il link da scaricare.
    #Argomento 2: command - è una LIST contenente il nome del programma da richiamare e tutti gli argomenti da passargli

    #print (youtubeLink)
    #print (command)
    #print (type(command))

    #if len(youtubeLink) == 11:
    #    print("[INFO] Il link fornito verrà normalizzato col prefisso YouTube.")
    #    youtubeLink = "https://www.youtube.com/watch?v=" + youtubeLink
    #if len(youtubeLink) > 43:
    #    print("[INFO] Il link fornito verrà ridotto al solo link fondamentale.")
    #    youtubeLink = youtubeLink[0:youtubeLink.find("&")]

    print("[INFO] Download del link: {}".format(youtubeLink))
    cmd = command.copy()
    cmd.append(youtubeLink)

    try:
        #print (cmd)
        #res = subprocess.Popen(cmd, stderr=subprocess.STDOUT)
        res = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError:
        #raise #PER DEBUG
        print("[ERR] Subprocess popen.")
        exit(-1)

    res.wait()

    output_out = res.stdout.read()
    output_err = res.stderr.read()
    return_code = res.returncode
    
    #In questo punto del programma, output_xxx sono dei b'' bytes e contengono riga per riga
    # tutte le info ritornate da youtube-dl. Ogni riga è delimitata da un carattere di escape '/n'
        
    #print("VALORE DI OUTPUT:")
    #print(output_out)   # returns b''
    #print(output_err)   # returns b''

    if output_err.find(b'ERROR') != -1 :
        print("[ERR] Impossibile scaricare {} - ERROR in the output pipe".format(youtubeLink))
        return FAIL

    if return_code !=0 :
        print("[ERR] Impossibile scaricare {} - Returncode: {}".format(youtubeLink,res.returncode))
        return FAIL

    print("[INFO] {} scaricato con successo.".format(youtubeLink))
    return GOOD

if __name__ == '__main__':
   main()
