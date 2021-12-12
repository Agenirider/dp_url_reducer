FROM nginx:1.13

COPY ./revers_proxy/default.conf /etc/nginx/conf.d/default.conf
COPY ./url_reducer/domains /etc/nginx/conf.d/domains

COPY ./revers_proxy/entrypoint.sh /entrypoint.sh
RUN chmod -R 755 /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]