ls
django-admin startapp conf
ls
ll
cd conf
ls
cd ..
rm -rf conf
django-admin startproject conf
cd conf
ll
mv manage.py  conf ..
ll
mv conf/* .
ll
rmdir conf
ll
cd ..
ll
pip install -r requirements.txt 
ll
django-admin startapp webconsole
ll
vi conf/settings.py 
ll
ll
vi conf/urls.py 
vi webconsole/views.py 
vi webframe/views.py 
vi conf/urls.py 
vi webconsole/views.py 
ll
exit
django-admin makemigrations
ls
./manage.py makemigrations
./manage.py migrate
./manage.py createsuperuser 
exit
