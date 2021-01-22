config = dict(
    COMMAND_BEST_AUDIO = ['youtube-dl', \
                            '--socket-timeout','15', \
                            '-f','bestaudio', \
                            '--extract-audio', \
                            '--audio-format','mp3', \
                            '--audio-quality','0',\
                            '-k',\
                            '-o','./output/%(title)s - %(id)s.%(ext)s'],

    COMMAND_BEST_VIDEO = ['youtube-dl',\
                            '--socket-timeout','15', \
                            '-f','bestvideo+bestaudio',\
                            '-o','./output/%(title)s - %(id)s.%(ext)s'],

    COMMAND_720 = ['youtube-dl',\
                            '--socket-timeout','15', \
                            '-f','136+251',\
                            '-o','./output/%(title)s - %(id)s.%(ext)s'],

    COMMAND_1080 = ['youtube-dl',\
                            '--socket-timeout','15', \
                            '-f','137+251',\
                            '-o','./output/%(title)s - %(id)s.%(ext)s'],

    
    COMMAND_STANDARD   = ['youtube-dl',\
                            '--socket-timeout','15', \
                            '-f','best',\
                            '-o','./output/%(title)s - %(id)s.%(ext)s'],

    COMMAND_PLAYLIST   = ['youtube-dl',\
                            '--socket-timeout','15', \
                            '-f','best',\
                            '-i',\
                            '--yes-playlist',\
                            '-o','./output/%(title)s - %(id)s.%(ext)s'],

)
