"""Initialisation script for Argux DB."""
import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from pyramid.scripts.common import parse_vars

from ..models import (
    DB_SESSION,
    BASE,
    ItemName,
    ItemType,
    ItemCategory,
    TriggerSeverity
)


def usage(argv):
    """Print usage string."""

    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main():
    """Main function for Initialisation script."""

    if len(sys.argv) < 2:
        usage(sys.argv)
    config_uri = sys.argv[1]
    options = parse_vars(sys.argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DB_SESSION.configure(bind=engine)
    BASE.metadata.create_all(engine)
    with transaction.manager:
        model = ItemType(name='int', description='Integer field')
        DB_SESSION.add(model)
        model = ItemType(name='float', description='Floating point')
        DB_SESSION.add(model)
        model = ItemType(name='text', description='Text')
        DB_SESSION.add(model)

        model = TriggerSeverity(level=1, key="info", name="Information")
        DB_SESSION.add(model)
        model = TriggerSeverity(level=2, key="warn", name="Warning")
        DB_SESSION.add(model)
        model = TriggerSeverity(level=3, key="crit", name="Critical")
        DB_SESSION.add(model)
