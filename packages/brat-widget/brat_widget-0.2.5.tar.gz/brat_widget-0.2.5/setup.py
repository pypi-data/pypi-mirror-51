from __future__ import print_function
from setuptools import setup, find_packages, Command
from setuptools.command.sdist import sdist
from setuptools.command.build_py import build_py
from setuptools.command.egg_info import egg_info
from subprocess import check_call
import glob
import os
import sys
import platform
from os.path import join as pjoin

here = os.path.dirname(os.path.abspath(__file__))
node_root = pjoin(here, 'js')
is_repo = os.path.exists(pjoin(here, '.git'))
tar_path = pjoin(here, 'brat_widget', '*.tgz')

npm_path = os.pathsep.join([
    pjoin(node_root, 'node_modules', '.bin'),
                os.environ.get('PATH', os.defpath),
])

from distutils import log
log.set_verbosity(log.DEBUG)
log.info('setup.py entered')
log.info('$PATH=%s' % os.environ['PATH'])

LONG_DESCRIPTION = 'Jupiter Widget library for BRAT visualization and annotation functionality.'

def js_prerelease(command, strict=False):
    """decorator for building minified js/css prior to another command"""
    class DecoratedCommand(command):
        def run(self):
            jsdeps = self.distribution.get_command_obj('jsdeps')
            if not is_repo and all(os.path.exists(t) for t in jsdeps.targets):
                # sdist, nothing to do
                command.run(self)
                return

            try:
                self.distribution.run_command('jsdeps')
            except Exception as e:
                missing = [t for t in jsdeps.targets if not os.path.exists(t)]
                if strict or missing:
                    log.warn('rebuilding js and css failed')
                    if missing:
                        log.error('missing files: %s' % missing)
                    raise e
                else:
                    log.warn('rebuilding js and css failed (not a problem)')
                    log.warn(str(e))
            command.run(self)
            update_package_data(self.distribution)
    return DecoratedCommand

def update_package_data(distribution):
    """update package_data to catch changes during setup"""
    build_py = distribution.get_command_obj('build_py')
    # distribution.package_data = find_package_data()
    # re-init build_py options which load package_data
    build_py.finalize_options()


def get_data_files():
    """Get the data files for the package.
    """
    return [
        ('share/jupyter/nbextensions/brat-widget', [
            'brat_widget/static/extension.js',
            'brat_widget/static/index.js',
            'brat_widget/static/index.js.map',
            'brat_widget/static/package.json',
            'brat_widget/static/jupyterlab-plugin.js',
            'brat_widget/static/static/fonts/Astloch-Bold.ttf',
            'brat_widget/static/static/fonts/Liberation_Sans-Regular.svg',
            'brat_widget/static/static/fonts/Liberation_Sans-Regular.ttf',
            'brat_widget/static/static/fonts/PT_Sans-Caption-Web-Regular.svg',
            'brat_widget/static/static/fonts/PT_Sans-Caption-Web-Regular.ttf',
        ]),
        ('share/jupyter/lab/extensions', [
            os.path.relpath(f, '.') for f in glob.glob(tar_path)
        ]),
        ('etc/jupyter/nbconfig/notebook.d' , ['brat-widget.json'])
    ]


class NPM(Command):
    description = 'install package.json dependencies using npm'

    user_options = []

    node_modules = pjoin(node_root, 'node_modules')

    targets = [
        pjoin(here, 'brat_widget', 'static', 'extension.js'),
        pjoin(here, 'brat_widget', 'static', 'index.js'),
        pjoin(here, 'brat_widget', 'static', 'package.json')
    ]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def get_npm_name(self):
        npmName = 'npm';
        if platform.system() == 'Windows':
            npmName = 'npm.cmd';
            
        return npmName;
    
    def has_npm(self):
        npmName = self.get_npm_name();
        try:
            check_call([npmName, '--version'])
            return True
        except:
            return False

    def should_run_npm_install(self):
        node_modules_exists = os.path.exists(self.node_modules)
        return self.has_npm() and not node_modules_exists

    def should_run_npm_pack(self):
        return self.has_npm()

    def run(self):
        has_npm = self.has_npm()
        if not has_npm:
            log.error("`npm` unavailable.  If you're running this command using sudo, make sure `npm` is available to sudo")

        env = os.environ.copy()
        env['PATH'] = npm_path
        npmName = self.get_npm_name();

        if self.should_run_npm_install():
            log.info("Installing build dependencies with npm.  This may take a while...")
            check_call([npmName, 'install'], cwd=node_root, stdout=sys.stdout, stderr=sys.stderr)
            os.utime(self.node_modules, None)

        if self.should_run_npm_pack():
            check_call([npmName, 'pack', node_root], cwd=pjoin(here, 'brat_widget'), stdout=sys.stdout, stderr=sys.stderr)

        files = glob.glob(tar_path)
        self.targets.append(tar_path if not files else files[0])

        for t in self.targets:
            if not os.path.exists(t):
                msg = 'Missing file: %s' % t
                if not has_npm:
                    msg += '\nnpm is required to build a development version of a widget extension'
                raise ValueError(msg)

        self.distribution.data_files = get_data_files()

        # update package data in case this created new files
        update_package_data(self.distribution)

version_ns = {}
with open(pjoin(here, 'brat_widget', '_version.py')) as f:
    exec(f.read(), {}, version_ns)

setup_args = {
    'name': 'brat_widget',
    'version': version_ns['__version__'],
    'description': 'Jupiter Widget library for BRAT visualization and annotation functionality.',
    'long_description': LONG_DESCRIPTION,
    'include_package_data': True,
    'data_files': get_data_files(),
    'install_requires': [
        'ipywidgets>=7.0.0',
    ],
    'packages': find_packages(),
    'zip_safe': False,
    'cmdclass': {
        'build_py': js_prerelease(build_py),
        'egg_info': js_prerelease(egg_info),
        'sdist': js_prerelease(sdist, strict=True),
        'jsdeps': NPM,
    },

    'author': 'Edilmo Palencia',
    'author_email': 'edilmo@mammut.io',
    'url': 'https://github.com/mammut-io/brat-widget',
    'keywords': [
        'ipython',
        'jupyter',
        'widgets',
        'brat',
        'annotation'
        'NLP',
    ],
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Framework :: IPython',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Multimedia :: Graphics',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
}

setup(**setup_args)
