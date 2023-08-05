#!/usr/bin/python3

import sys
if sys.version_info < (3, 2):
    sys.exit('Kazam requires Python 3.2 or newer')

from distutils.core import setup
from DistUtilsExtra.command import *

import re
import glob

try:
    line = open("kazam/version.py").readline()
    VERSION = re.search(r"VERSION = '(.*)'", line).group(1)
except:
    VERSION = "1.0.0"

setup(name='kazam',
      version=VERSION,
      description='A screencasting program created with design in mind.',
      author='David Klasinc, Henry Fuheng Wu',
      author_email='bigwhale@lubica.net, i@quant365.com',
      #long_description=(open('README.md').read() + '\n'),
      #long_description_content_type="text/markdown",
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: X11 Applications :: GTK',
                   'Intended Audience :: End Users/Desktop',
                   'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python',
                   'Topic :: Multimedia :: Graphics :: Capture :: Screen Capture',
                   'Topic :: Multimedia :: Sound/Audio :: Capture/Recording',
                   'Topic :: Multimedia :: Video :: Capture',
                   ],
      keywords='screencast screenshot capture audio sound video recorder kazam',
      url='https://github.com/henrywoo/kazam-screen-recorder',
      license='GPLv3',
      scripts=['bin/kazam'],
      packages=['kazam',
                'kazam.pulseaudio',
                'kazam.backend',
                'kazam.frontend',
                ],
      data_files=[('share/kazam/ui/', glob.glob('data/ui/*ui')),
                  ('share/kazam/sounds/', glob.glob('data/sounds/*ogg')),
                  ('share/icons/gnome/scalable/apps/', glob.glob('data/icons/scalable/*svg')),
                  ],
      cmdclass={'build': build_extra.build_extra,
                'build_i18n':  build_i18n.build_i18n,
                'build_help': build_help.build_help,
                'build_icons': build_icons.build_icons}
      )
