config = dict(
    COMMAND_BEST_AUDIO = ['youtube-dl', \
                          '-f','bestaudio', \
                          '--extract-audio', \
                          '--audio-format','mp3', \
                          '--audio-quality','0',\
                          '-k',\
                          '-o','./output/%(title)s - %(id)s.%(ext)s'],

    COMMAND_BEST_VIDEO = ['youtube-dl',\
                          '-f','bestvideo+bestaudio',\
                          '-o','./output/%(title)s - %(id)s.%(ext)s'],

    COMMAND_STANDARD   = ['youtube-dl',\
                          '-f','best',\
                          '-o','./output/%(title)s - %(id)s.%(ext)s'],
)
