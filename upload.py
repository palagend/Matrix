#!/usr/bin/env python3
# from oslo_config import cfg
# CONF = cfg.CONF

import os
import pathlib
import shutil

WORKING_DIR = os.getcwd()
theme_name = 'nagisa'
username = 'palagend'
gitserver = 'github.com'
site_name = 'palagend.github.io'


def init_public():
    public_dir_git = pathlib.Path(os.path.join(WORKING_DIR, 'public', '.git'))
    public_dir = public_dir_git.parent
    clone = (f"git clone https://{gitserver}/{username}"
             f"/{site_name}.git {str(public_dir)}")
    if(not public_dir.exists()):
        if (os.system(clone) != 0):
            raise Exception('Clone failed')
    elif(public_dir.exists() and (not public_dir_git.is_dir())):
        shutil.rmtree(public_dir)
        if (os.system(clone) != 0):
            raise Exception('Clone failed')
    deploy_cmd = f"""
echo "\033[0;32mDeploying updates to {site_name}\033[0m"
hugo -t {theme_name}
cd {str(public_dir)}
git add .
git commit --amend -m "rebuilding site `date`"
git push origin master -f
    """
    if (os.system(deploy_cmd) != 0):
        raise Exception('Deploy failed')


def load_theme():
    theme_dir = pathlib.Path(os.path.join(WORKING_DIR, 'themes', theme_name))
    if(theme_dir.is_dir() and os.listdir(theme_dir)):
        print(f'{theme_name}  has been exist, skip.')
        return
    if(theme_dir.exists()):
        os.rmdir(theme_dir)
    clone = (f"git clone https://{gitserver}/{username}"
             f"/{theme_name}.git {str(theme_dir)}")
    if (os.system(clone) != 0):
        raise Exception('Clone failed')


if __name__ == '__main__':
    load_theme()
    init_public()
