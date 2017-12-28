## IMPI Boot Tool

This is a simple tool that allows you to boot/reboot/power down servers via IPMI

### Setup & Running

This requires you to have `python3`, `pip3`, andy `python3-virtualenv` installed. pip may be included with your installation of python 3. Package names may be different depending on your distribution.

This tool uses Django. It is recommended you install Django via pip in a virtualenv.

1. Clone this repository and then cd into the cloned directory.

2. Configure the environment

```
$ virtualenv --python=`which python3` ~/.virtualenvs/djangodev

$ source ~/.virtualenvs/djangodev/bin/activate

$ pip3 install Django

$ python3 manage.py migrate

$ python3 manage.py runserver
```

This will start a development server at http://127.0.0.1:8000

If you wish to run this in a webserver, the recommended way is to use `gunicorn` and `nginx`.

1. Install Gunicorn

```
$ pip3 install gunicorn
```

Navigate to the root of the cloned repository

```
$ gunicorn servermgr.wsgi
```

2. Configure your web server for Gunicorn
http://docs.gunicorn.org/en/stable/deploy.html

### Usage

 - Navigate to the root directory of this application
 - From here you can add/delete servers, see a list of servers and navigate to individual server pages to send boot/reboot/shut down commands.
