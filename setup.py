from setuptools import setup
from setuputils import TestCoverageRatchetCommand, VerifyVersionCommand

version = '0.5.0'
setup(
    name='sqlalchemy-vertica-python',
    version=version,
    description='Vertica dialect for sqlalchemy using vertica_python',
    long_description=open("README.rst").read(),
    license="MIT",
    url='https://github.com/LocusEnergy/sqlalchemy-vertica-python',
    download_url = 'https://github.com/LocusEnergy/sqlalchemy-vertica-python/tarball/{}'.format(version),
    author='Locus Energy',
    author_email='dbio@locusenergy.com',
    packages=[
        'sqla_vertica_python',
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
