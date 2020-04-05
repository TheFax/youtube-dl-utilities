#!/usr/bin/python3

import settings
import web_settings
import requests
import subprocess

GOOD=0
FAIL=-1

def main():
    r = requests.get(web_settings.web_config['JSON_LINK'])
    if r.status_code != 200:
        #r.status_code conterrà 200 se la richiesta è andata a buon fine
        print("[ERR] impossibile contattare il server contenente la lista json")
        exit(-1)

    values=r.json()
    #print(values)

    for x in range(len(values)):
        print("\n")
        #print("ID {} - Analisi della nota".format(values[x]['ID']))
        if values[x]['title'] == "a":
            print("ID {} - Sarà scaricato l'audio alla massima qualità".format(values[x]['ID']))
            status = download(values[x]['content'], settings.config['COMMAND_BEST_AUDIO'])
            feedbackNote(values[x]['ID'], status)

        elif values[x]['title'] == "v":
            print("ID {} - Audio e video saranno scaricati e muxati insieme alla massima qualità".format(values[x]['ID']))
            status = download(values[x]['content'], settings.config['COMMAND_BEST_VIDEO'])
            feedbackNote(values[x]['ID'], status)

        elif values[x]['title'] == "b":
            print("ID {} - Sarà scaricato l'audio (massima qualità) e anche il video (massima qualità)".format(values[x]['ID']))
            status = download(values[x]['content'], settings.config['COMMAND_BEST_AUDIO'])
            status = status + download(values[x]['content'], settings.config['COMMAND_BEST_VIDEO'])
            feedbackNote(values[x]['ID'], status)

        elif values[x]['title'] == "n":
            print("ID {} - Sarà scaricato il video in formato standard".format(values[x]['ID']))
            status = download(values[x]['content'], settings.config['COMMAND_STANDARD'])
            feedbackNote(values[x]['ID'], status)

        else:
            print("ID {} - La nota sarà ignorata poichè non sembra diretta a questo script".format(values[x]['ID']))

    exit(0)

def feedbackNote(identifier, status):
    if status == GOOD:
        deleteNote(identifier)

def deleteNote(identifier):
    link = web_settings.web_config['DEL_LINK'] + str(identifier)
    r = requests.get(link)

def download(youtubeLink, command):
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
        res = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError:
        #raise #PER DEBUG
        print("[ERR] Subprocess popen.")
        exit(-1)

    res.wait()

    output = res.stdout.read()
    #In questo punto del programma, output è una lista e contiene riga per riga
    #  tutte le info ritornate da youtube-dl
    #TODO: analizzare il ritorno di youtube-dl alla ricerca di errori o info utili

    if res.returncode !=0:
        print("[ERR] Impossibile scaricare {} - Returncode: {}".format(youtubeLink,res.returncode))
        return FAIL
    else:
        print("[INFO] {} scaricato con successo.".format(youtubeLink))
        return GOOD

if __name__ == '__main__':
   main()
