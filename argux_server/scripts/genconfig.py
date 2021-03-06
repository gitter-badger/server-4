"""Initialisation script for Argux-Server Config file."""

import os

import configparser


from argux_server import cli


def main():
    """Main function for Initialisation script."""
    print("")
    print("###########################################")
    print("###                                     ###")
    print("### Argux Server configuration wizard.  ###")
    print("###                                     ###")
    print("###########################################")
    print("")

    config = configparser.ConfigParser()

    config['app:main'] = {}
    config['app:main']['use'] = 'egg:argux-server'

    filename = input('Config file location [./argux-server.ini]: ')
    if filename == '':
        filename = './argux-server.ini'

    # Check if the file exists, if so... ask if it should be overwriten.
    if os.path.exists(filename):
        overwrite = cli.yesno_question('\nFile \''+filename+'\' exists, overwrite?')
        if overwrite is False:
            exit(0)

    secure_cookie = cli.yesno_question(
        'Use secure cookies? (Enforce HTTPS)',
        default='y')
    if secure_cookie:
        config['app:main']['session.secure_cookie'] = 'true'
    else:
        config['app:main']['session.secure_cookie'] = 'false'

    enable_debug = cli.yesno_question(
        'Enable debugging?',
        default='n')
    if enable_debug:
        config['app:main']['rest.pretty_json'] = 'true'
        config['app:main']['pyramid.reload_templates'] = 'true'
        config['app:main']['pyramid.includes'] = \
            'pyramid_debugtoolbar pyramid_tm'
    else:
        config['app:main']['rest.pretty_json'] = 'false'
        config['app:main']['pyramid.reload_templates'] = 'false'

    wsgi = cli.option_question(
        'WSGI Server?',
        ['pserve', 'uwsgi'],
        default='pserve')
    if wsgi == 'pserve':
        config['server:main'] = {}
        config['server:main']['use'] = 'egg:waitress#main'
        config['server:main']['host'] = '0.0.0.0'
        config['server:main']['port'] = '7000'

    if wsgi == 'uwsgi':
        config['uwsgi'] = {}
        config['uwsgi']['http'] = '0.0.0.0:7000'

    database_engine = cli.option_question(
        'Choose Database Engine',
        ['mysql', 'pgsql', 'sqlite'])

    if database_engine == 'sqlite':
        database_path = input(
            'database path: (/var/lib/argux-server/argux.sqlite)')
        if database_path == '':
            database_path = '/var/lib/argux-server/argux.sqlite'

        config['app:main']['sqlalchemy.url'] = \
            'sqlite:///'+database_path

    if database_engine == 'pgsql':
        db_server = input(
            'database server: (localhost) ')
        if db_server == '':
            db_server = 'localhost'

        db_name = input(
            'database name: (argux) ')
        if db_name == '':
            db_name = 'argux'

        db_user = input(
            'database user: ')

        db_password = input(
            'database password: ')

        config['app:main']['sqlalchemy.url'] = \
            'postgresql+psycopg2://'+db_user+':'+db_password+'@'+db_server+'/'+db_name

    with open(filename, 'w') as configfile:
        config.write(configfile)

    return
