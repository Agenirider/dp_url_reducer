### STAGE 1: Build ###
FROM node:alpine as build

ARG API_HOST
ENV NODE_OPTIONS=--openssl-legacy-provider

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY ./package.json .
COPY ./src /app/src
COPY ./.babelrc .

COPY ./webpack.config.js .
COPY ./package-lock.json .

RUN npm i --save-dev
RUN npm i --save-dev html-webpack-plugin

RUN API_HOST=${API_HOST}/api/v1/ npm run-script build

### STAGE 2: Production Environment ###
FROM nginx:1.13.12-alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY ./nginx/default.conf /etc/nginx/nginx.conf
COPY ./nginx/robots.txt /usr/share/nginx/html
COPY ./nginx/errors /usr/share/nginx/errors

CMD ["nginx", "-g", "daemon off;"]