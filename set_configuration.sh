#!/bin/bash

set -x

docker exec -u www-data storage-nextcloud php occ --no-warnings config:system:get trusted_domains >> trusted_domain.tmp

if ! grep -q "www.rfi.avanta-sourcing.com" trusted_domain.tmp; then
    TRUSTED_INDEX=$(cat trusted_domain.tmp | wc -l);
    docker exec -u www-data storage-nextcloud php occ --no-warnings config:system:set trusted_domains $TRUSTED_INDEX --value="www.rfi.avanta-sourcing.com:8443"
fi

if ! grep -q "rfi.avanta-sourcing.com" trusted_domain.tmp; then
    TRUSTED_INDEX=$(cat trusted_domain.tmp | wc -l);
    docker exec -u www-data storage-nextcloud php occ --no-warnings config:system:set trusted_domains $TRUSTED_INDEX --value="rfi.avanta-sourcing.com:8443"
fi

if ! grep -q "nginx-server" trusted_domain.tmp; then
    TRUSTED_INDEX=$(cat trusted_domain.tmp | wc -l);
    docker exec -u www-data storage-nextcloud php occ --no-warnings config:system:set trusted_domains $TRUSTED_INDEX --value="nginx-server"
fi

if ! grep -q "onlyoffice-document-server" trusted_domain.tmp; then
    TRUSTED_INDEX=$(cat trusted_domain.tmp | wc -l);
    docker exec -u www-data storage-nextcloud php occ --no-warnings config:system:set trusted_domains $TRUSTED_INDEX --value="onlyoffice-document-server"
fi

rm trusted_domain.tmp

docker exec -u www-data storage-nextcloud php occ --no-warnings app:install onlyoffice

docker exec -u www-data storage-nextcloud php occ --no-warnings config:system:set onlyoffice DocumentServerUrl --value="/ds-vpath/"
docker exec -u www-data storage-nextcloud php occ --no-warnings config:system:set onlyoffice DocumentServerInternalUrl --value="http://onlyoffice-document-server/"
docker exec -u www-data storage-nextcloud php occ --no-warnings config:system:set onlyoffice StorageUrl --value="https://nginx-server:8443/" 
docker exec -u www-data storage-nextcloud php occ --no-warnings config:system:set onlyoffice jwt_secret --value="secret"
