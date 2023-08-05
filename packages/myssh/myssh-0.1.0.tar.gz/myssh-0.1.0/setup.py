
from setuptools import setup
from setuptools.command.install import install
from setuptools.command.develop import develop


class InstallWrapper(install):


    def run(self):
        install.run(self)
        from alembic.config import Config
        from alembic import command
        import os
        main_link = os.path.dirname(os.path.abspath(__file__))
        alembic_cfg = Config("{}/alembic.ini".format(main_link))
        command.upgrade(alembic_cfg, "head")

class InstallWrapperD(develop):
    
    def run(self):
        develop.run(self)
        from alembic.config import Config
        from alembic import command
        import os
        main_link = os.path.dirname(os.path.abspath(__file__))
        alembic_cfg = Config("{}/alembic.ini".format(main_link))
        command.upgrade(alembic_cfg, "head")
setup(
    name='myssh',
    version='0.1.0',
    author='Ahmed Khatab',
    author_email='ahmmkhh@gmail.com',
    packages=['ssh_app'],
    scripts=['bin/con','bin/sshentry'],
    url='http://pypi.python.org/pypi/myssh/',
    license='LICENSE.txt',
    description='Useful ssh acess tool.',
    long_description=open('README.txt').read(),
    install_requires=['alembic==1.0.11','SQLAlchemy==1.3.6',
		      'argcomplete==1.10.0'
   
    ],
    cmdclass={'install': InstallWrapper,
            'develop':InstallWrapperD}
)
