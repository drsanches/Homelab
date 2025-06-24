# Overview

**Services:**
- Cockpit
- Nextcloud
- Nginx (proxy)

## Server requirements

**OS:** Ubuntu Server 24.04.2 LTS

1. `sudo apt install net-tools`
2. `sudo apt install openssh-server -y`
3. `sudo apt install python3`
4. `sudo apt install python3-pip`

## Folder structure

```text
/
├── etc/
│   ├── cockpit/
│   │   └── cockpit.conf                # [Cockpit] Cockpit config for proxying
│   └── systemd/
│       └── system/
│           ├──cockpit.socket.d/
│           │  └── listen.conf          # [Cockpit] Cockpit socket config
│           ├── nginx.service           # [Nginx] Nginx service
│           └── nextcloud.service       # [Nextcloud] Nextcloud service
│
├── opt/
│   ├── nextcloud/
│   │   ├── docker-copmose.yml          # [Nextcloud] Nextcloud docker compose 
│   │   └── .env                        # [Nextcloud] Environment for docker compose 
│   │
│   └── nginx/
│       ├── config/
│       │   ├── config.d/
│       │   │   ├── cockpit.conf        # [Nginx] Nginx config for cockpit
│       │   │   └── nextcloud.conf      # [Nginx] Nginx config for nextcloud
│       │   └── nginx.conf              # [Nginx] Main nginx config (includes config.d)
│       ├── ssl/
│       │   ├── domain.key              # [Nginx] Private key
│       │   └── domain.crt              # [Nginx] Certificate
│       └── docker-compose.yml          # [Nginx] Nginx docker compose
│
├── {{ nginx_logs }}/
│   ├── cockpit/                        # [Nginx] Cockpit access and error logs
│   └── nextcloud/                      # [Nginx] Nextcloud access and error logs
│
└── {{ nextcloud_data_directory }}/
    ├── app_data/
    │   ├── data/                       # [Nextcloud] Nextcloud data of all users
    │   └── config/
    │       └──config.php               # [Nextcloud] Main nextcloud config
    └── db/                             # [Nextcloud] Nextcloud database data
 ```

## Network diagram

![Network diagram](./doc/network_diagram.drawio.png)

# Commands

```shell
ansible-playbook \
-i 172.30.137.122, -e ansible_port=122 \
-u user --ask-pass --ask-become-pass \
--extra-vars "new_port=123" \
set_ssh_port.yaml
```

```shell
ansible-playbook \
-i 172.30.137.122, -e ansible_port=123 \
-u user --ask-pass --ask-become-pass \
apt_update_and_upgrade.yaml
```

```shell
ansible-playbook \
-i 172.30.137.122, -e ansible_port=123 \
-u user --ask-pass --ask-become-pass \
install_cockpit.yaml
```

```shell
ansible-playbook \
-i 172.30.137.122, -e ansible_port=123 \
-u user --ask-pass --ask-become-pass \
install_docker.yaml
```

```shell
ansible-playbook \
-i 172.30.137.122, -e ansible_port=123 \
-u user --ask-pass --ask-become-pass \
--extra-vars "nextcloud_data_directory=/mnt/md127/nextcloud \
              db_root_password=pswd \
              db_password=pswd" \
install_nextcloud.yaml
```

```shell
ansible-playbook \
-i 172.30.137.122, -e ansible_port=123 \
-u user --ask-pass --ask-become-pass \
--extra-vars "cockpit_external_port=9435 \
              nextcloud_external_port=9436 \
              nginx_logs=/mnt/md127/nginx/logs" \
install_nginx.yaml
```

```shell
ansible-playbook \
-i 172.30.137.122, -e ansible_port=123 \
-u user --ask-pass --ask-become-pass \
--extra-vars "nextcloud_data_directory=/mnt/md127/nextcloud \
              protocol=https \
              host=172.30.137.122:9436" \
configure_nextcloud.yaml
```
