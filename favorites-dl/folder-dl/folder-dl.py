#!/usr/bin/python3

import sys
import os
import subprocess
import argparse    #https://docs.python.org/2/howto/argparse.html

# --audio-quality  -->   0 è il massimo

COMMAND_AUDIO = ['youtube-dl', \
                 '-f','bestaudio', \
                 '--extract-audio', \
                 '--audio-format','mp3', \
                 '--audio-quality','0',\
                 '-k']
                 
COMMAND_VIDEO = ['youtube-dl,',\
                 '-f','bestvideo+bestaudio']

def main():
   #Parser degli argomenti
   parser = argparse.ArgumentParser(description='Scarica da YouTube i video elencati nel file')
   parser.add_argument("file", help="file contenente l'elenco dei video (servono diritti RW)")
   parser.add_argument("-t", "--type", type=str, choices=["a", "v"], help="specifica se scaricare a-audio o v-video")
   args = parser.parse_args()

   filepath = args.file

   #Verifico se il file esiste
   if not os.path.isfile(filepath):
       print("[ERR] Il file {} non esiste.".format(filepath))
       sys.exit()

   #valuto gli argomenti passati allo script
   if args.type == "a":
      print("[INFO] Si è scelto di scaricare l'audio")
      command = COMMAND_AUDIO.copy()
   elif args.type == "v":
      print("[INFO] Si è scelto di scaricare il video")
      command = COMMAND_VIDEO.copy()
   else:
      print("Per default si scarica l'audio")
      print("Per scaricare il video, vedere la guida argomenti: -h")
      command = COMMAND_AUDIO.copy()
   
   analizzaFile(filepath, command)


def analizzaFile(filepath, command):
    #trasferisco tutto il file in una lista
    print("[INFO] Lettura del file {}".format(filepath))
    with open(filepath) as fp:
        content_list = [line.rstrip('\n') for line in fp]

    #trim di ogni riga per rimuovere spazi iniziali e finali
    for i in range(len(content_list)):
        content_list[i] = content_list[i].strip()

    #tolgo tutte le righe vuote
    content_list = list(filter(None, content_list))

    #verifico che ogni elemento della lista abbia il prefisso URL davanti, sennò lo metto     
    for i in range(len(content_list)):
        if len(content_list[i]) == 11:
           content_list[i] = "https://www.youtube.com/watch?v=" + content_list[i]

    #digerisco la lista: download dei file e rimozione dell'elemento dalla lista e dal file
    for i in range(len(content_list)):
        print("[INFO] Download e conversione di: {}".format(content_list[0]))
        cmd = command.copy()
        cmd.append(content_list[0])
        try:
             #print (cmd)
             res = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except OSError:
            print("[ERR] Subprocess popen.")
            exit(-1)

        res.wait()

        #Se qualcosa è andato storto, non devo cancellare l'elemento dal file.
        #Per fare questo, allungo la lista aggiungendo alla fine l'elemento non scaricato.
        #Siccome la reiterazione avviene per un numero preciso di volte, mi troverò alla
        #fine ad aver finito questo ciclo FOR con degli elementi ancora presenti in lista.
        #Tali elementi sono appunto quelli che aggiungo mediante la seguente riga:
        if res.returncode !=0:
           print("[ERR] Impossibile scaricare {} - Returncode: {}".format(content_list[0],res.returncode))
           content_list.append(content_list[0])
        else:
           print("[INFO] {} scaricato con successo.".format(content_list[0]))

        output = res.stdout.read()
        
        #In questo punto del programma, output è una lista e contiene riga per riga
        #  tutte le info ritornate da youtube-dl
        #TODO: analizzare il ritorno di youtube-dl alla ricerca di errori o info utili
        
        #for output_line in output:
        #    print("line {}".format(output_line))

        content_list.pop(0) #rimuovo l'elemento [0] cioè quello appena elaborato

        #ri-salvo il file, con la lista aggiornata.
        #print("[INFO] Aggiornamento del file {}".format(filepath))
        with open(filepath, 'w') as fp:
            for item in content_list:
                fp.write("%s\n" % item)
        
    print("[INFO] Fine elementi.")
    print("[INFO] Esecuzione terminata.")
    exit(0)

if __name__ == '__main__':
   main()
