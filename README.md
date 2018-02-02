# sec440_2fa_demo

Simple django website that will allow users to log in. Once basic login abilities are in, we'll beginning hooking it to the asterisk api for 2fa.

__Requirements:__

* LAMP stack
* python3.5
* pip3
  * django
  * mysqlclient
  * bcrypt

if mysqlclient is giving trouble, try running `sudo apt-get install libmysqlclient-dev` first

__Running Updates__

When building the program, it is important to make sure that all migrations have been run.
To do so, run:

`python3 manage.py migrate`

if you are making new changes to models, run
`python3 manage.py makemigrations`

to run migrations, run
`python3 manage.py sqlmigrate voip_2fa_demo [migration name]`