"""Fabfile for Django-centric Project Setup and Deployment

Author: Ken Chida
Tags: INFO, TODO, FIXME

The following assumptions are made:
 - INFO1: Project name is hardcoded in Django settings
 - INFO2: On remote machines, the relative path of the site root, with respect
   to $HOME, mirrors that of the local machine. If the local site root is moved,
   you will need to setup and deploy on the remote machine again to reflect changes.
 - INFO3: Local virtualenv must be activated before running fab commands.
 - INFO4: Fabfile always invoked from local development machine and has access to a
   fully-built site directory.

*Filesystem Layout*::
-----------------------
SITE_ROOT/
|-- env_PROJECT/      # Populated with virtualenv + pip install
|-- PROJECT_ROOT/     # Project content under source control
|-- cache/            # Filesystem-based cache
|-- db/               # SQLite database goes here for development
|-- log/              # Log files
|-- pid/              # PID files
|-- sock/             # Unix sockets
|-- tmp/              # Temporary files
`-- uploads/          # Site media uploads

PROJECT_ROOT/         # Git or mercurial repo
|-- apps/             # Django apps
|-- etc               # Symlink to a sub-directory in etcs/
|-- etcs/             # Mode-specific configuration (e.g., nginx.conf, supervisord.conf)
|   |-- dev/
|   |-- prod/
|   `-- stage/
|-- lib/              # Libraries that are not in the virtualenv directory.
|-- static/           # Static site media
|-- settings/         # Replaces Django settings.py
|   |-- __init__.py
|   |-- common.py     # Common settings.py content
|   |-- dev.py
|   |-- prod.py
|   `-- stage.py
|-- templates/        # Site-wide Django templates
|-- requirements.txt  # pip install -r requirements.txt
|-- urls.py           # Root URLconf
`-- uwsgi/             # Optional: for uwsgi server
"""

import os
from os.path import abspath, dirname, exists, expanduser, join, relpath

from fabric.contrib.console import confirm
from fabric.api import (abort, cd, env, execute, fastprint, get, hide, hosts, lcd,
                        local, open_shell, output, parallel, path, prefix, prompt,
                        put, puts, reboot, require, roles, run, runs_once, serial,
                        settings, show, sudo, task, warn, with_settings)
try:
    import settings as django_settings
except:
    raise ImportError("Django settings does not exist.")


######################
# Base Configuration #
######################
# User-defined constants
  #TODO: Clean up and consider moving to a shared (w/ django) external config file.
  #INFO: rkhunter omitted as it prompts for config info during apt-get install.

ORIGIN_CLONE_CMD= "hg clone https://kchida@bitbucket.org/kchida/kchida_aws"

RUBY_GEMS = "sass compass"
COM_APT_PKGS = "build-essential binutils-doc autoconf flex bison libreadline-dev " + \
    "zlib1g-dev libxml2-dev libpcre3 libpcre3-dev aptitude checkinstall gdebi " + \
    "libxslt1-dev debconf-utils bash-completion libncurses5-dev libglib2.0-dev " + \
    "python-dev python-setuptools python-software-properties ruby rubygems " + \
    "mercurial git-core gitk subversion tmux byobu libssl-dev openssh-server " + \
    "openssh-client openssl locate htop tree chkrootkit vim strace sysstat unzip " + \
    "pv ntp ntpdate iptables curl dnsutils iotop ncurses-term nmap "

DEV_HOSTS = ('kchida@127.0.0.1:8000', )
DEV_ROLES = ()
DEV_APT_PKGS = COM_APT_PKGS + "sqlite3 "

STAGE_HOSTS = ('ubuntu@ec2-foobar.amazonaws.com', )
STAGE_ROLES = (None,)
STAGE_APT_PKGS = COM_APT_PKGS + ""

PROD_HOSTS = ('ubuntu@23.23.200.199', )
PROD_ROLES = ()
PROD_APT_PKGS = COM_APT_PKGS + ""

SITE_SUBDIRS = ('db', 'cache', 'log', 'pid', 'sock', 'tmp', 'uploads')

# General configuration
env.project_name = django_settings.PROJECT_NAME                              #INFO1
env.project_path = join('~', relpath(abspath(dirname(__file__)),             #INFO2
                                     start=os.environ['HOME']))
env.site_path = dirname(env.project_path)

