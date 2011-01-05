from ConfigParser import SafeConfigParser
from django.utils.encoding import smart_unicode, smart_str
from optparse import OptionParser
from subprocess import call
import locale
import os
import random
import shutil
import string
import urllib

SECRET_KEY_CHARS = string.ascii_letters + string.digits

TEMPLATE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'template')
)



class ValidationError(Exception): pass
class BASE_NULL:
    def __str__(self):
        return ''
NULL = BASE_NULL()


def get_default_language():
    l = locale.getlocale()
    if l and len(l) == 2 and l[0]:
        return l[0].replace('_', '-') 
    return 'en' # default...

class WorkingDirectory(object):
    def __init__(self, newcwd):
        self.newcwd  = newcwd
        
    def __enter__(self):
        self.oldcwd = os.getcwd()
        os.chdir(self.newcwd)
    
    def __exit__(self, type, value, traceback):
        os.chdir(self.oldcwd)

class Configuration(object):
    defaults = {
        'database_engine': 'sqlite3',
        'database_host': '',
        'database_port': '',
        'database_user': '',
        'database_password': '',
        'database_name': NULL,
        'outdir': os.getcwd(),
        'cache_backend': 'locmem://',
        'i18n': True,
        'l10n': True,
        'dev': False,
        'languages': [get_default_language()],
        'permissions': False,
        'moderator': False,
        'reversion': False,
    }
    attrs = defaults.keys()
    required = [key for key, value in defaults.items() if value is NULL]
    valid_databases = (
        'sqlite3',
        'mysql',
        'postgres',
    )
    advanced_databases = (
        'mysql',
        'postgres',
    )
    advanced_databases_require = (
        'database_user',
        'database_password',
    )
    
    def __init__(self):
        for attr, default in self.defaults.items():
            setattr(self, attr, default) 
    
    def interactive(self):
        """
        Configure interactively
        """
        raise NotImplementedError
    
    def from_options(self, options):
        """
        Configure from command line options
        """
        for attr in self.attrs:
            value = getattr(options, attr, NULL)
            if value is None:
                value = NULL
            setattr(self, attr, value)
    
    def from_file(self, fpath):
        """
        Configure from a config file
        """
        cfg = SafeConfigParser()
        cfg.read(fpath)
        if not cfg.has_section('cmsquickstart'):
            return
        for attr in self.attrs:
            if cfg.has_option('cmsquickstart', attr):
                setattr(self, attr, cfg.get('cmsquickstart', attr))
    
    def validate(self):
        """
        Validate configuration
        """
        for attr in self.required:
            if getattr(self, attr, NULL) is NULL:
                raise ValidationError(
                    "'%s' is a required configuration variable" % attr
                )
        if self.database_engine in self.advanced_databases:
            for attr in self.advanced_databases_require:
                if getattr(self, attr, NULL) is NULL:
                    raise ValidationError(
                        "'%s' is a required configuration variable for "
                        "database engine '%s'" % (attr, self.database)
                    )

    def as_dict(self):
        return dict([
            (attr, smart_unicode(getattr(self, attr))) for attr in self.attrs
        ])


def gen_secret_key():
    s = ''
    for i in range(40):
        s += random.choice(SECRET_KEY_CHARS)
    return s

def render_template(tplname, data=None):
    if not data:
        data = {}
    fpath = os.path.join(TEMPLATE_DIR, tplname)
    with open(fpath, 'rb') as fobj:
        raw_tpl = smart_unicode(fobj.read())
    output = raw_tpl % data
    s_output = smart_str(output)
    with open(fpath, 'wb') as fobj:
        fobj.write(s_output)
        
def install_base(config):
    print 'Copying files'
    shutil.copytree(TEMPLATE_DIR, config.outdir)
        
def install_buildout(config):
    print 'Setting up buildout'
    bootstrap_path = os.path.join(config.outdir, 'bootstrap.py')
    bootstrap_url = 'http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py'
    urllib.urlretrieve(bootstrap_url, bootstrap_path)
    with WorkingDirectory(config.outdir):
        call(['python', 'bootstrap.py'])
        call(['bin/buildout'])

