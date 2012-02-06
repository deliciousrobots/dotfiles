#!/usr/bin/env python
'''
make_links.py, a script to backup current config files
and replace with symlinks to files in dotfiles folder.

copyright 2010 Stephen A. Goss
'''
from __future__ import print_function

import os, shutil, stat

dotfiles_dir = os.path.dirname(os.path.realpath(__file__))
home_dir = os.path.expanduser("~")

def should_ask(filename):
    return filename.startswith('.bash') or filename.endswith('profile')

print("dotfiles in this folder : %s" % dotfiles_dir)
dotfiles = set(os.listdir(dotfiles_dir))
dotfiles = dotfiles - set(['.git', 'make_links.py', '.gitignore', 'README.md', 'configurations','profiles'])
dotfiles = list(dotfiles)
print("\n".join(dotfiles))
print("target home folder : %s" % home_dir)
backup_folder_path = os.path.join(home_dir, "backups")
if not os.path.isdir(backup_folder_path):
    print("creating backup folder : %s" % backup_folder_path)
    os.mkdir(backup_folder_path)
for filename in dotfiles:
    if should_ask(filename):
        answer = raw_input('Symlink %s ? ' % filename)
        if not answer in ['y', 'Y']:
            continue
    print("processing %s ..." % filename)
    target = os.path.join(home_dir, filename)
    dotfile = os.path.join(dotfiles_dir, filename)
    try:
        statinfo = os.lstat(target)
    except:
        print("file does not exist : %s" % target)
        statinfo = None
    if statinfo:
        if stat.S_ISLNK(statinfo.st_mode):
            print("skipping symlink : %s" % target)
            continue
        else:
            backup = os.path.join(backup_folder_path, filename)
            if stat.S_ISDIR(statinfo.st_mode):
                if not os.path.isdir(backup):
                    print("copying (folder) %s to %s " % (target, backup))
                    shutil.copytree(target, backup)
                print("deleting folder: %s" % target)
                shutil.rmtree(target)
            else:
                if not os.path.isfile(backup):
                    print("copying %s to %s " % (target, backup))
                    shutil.copyfile(target, backup)
                print("delete file : %s" % target)
                os.remove(target)
    print("creating symlink : %s to %s" % (dotfile,target))
    os.symlink(dotfile, target)

print("done!")
