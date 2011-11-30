Slapd buildout recipe
=====================

This package provides buildout_recipes for the configuration of slapd_.

We use the system slapd, so this recipe will not install slapd for you.  If you
wish to install slapd, use `zc.recipe.cmmi`_ perhaps.

.. _buildout: http://pypi.python.org/pypi/zc.buildout
.. _slapd: http://www.openldap.org/software/man.cgi?query=slapd
.. _`zc.recipe.cmmi`: http://pypi.python.org/pypi/zc.recipe.cmmi

Mandatory parameters
--------------------

includes
    The schema and config files to load

Optional parameters
-------------------

executable
    The path to the slapd binary.  Defaults to ``/usr/sbin/slapd``.
pidfile
    The location to store the pidfile. Defaults to ``${buildout:run-directory}/PARTNAME.pid``, or ``${buildout:parts-directory}/PARTNAME/slapd.pid``
directory
    The location to store data. Defaults to ``${buildout:directory}/var/PARTNAME``.
user
    The user to run slapd as.  Defaults to ``openldap``.
group
    The group to run slapd as.  Defaults to ``openldap``.
indexes
    A list of indexes to apply to the LDAP instance.
template
    The full path to the configuration file template, if you want to customise further.  Defaults to slapd.conf.j2 template in this package.


