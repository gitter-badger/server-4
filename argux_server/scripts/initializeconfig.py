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
        filename= './argux-server.ini'

    # Check if the file exists, if so... ask if it should be overwriten.
    if os.path.exists(filename):
        overwrite = cli.yesno_question('\nFile \''+filename+'\' exists, overwrite?')
        if overwrite == False:
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
        config['app:main']['session.pretty_json'] = 'true'
        config['app:main']['pyramid.reload_templates'] = 'true'
    else:
        config['app:main']['session.pretty_json'] = 'false'
        config['app:main']['pyramid.reload_templates'] = 'false'
        
    wsgi = cli.option_question(
        'WSGI Server?',
        ['pserve','uwsgi'],
        default='pserve')

    with open(filename, 'w') as configfile:
        config.write(configfile)

    return
