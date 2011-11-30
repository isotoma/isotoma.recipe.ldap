from setuptools import setup, find_packages

version = '0.0.0'

setup(
    name = 'isotoma.recipe.ldap',
    version = version,
    description = "Buildout recipes to configure slapd",
    long_description = open("README.rst").read() + "\n" + \
                       open("CHANGES.txt").read(),
    url = "http://pypi.python.org/pypi/isotoma.recipe.slapd",
    classifiers = [
        "Framework :: Buildout",
        "Framework :: Buildout :: Recipe",
        "Intended Audience :: System Administrators",
        "Operating System :: POSIX",
        "License :: OSI Approved :: Apache Software License",
    ],
    keywords = "ldap buildout slapd",
    author = "Doug Winter",
    author_email = "doug.winter@isotoma.com",
    license="Apache Software License",
    packages = find_packages(exclude=['ez_setup']),
    package_data = {
        '': ['README.rst', 'CHANGES.txt'],
        'isotoma.recipe.ldap': ['slap.conf.j2']
    },
    namespace_packages = ['isotoma', 'isotoma.recipe'],
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'setuptools',
        'zc.buildout',
        'Jinja2',
        'isotoma.recipe.gocaptain',
    ],
    entry_points = {
        "zc.buildout": [
            "default = isotoma.recipe.ldap:Slapd",
        ],
    }
)
