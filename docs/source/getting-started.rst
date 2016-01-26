===============
Getting Started
===============

Generate a config file
-------------------
Use `initialize_argux-server_config` to generate a configuration-file.
This command asks you a number of questions about the preferred
configuration before generating the configuration-file::

   $ argux-server_genconfig

   ###########################################
   ###                                     ###
   ### Argux Server configuration wizard.  ###
   ###                                     ###
   ###########################################

The first question asks for the config-file location::

   Config file location[./argux-server.ini]: 


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

