Provisioning a new Site
=======================

## Required packages

* nginx
* Python 3.6
* virtualenv + pip
* Git

## Nginx Virtual Host config

* see `nginx.template.conf`
* replace `DOMAIN` with, e.g, staging.my-domain.com

## Systemd service

* see `gunicorn-systemd.template.service`
* replace `DOMAIN` with, e.g, staging.my-domain.com

## Folder structure

Assuming we have an user account at `/home/username`

```
/home/username
└──sites
   ├──DOMAIN1
   │   ├── db.sqlite3
   │   ├── .env
   │   ├── lists
   │   ├── manage.py
   │   ├── static
   │   ├── superlists
   │   └── virtualenv
   │ 
   └──DOMAIN2
       ├── db.sqlite3
       ├── .env
       ├── lists
       ├── manage.py
       ├── static
       ├── superlists
       └── virtualenv
```