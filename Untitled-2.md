sudo nano /etc/systemd/system/santinelli.service

[Unit]
Description=Gunicorn instance to serve santinelli
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/home/santinelli_django
Environment="PATH=/home/santinelli_django/venv/bin"
ExecStart=/home/santinelli_django/venv/bin/gunicorn --workers 3 --bind unix:/home/santinelli_django/santinelli.sock project.wsgi:application

[Install]
WantedBy=multi-user.target

sudo nano /etc/systemd/system/santinelli.socket

[Unit]
Description=Gunicorn socket for santinelli Django project

[Socket]
ListenStream=/home//santinelli.sock

[Install]
WantedBy=sockets.target

sudo systemctl daemon-reload

sudo apt update
sudo apt install nginx -y

sudo systemctl start nginx
sudo systemctl enable nginx

sudo nano /etc/nginx/sites-available/santinelli

server {
    listen 80;
    server_name santinelli.com.br www.santinelli.com.br;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/santinelli_django/static/;
    }

    location /media/ {
        alias /home/santinelli_django/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/santinelli_django/santinelli.sock;
    }
}

sudo ln -s /etc/nginx/sites-available/santinelli /etc/nginx/sites-enabled/

sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d santinelli.com.br -d www.santinelli.com.br




