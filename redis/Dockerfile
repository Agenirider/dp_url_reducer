FROM redis

RUN mkdir -p /data/bases
RUN mkdir -p /data/log

RUN chown -R redis:redis /data
RUN chmod -R 775 /data

CMD ["redis-server"]

EXPOSE 6379