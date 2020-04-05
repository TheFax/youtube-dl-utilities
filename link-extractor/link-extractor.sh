sed -n 's/.*href="https:\/\/www.youtube.com\/watch?v=\([^&^"]*\).*/\1/p' 'Video piaciuti - YouTube.html' | uniq | sed -n 's/.*/https:\/\/www.youtube.com\/watch?v=&/p' > output.txt
