"""Initialisation script for Argux-Server Config file."""


def main():
    """Main function for Initialisation script."""
    print("")
    print("###########################################")
    print("###                                     ###")
    print("### Argux Server configuration wizard.  ###")
    print("###                                     ###")
    print("###########################################")
    print("")

    filename = input('Config file location [./argux-server.ini]: ')
    if filename == '':
        filename= './argux-server.ini'
    print(filename)

    return
