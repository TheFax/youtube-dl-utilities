config = dict(
    JSON_LINK = "https://xxxxxxxx/index.php?list=1",
    DEL_LINK  = "https://xxxxxxxx/index.php?del=",
    COMMAND_BEST_AUDIO = ['youtube-dl', \
                          '-f','bestaudio', \
                          '--extract-audio', \
                          '--audio-format','mp3', \
                          '--audio-quality','0',\
                          '-k'],
    COMMAND_BEST_VIDEO = ['youtube-dl',\
                          '-f','bestvideo+bestaudio'],
    COMMAND_STANDARD   = ['youtube-dl',\
                          '-f','best'],
)
