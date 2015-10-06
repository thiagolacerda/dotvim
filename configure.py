#!/usr/bin/env python

import json
import os
import shutil
import subprocess

def _setupDirs():
    if not os.path.exists('plugins'):
        os.makedirs('plugins')
    if not os.path.exists('.backup'):
        os.makedirs('.backup')
    if not os.path.exists('.tmp'):
        os.makedirs('.tmp')


def _setupVimrc():
    f = open('vimrc', 'w')

    path = os.getcwd()
    f.write('" dotvim path\nlet g:dotvim_path = "%s"\n' % path)
    f.write('" directory to store backup files\nlet g:dotvim_backupdir = "%s"\n' % (os.getcwd() + '/.backup'))
    f.write('" directory to store temp files\nlet g:dotvim_tmpdir = "%s"\n' % (os.getcwd() + '/.tmp/'))
    f.write('" source the real vimrc file\nexe "source ".g:dotvim_path."/dotvimrc.vim"')
    f.close()


def _getPluginRepos():
    f = open('pluginsrepos')
    plugins = json.load(f)
    f.close()
    return plugins


def _cloneExuberantCTags():
    subprocess.check_call(['git', 'clone', 'https://github.com/mortice/exuberant-ctags.git'])


def _clonePlugins():
    plugins = _getPluginRepos()
    os.chdir('plugins')
    for plugin in plugins:
        command = 'git clone %s' % plugin['repo']
        subprocess.check_call(['git', 'clone', plugin['repo']])


if __name__ == '__main__':
    _setupDirs()
    _setupVimrc()
    _cloneExuberantCTags()
    _clonePlugins()
