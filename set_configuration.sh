#!/bin/bash

source .env 

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
docker exec -u www-data storage-nextcloud php occ --no-warnings config:system:set onlyoffice StorageUrl --value=$STORAGE_URL
docker exec -u www-data storage-nextcloud php occ --no-warnings config:system:set onlyoffice jwt_secret --value=$JWT_SECRET

# Set .services.CoAuthoring.requestDefaults.rejectUnauthorized = false
docker cp default.json onlyoffice-document-server:/etc/onlyoffice/documentserver/default.json
docker exec -it -d onlyoffice-document-server ./app/ds/run-document-server.sh

# Attention si image nextcloud plus récente s'installe : {"error":"Strict Cookie has not been found in request"}
# Il faut downgraded et donc supprimer le volume sinon : Can't start Nextcloud because the version of the data (21.0.0.18) is higher than the docker image version (19.0.9.1) and downgrading is not supported. Are you sure you have pulled the newest image version?