FROM debian:bookworm

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        nginx \
        libnginx-mod-http-modsecurity \
        libmodsecurity3 \
        modsecurity-crs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY nginx.conf /etc/nginx/nginx.conf
COPY modsecurity.conf /etc/nginx/modsecurity.conf

COPY crs-setup.conf /etc/nginx/modsecurity.d/crs-setup.conf

CMD ["nginx", "-g", "daemon off;"]
