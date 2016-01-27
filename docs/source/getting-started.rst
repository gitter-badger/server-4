===============
Getting Started
===============

Generate a config file
----------------------
Use `initialize_argux-server_config` to generate a configuration-file.
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

Database Configuration
~~~~~~~~~~~~~~~~~~~~~~



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

