from fabric.api import local

def add(app_name):
    local('python manage.py startapp %s' % app_name)

def run():
    local('python manage.py runserver')