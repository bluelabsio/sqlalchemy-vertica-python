from decimal import Decimal
from distutils.cmd import Command
from setuptools import setup
from setuptools.command.install import install
import os.path
import sys


__version__ = '0.5.10'


# From https://circleci.com/blog/continuously-deploying-python-packages-to-pypi-with-circleci/
class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        from setup import __version__
        tag = os.getenv('CIRCLE_TAG')
        tag_formatted_version = 'v{}'.format(__version__)

        if tag != tag_formatted_version:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, __version__
            )
            sys.exit(info)


class CoverageRatchetCommand(Command):
    description = 'Run coverage ratchet'
    user_options = []  # type: ignore

    def finalize_options(self) -> None:
        pass

    def run(self) -> None:
        """Run command."""
        import xml.etree.ElementTree as ET

        tree = ET.parse(self.coverage_source_file)
        new_coverage = Decimal(tree.getroot().attrib["line-rate"]) * 100

        if not os.path.exists(self.coverage_file):
            with open(self.coverage_file, 'w') as f:
                f.write('0')

        with open(self.coverage_file, 'r') as f:
            high_water_mark = Decimal(f.read())

        if new_coverage < high_water_mark:
            raise Exception(
                "{} coverage used to be {}; "
                "down to {}%.  Fix by viewing '{}'".format(self.type_of_coverage,
                                                           high_water_mark,
                                                           new_coverage,
                                                           self.coverage_url))
        elif new_coverage > high_water_mark:
            with open(self.coverage_file, 'w') as f:
                f.write(str(new_coverage))
            print("Just ratcheted coverage up to {}%".format(new_coverage))
        else:
            print("Code coverage steady at {}%".format(new_coverage))


class TestCoverageRatchetCommand(CoverageRatchetCommand):
    def initialize_options(self) -> None:
        """Set default values for options."""
        self.type_of_coverage = 'Test'
        self.coverage_url = 'cover/index.html'
        self.coverage_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'metrics',
            'coverage_high_water_mark'
        )
        self.coverage_source_file = "coverage.xml"


setup(
    name='sqlalchemy-vertica-python',
    version=__version__,
    description='Vertica dialect for sqlalchemy using vertica_python',
    long_description=open("README.rst").read(),
    license="MIT",
    url='https://github.com/bluelabsio/sqlalchemy-vertica-python',
    download_url = 'https://github.com/bluelabsio/sqlalchemy-vertica-python/tarball/{}'.format(__version__),
    author='James Casbon, Luke Emery-Fertitta',
    maintainer='Vince Broz',
    maintainer_email='opensource@bluelabs.com',
    packages=[
        'sqla_vertica_python',
    ],
    keywords=['sqlalchemy', 'vertica', 'python'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    entry_points="""
    [sqlalchemy.dialects]
    vertica.vertica_python = sqla_vertica_python.vertica_python:VerticaDialect
    """,
    install_requires=[
        'vertica_python'
    ],
    cmdclass={
        'coverage_ratchet': TestCoverageRatchetCommand,
        'verify': VerifyVersionCommand,
    },
)
