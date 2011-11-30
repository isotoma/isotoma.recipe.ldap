# Copyright 2011 Isotoma Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os
import zc.buildout
from jinja2 import Environment, FileSystemLoader, PackageLoader, ChoiceLoader
from isotoma.recipe import gocaptain

try:
    from hashlib import sha1
except ImportError:
    import sha
    def sha1(str):
        return sha.new(str)

def sibpath(filename):
    return os.path.join(os.path.dirname(__file__), filename)


def to_list(buildout_var):
    # Helper for jinja to iterate over buildout lists
    for line in buildout_var.strip().split("\n"):
       if not line.strip():
           continue
       yield line.strip()


class Slapd(object):

    def __init__(self, buildout, name, options):
        self.name = name
        self.options = options
        self.buildout = buildout

        self.outputdir = os.path.join(self.buildout['buildout']['parts-directory'], self.name)
        self.cfgfile = os.path.join(self.outputdir, "slapd.conf")

        if 'run-directory' in self.buildout['buildout']:
            pidfile = os.path.join(self.buildout['buildout']['run-directory'], "%s.pid" % self.name)
        else:
            pidfile = os.path.join(self.buildout['buildout']['directory'], "var", "%s.pid" % self.name)

        self.options.setdefault('pidfile', pidfile)
        self.options.setdefault('directory', os.path.join(self.buildout['buildout']['directory'], 'var', self.name))
        self.options.setdefault('executable', '/usr/sbin/slapd')
        self.options.setdefault('user', 'openldap')
        self.options.setdefault('group', 'openldap')
        self.options.setdefault('template', sibpath("slapd.conf.j2"))
        self.options.setdefault('indexes', 'objectClass eq')

        self.options["__hashes_template"] = sha1(open(self.options["template"]).read()).hexdigest()

    def fill_template(self, template, args):
        dirname, basename = os.path.split(self.options['template'])
        loader = ChoiceLoader([
            FileSystemLoader(dirname),
            PackageLoader('isotoma.recipe.ldap'),
            ])
        e = Environment(loader=loader)
        e.globals = dict(to_list=to_list)
        template = e.get_template(basename)
        return template.render(args)

    def install(self):
        if not os.path.isdir(self.outputdir):
            os.mkdir(self.outputdir)

        # Create the slapd config file
        config = self.fill_template(self.options['template'], self.options)
        open(self.cfgfile, 'w').write(config)
        self.options.created(self.cfgfile)

        # Create a bin/slapd
        self.runscript()

        # Try and create the database directory
        # WE SPECIFICALLY DONT ADD THIS TO THE LIST OF BUILDOUT CREATED FILES!!
        if not os.path.exists(self.options['directory']):
            try:
                os.makedirs(self.options['directory'])
            except OSError:
                print "WARNING: '%s' not created, slapd will not start until it exists and is owned by the correct user" % self.options['directory']


        return self.options.created()

    def runscript(self):
        target = os.path.join(self.buildout["buildout"]["bin-directory"], self.name)
        args = '-f "%s" -u %s -g %s -h ldaps:///' % (self.cfgfile, self.options['user'], self.options['group'])

        gc = gocaptain.Automatic()
        gc.write(open(target, "wt"),
            daemon=self.options['executable'],
            args=args,
            pidfile=self.options['pidfile'],
            name=self.name, 
            description="%s daemon" % self.name)

        os.chmod(target, 0755)
        self.options.created(target)

    def update(self):
        pass

