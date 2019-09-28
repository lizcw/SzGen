FROM nginx:alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

RUN mkdir -p /etc/nginx/certs
COPY certs/* /etc/nginx/certs/
EXPOSE 8443