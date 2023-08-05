import os

try:
    from setuptools import find_packages, setup
except AttributeError:
    from setuptools import find_packages, setup

NAME = 'OASYS1-Elettra-Extensions'
VERSION = '0.0.3.12'
ISRELEASED = True

DESCRIPTION = 'OASYS extensions for Elettra'
README_FILE = os.path.join(os.path.dirname(__file__), 'README.md')
LONG_DESCRIPTION = open(README_FILE).read()
AUTHOR = 'Matteo Altissimo'
AUTHOR_EMAIL = 'matteo.altissimo@elettra.eu'
URL = 'https://github.com/oasys-elettra-kit/OASYS1-ELETTRA-Extensions'
DOWNLOAD_URL = 'https://github.com/oasys-elettra-kit/OASYS1-ELETTRA-Extensions'
LICENSE = 'GPLv3'

KEYWORDS = [
    'raytracing',
    'simulator',
    'oasys1',
]

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: X11 Applications :: Qt',
    'Environment :: Console',
    'Environment :: Plugins',
    'Programming Language :: Python :: 3',
    'Intended Audience :: Science/Research',
]	

SETUP_REQUIRES = (
    'setuptools',
)

INSTALL_REQUIRES = (
    'setuptools',
)

PACKAGES = find_packages(exclude=('*.tests', '*.tests.*', 'tests.*', 'tests'))

PACKAGE_DATA = {
    "orangecontrib.elettra.wofry.widgets.extension":["icons/*.png", "icons/*.jpg"],
    "orangecontrib.elettra.syned.widgets.extension":["icons/*.png", "icons/*.jpg"],
    "orangecontrib.elettra.shadow.widgets.extension":["icons/*.png", "icons/*.jpg", "misc/*.txt"],
    "orangecontrib.elettra.srw.widgets.extension":["icons/*.png", "icons/*.jpg"],
}

NAMESPACE_PACAKGES = ["orangecontrib",
                      "orangecontrib.elettra",
                      "orangecontrib.elettra.wofry",
                      "orangecontrib.elettra.syned",
                      "orangecontrib.elettra.shadow",
                      "orangecontrib.elettra.srw",
                      "orangecontrib.elettra.wofry.widgets",
                      "orangecontrib.elettra.syned.widgets",
                      "orangecontrib.elettra.shadow.widgets",
                      "orangecontrib.elettra.srw.widgets",
                      ]

ENTRY_POINTS = {
    'oasys.addons' : ("WOFRY Elettra Extension = orangecontrib.elettra.wofry",
                      "SYNED Elettra Extension = orangecontrib.elettra.syned",
                      "Shadow Elettra Extension = orangecontrib.elettra.shadow",
                      "SRW Elettra Extension = orangecontrib.elettra.srw",
                      ),
    'oasys.widgets' : (
        "WOFRY Elettra Extension = orangecontrib.elettra.wofry.widgets.extension",
        "SYNED Elettra Extension = orangecontrib.elettra.syned.widgets.extension",
        "Shadow Elettra Extension = orangecontrib.elettra.shadow.widgets.extension",
        "SRW Elettra Extension = orangecontrib.elettra.srw.widgets.extension",
    ),
    'oasys.menus' : ("elettraoasysmenu = orangecontrib.elettra.menu",)
}

if __name__ == '__main__':
    try:
        import PyMca5, PyQt4

        raise NotImplementedError("This version of Elettra Oasys Extensions doesn't work with Oasys1 beta.\nPlease install OASYS1 final release: http://www.elettra.eu/oasys.html")
    except:
        setup(
              name = NAME,
              version = VERSION,
              description = DESCRIPTION,
              long_description = LONG_DESCRIPTION,
              author = AUTHOR,
              author_email = AUTHOR_EMAIL,
              url = URL,
              download_url = DOWNLOAD_URL,
              license = LICENSE,
              keywords = KEYWORDS,
              classifiers = CLASSIFIERS,
              packages = PACKAGES,
              package_data = PACKAGE_DATA,
              #          py_modules = PY_MODULES,
              setup_requires = SETUP_REQUIRES,
              install_requires = INSTALL_REQUIRES,
              #extras_require = EXTRAS_REQUIRE,
              #dependency_links = DEPENDENCY_LINKS,
              entry_points = ENTRY_POINTS,
              namespace_packages=NAMESPACE_PACAKGES,
              include_package_data = True,
              zip_safe = False,
              )
