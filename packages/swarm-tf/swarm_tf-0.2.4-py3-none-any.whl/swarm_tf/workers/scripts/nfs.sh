#!/usr/bin/env bash

apt install -y nfs-kernel-server nfs-common
chown nobody:nogroup /data

cat << EOF > /etc/exports
/data    10.0.0.0/8(rw,sync,no_subtree_check)
EOF

systemctl restart nfs-kernel-server
systemctl status nfs-kernel-server




#---- @todo remove this
# test
sudo apt install -y nfs-common
sudo mount -t nfs4 persistent-01-internal.t.xpto.us:/data /tmp/x

https://vitux.com/install-nfs-server-and-client-on-ubuntu/

https://docs.docker.com/engine/reference/commandline/volume_create/
https://forums.docker.com/t/docker-compose-how-to-use-nfs-volumes/23255/2

docker volume create --driver local \
    --opt type=nfs4 \
    --opt o=addr=persistent-01-internal.t.xpto.us,rw,noatime,rsize=8192,wsize=8192,tcp,timeo=14 \
    --opt device=:/data \
    persistent-01-nfs



version: '3.4'
services:
  php-fpm:
    image: byjg/php:7.3-fpm-nginx
    volumes:
      - type: volume
        source: nfs
        target: /xyz
        volume:
          nocopy: true

volumes:
  nfs:
    driver: local
    driver_opts:
      type: "nfs4"
      o: "addr=persistent-01-internal.t.xpto.us,rw,noatime,nolock,soft"
      device: ":/data"

Failure
error while mounting volume '/var/lib/docker/volumes/teste/_data':
failed to mount local volume: mount :/data:/var/lib/docker/volumes/teste/_data, flags: 0x400, data: addr=persistent-01-internal.t.xpto.us,rsize=8192,wsize=8192,tcp,timeo=14: invalid argument