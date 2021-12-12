#!/bin/bash


filename='/etc/nginx/conf.d/domains'
n=1
while read line; do
   echo "
        server {
         listen 80;
        server_name $line;
        return 301 \$scheme://api.redirect.link/url_reducer/redirect/\$server_name\$uri;
        }
      " >> /etc/nginx/conf.d/default.conf

  n=$((n+1))

done < $filename

# Launch nginx
echo "starting nginx ..."
nginx -g "daemon off;"