def install_files(config):
    print 'Setting up files'
    settings_dir = os.path.join(config.outdir, 'py_src', 'project', 'settings')
    data = config.as_dict()
    data['secret_key'] = gen_secret_key()
    data['language_code'] = data['languages'][0]
    if data['reversion']:
        data['reversion_app'] = "'reversion',"
        data['reversion_egg'] = 'django-reversion'
    else:
        data['reversion_app'] = ''
        data['reversion_egg'] = ''
    for name in ('settings', 'i18n', 'cms', 'paths'):
        fpath = os.path.join(settings_dir, 'base_%s.py' % name)
        render_template(fpath, data)
    buildout = os.path.join(config.outdir, 'buildout.cfg')
    render_template(buildout, data)

def install_database(config):
    print 'Setting up database'
    with WorkingDirectory(config.outdir):
        call(['bin/django', 'syncdb', '--all'])
        call(['bin/django', 'migrate', '--fake'])

def install(config):
    installers = [
        install_base,
        install_files,
        install_buildout,
        install_database,
    ]
    for func in installers:
        func(config)

def main():
    parser = OptionParser()
    parser.add_option("-i", "--interactive", dest="interactive",
        help="Run cms-quickstart in interactive mode", action="store_true")
    parser.add_option("-c", "--config-file", dest="config_file",
        help="Use the specified configuration file", action="store_true")
    parser.add_option("-o", "--outdir", dest="outdir",
        default=Configuration.defaults['outdir'],
        help="Initialize the new project to the specified path")
    parser.add_option("-e", "--database-engine", dest="database_engine",
        default=Configuration.defaults['database_engine'],
        help="Database engine to use, choices are: mysql, postgres, sqlite3",
        choices=["mysql", "postgres", "sqlite3"])
    parser.add_option("-u", "--database-user", dest="database_user",
        help="Database user to use, not required for sqlite3.")
    parser.add_option("-p", "--database-password", dest="database_password",
        help="Database password to use, not required for sqlite3.")
    parser.add_option("-s", "--database-host", dest="database_host",
        help="Database host to use, not required for sqlite3.",
        default=Configuration.defaults['database_host'])
    parser.add_option("-n", "--database-name", dest="database_name",
        help="Database name to use.")
    parser.add_option('--database-port', dest="database_port",
        help="Port to use for database",
        default=Configuration.defaults['database_port'])
    parser.add_option("--use-moderator", dest="moderator",
        help="Use CMS_MODERATOR", action="store_true",
        default=Configuration.defaults['moderator'])
    parser.add_option("--use-reversion", dest="reversion",
        help="Use reversion", action="store_true",
        default=Configuration.defaults['reversion'])
    parser.add_option("--use-permissions", dest="permissions",
        help="Use CMS_PERMISSIONS", action="store_true",
        default=Configuration.defaults['permissions'])
    parser.add_option("-l", "--language", dest="languages",
        help="Language to use (can be used multiple times", action="append",
        default=Configuration.defaults['languages'])
    parser.add_option("--cache-backend", dest="cache_backend",
        default=Configuration.defaults['cache_backend'],
        help="Cache backend to use")
    parser.add_option("-d", "--dev", dest="dev", action="store_true",
        help="Enable development mode", default=Configuration.defaults['dev'])
    parser.add_option("--no-i18n", dest="i18n", action="store_false",
        help="Disable i18n", default=Configuration.defaults['i18n'])
    parser.add_option("--no-l10n", dest="l10n", action="store_false",
        help="Disable l10n", default=Configuration.defaults['l10n'])
    
    options = parser.parse_args()[0]
    
    config = Configuration()
    if options.interactive:
        config.interactive()
    elif options.config_file:
        config.from_file(options.config_file)
    else:
        config.from_options(options)
    config.validate()
    install(config)
    print "Now head over to your new project and enter 'bin/django runserver' to start your server!"

if __name__ == '__main__':
    main()