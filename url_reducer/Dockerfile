# pull official base image
FROM python:3.8.3-alpine

# SET WORK DIRECTORY
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code

# SET ENVIRONMENT VARIABLES

# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1

# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# INSTALL DEPNDENCIES
RUN apk update \
    && apk add --virtual build-deps gcc g++ make libffi-dev python3-dev musl-dev mariadb-connector-c-dev \
    && apk add mysql-client

RUN pip install --upgrade pip
RUN pip install pynacl
RUN pip install pymysql mysqlclient --no-cache-dir
RUN python3 -m pip install -r requirements.txt --no-cache-dir

COPY . /code
RUN chmod +x /code/* \
    && chmod 777 /code/entrypoint.sh \
    && chmod 777 -R /code/url_reducer \
    && touch /code/url_reducer/debug.log \
    && chmod 777 /code/url_reducer/debug.log


# STATIC FILE SERVING
RUN mkdir -p /vol/web/static \
    && mkdir -p /vol/web/media

RUN adduser -D user \
    && chmod -R 755 /vol/web \
    && chown -R user:user /vol


#RUN python manage.py test

USER user

CMD ["sh","entrypoint.sh"]