# Python
env.virtualenv_name = 'env_%(project_name)s' % env
env.virtualenv_path = join(env.site_path, env.virtualenv_name)
#TODO: Figure out how to use 'source' and 'export'
#env.virtualenv_on = 'source %s' % join(env.virtualenv_path, 'bin/activate')
env.virtualenv_python = join(env.virtualenv_path, 'bin/python')
env.virtualenv_pip = join(env.virtualenv_path, 'bin/pip')
env.pip_requirements_path = join(env.project_path, 'requirements.txt')

# Site data (frequently changing)
for subdir in SITE_SUBDIRS:
    env['%s_path' % subdir] = join(env.site_path, subdir)

# Project data (version controlled)
env.etc_path = join(env.project_path, 'etc')
env.etcs_path = join(env.project_path, 'etcs')

#INFO3
try:
    # VIRTUAL_ENV environment variable exists if virtualenv activated.
    shell_env = local('env | grep VIRTUAL_ENV', capture=True)
except:
    if confirm("Local virtualenv not activated! Abort?"):
        abort("Local virtualenv not activated.")

#TODO
#env.database_password = '$(db_password)'
#env.site_media_prefix = "site_media"
#env.admin_media_prefix = "admin_media"
#env.repo_path = '%(path)s/repository' % env
#env.apache_config_path = '/home/newsapps/sites/apache/%(project_name)s' % env
#env.python = 'python2.6'
#env.key_filename = None  # check in ~/.ssh by default? string or list of string of SSH key paths.


######################
# Mode Configuration #
######################
@task
def dev():
    """Configures env and etc symlink for local development.

       This task assumes that the project repository, which includes this fabfile,
       is already set up locally; otherwise, we wouldn't have access to the fabfile
       to begin with.

       Default branch: unstable
    """
    env.mode = 'dev'
    env.hosts = DEV_HOSTS
    env.roles = DEV_ROLES
    unstable()

@task
def stage():
    """Configures env and etc symlink for remote staging.

       Default branch: master
    """
    env.mode = 'stage'
    env.hosts = STAGE_HOSTS
    env.roles = STAGE_ROLES
    env.disable_known_hosts = True    # Set to True for EC2
    master()

@task
def prod():
    """Configures env and etc symlink for production.

       Default branch: master
    """
    env.mode = 'prod'
    env.hosts = PROD_HOSTS
    env.roles = PROD_ROLES
    env.disable_known_hosts = True    # Set to True for EC2
    master()


####################
# Branch Selection #
####################
@task
def master():
    """Work on master/trunk branch."""
    env.branch = 'master'

@task
def unstable():
    """Work on development branch."""
    env.branch = 'unstable'

@task
def branch(branch_name):
    """Work on specified branch."""
    env.branch = branch_name


###########
#  Setup  #
###########
#TODO
#@task
#def create_launch_EC2():
#    pass

@task
def setup():
    """
    Setup a fresh virtualenv, install everything we need, and fire up the database.

    Does NOT perform the functions of deploy().
    Purpose:
     - remote: This script is run locally to setup remote machines.
     - local: For local/dev, it is assumed that the user has cloned the repo into
              the chosen site directory, which gives him access to this fabfile. For
              local setup, the main goal is to do everything after cloning the repo.
    """
    require('branch', provided_by=[master, unstable, branch])
    require('mode', provided_by=[dev, prod, stage])
    if env.mode not in ('dev', 'stage', 'prod'):
        raise ValueError("'env.mode' has invalid value.")

    install_apt_pkgs()
    setup_dotfiles()         # make symlinks
    setup_site_dirs()
    clone_project_repo()     # don't do this for local/dev
    set_etc_symlink
    setup_virtualenv()
    pip_requirements()    # consider setting up chishop
    install_ruby_gems()   # not needed for remote
    #checkout_latest()
    #destroy_database()
    #create_database()
    #load_data()
    #install_apache_conf()
    #deploy_requirements_to_s3()

def install_apt_pkgs():
    """Install Ubuntu Apt packages and install pip"""

    if env.mode is 'dev':
        local('sudo apt-get update && sudo apt-get install -y %s' % DEV_APT_PKGS)
        local('sudo easy_install pip')
    elif env.mode is 'stage':
        sudo('apt-get update && apt-get install -y %s' % STAGE_APT_PKGS)
        sudo('easy_install pip')
    elif env.mode is 'prod':
        sudo('apt-get update && apt-get install -y %s' % PROD_APT_PKGS)
        sudo('easy_install pip')

