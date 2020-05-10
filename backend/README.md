Open terminal and run:

```shell
virtualenv -p python3 envname
cd envname
source bin/activate
git clone https://github.com/sinisaos/drf-vue.git
cd drf-vue/backend/
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```


