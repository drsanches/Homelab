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
4. `sudo apt install python3-pip -y`

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

#### TODO: Close cockpit_internal_port

# Commands

```shell
ansible-playbook \
    -i inventory_example.yml \
    -u user --ask-pass --ask-become-pass \
    server.yml
```