def setup_dotfiles():
    """Remote Only - Clones dot-file repository to import user settings."""

    if env.mode in ('stage', 'prod'):
        _delete_all('~/dot-files')
        run('hg clone https://bitbucket.org/kchida/dot-files')
        run('ln -sf ~/dot-files/.bashrc ~/.bashrc')
        run('ln -sf ~/dot-files/.profile ~/.profile')
        run('ln -sf ~/dot-files/.inputrc ~/.inputrc')
        run('ln -sf ~/dot-files/.vimrc ~/.vimrc')
        run('ln -sf ~/dot-files/.vim ~/.vim')
    #TODO: Contingency plan if github/bitbucket is not available.
    #TODO: Make this function auto-detect the items that need to be symlinked.


def setup_site_dirs():
    """Setup directories in site root."""

    # Remotes may not have site dir; local is assumed to always have one.   #INFO4
    if env.mode in ('stage', 'prod'):
        _full_mkdir(env.site_path)

    # For local and remote, set up subdirs in the site directory if they don't exist.
    for subdir_name in SITE_SUBDIRS:
        subdir_path = join(env.site_path, subdir_name)
        _full_mkdir(subdir_path)


#TODO: Backup plan if github or bitbucket repo are down.
def clone_project_repo():
    """Remote Only - Clones project repository into workspace."""

    if env.mode in ('stage', 'prod'):
        _delete_all(env.project_path)
        with cd(env.site_path):
            run(ORIGIN_CLONE_CMD)


def set_etc_symlink():
    """Delete etc symlink or directory from project root"""

    _delete_all(env.etc_path)
    if env.mode is 'dev':
        local('ln -s %s %s' % (join(env.etcs_path, env.mode), env.etc_path))
    elif env.mode in ('stage', 'prod'):
        run('ln -s %s %s' % (join(env.etcs_path, env.mode), env.etc_path))

def setup_virtualenv():
    """Pip-installs virtualenv into /usr/..."""

    if env.mode is 'dev':
        local('sudo pip install virtualenv')
        with lcd(env.site_path):
            local('virtualenv %(virtualenv_name)s' % env)
    elif env.mode in ('stage', 'prod'):
        sudo('pip install virtualenv')
        with cd(env.site_path):
            run('virtualenv %(virtualenv_name)s' % env)

def pip_requirements():
    """Install all pip requirements"""

    if env.mode is 'dev':
        local('%(virtualenv_pip)s install -r %(pip_requirements_path)s' % env)
    elif env.mode in ('stage', 'prod'):
        run('%(virtualenv_pip)s install -r %(pip_requirements_path)s' % env)

def install_ruby_gems():
    """Local only - Install ruby packages on dev machine."""

    local('sudo gem install %s' % RUBY_GEMS)
    #TODO: Add 'compass create' and 'compass watch'?


############
#  Deploy  #
############
#####################
# Utility Functions #
#####################
def _delete_all(path):
    """Remove file/dir recursively if it already exists"""

    with settings(hide('warnings', 'stderr'), warn_only=True):
        if env.mode is 'dev':
            local('ls {0} && rm -rf {0}'.format(path))
        elif env.mode in ('stage', 'prod'):
            run('ls {0} && rm -rf {0}'.format(path))

def _full_mkdir(path):
    """mkdir locally or remotely and build all parent dirs as needed"""

    with settings(hide('warnings', 'stderr'), warn_only=True):
        if env.mode is 'dev':
            if not exists(expanduser(path)):
                local('mkdir -p %s' % path)
        elif env.mode in ('stage', 'prod'):
            run("ls {0} || mkdir -p {0}".format(path))

# USE CASES:
#1 setup site (not project cause it's already built) dirs tree (local/remote)
#2 setup virtualenv
#3 clone project git repo (local/remote)
#4 install apt-get libs (local/remote)
#5 install pip requirements (local/remote)
#6 start/restart server (local/remote)
#7 stop server (remote)
#8 syncdb (local/remote)
#9 install debian package of compiled programs

#- deploy to EC2 (remote): 1,2,3,4,5
#-

