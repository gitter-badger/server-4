===============
Getting Started
===============

Generate a config file
----------------------
Use `argux-server_genconfig` to generate a configuration-file.
This command asks you a number of questions about the preferred
configuration before generating the configuration-file::

   $ argux-server_genconfig

   ###########################################
   ###                                     ###
   ### Argux Server configuration wizard.  ###
   ###                                     ###
   ###########################################

Specify the location where the configuration-file should be created::

   Config file location[./argux-server.ini]: 

If the file already exists, you are asked if it okay to overwrite.
Answering 'y' will continue the wizard, 'n' will terminate it::

   File 'filename' exists, overwrite? ['y','n'] (Default: y): 

If you do not plan to use Argux-Server over HTTPS, you can disable
secure-cookies, it is advised to use secure-cookies::

   Use secure cookies? (Enforce HTTPS) ['y', 'n'] (Default: y): 

.. NOTE::
   If secure-cookies is enabled and you don't use HTTPS, the system won't work.

Debugging
~~~~~~~~~

Do you want to enable debugging? (useful for development or troubleshooting)::

   Enable debugging? ['y', 'n'] (Default: n): 

WSGI Server
~~~~~~~~~~~
Pick the wsgi server::

   WSGI Server? ['pserve','uwsgi'] (Default: pserve):

If you've picked pserve, you start argux-server like this::

   pserve argux-server.ini

If you've picked uwsgi, it will start as followed::

   uwsgi --ini-paste argux-server.ini

Database Configuration
~~~~~~~~~~~~~~~~~~~~~~
Choose the database engine::

    Choose Database Engine (mysql, pgsql, sqlite):

.. NOTE::
    Only sqlite is implemented in this wizard at the moment. Other engines
    should work (like mysql and postgresql), but you'd have to modify the
    configuration-file manually to do so.

Sqlite3
.......
Select the sqlite3 db-path::

   'database path: (/var/lib/argux-server/argux.sqlite)')


Initialize database
-------------------
Argux-Server supports a number of database backends::

    $ argux-server_initdb ./argux-server.ini

Add users
---------------
...

Protect default admin account
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
...

