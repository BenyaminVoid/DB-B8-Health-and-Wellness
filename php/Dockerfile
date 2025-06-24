
FROM php:8.2-apache

RUN apt-get update && apt-get install -y \
    libssl-dev \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN docker-php-ext-install pdo_sqlite
RUN pecl install mongodb && docker-php-ext-enable mongodb