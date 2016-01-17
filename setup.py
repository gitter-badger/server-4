"""ArguxServer setup script."""

import os

from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, 'README.md')) as f:
    README = f.read()
with open(os.path.join(HERE, 'CHANGES.txt')) as f:
    CHANGES = f.read()

REQUIRES = [
    'pyramid == 1.5.7',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'python-dateutil == 2.4',
    'bcrypt == 2.0',
    ]

setup(name='argux-server',
      version='0.0.1',
      description='argux-server',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Stephan Arts',
      author_email='stephan@xfce.org',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=REQUIRES,
      tests_require=REQUIRES,
      test_suite="tests",
      entry_points="""\
      [paste.app_factory]
      main = arguxserver:main
      [console_scripts]
      initialise_argux-server_db = arguxserver.scripts.initializedb:main
      """,
      )
