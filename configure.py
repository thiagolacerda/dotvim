#!/usr/bin/env python

import json
import os
import shutil
import subprocess
import sys

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

def _cloneOrUpdatePlugins(update):
    plugins = _getPluginRepos()
    os.chdir('plugins')
    for plugin in plugins:
        try:
            if update and os.path.exists(plugin['name']):
                subprocess.check_call(['git', 'remote', 'update'])
                subprocess.check_call(['git', 'reset', '--hard', 'origin/master'])
            else:
                subprocess.check_call(['git', 'clone', plugin['repo'], plugin['name']])
        except:
            pass


if __name__ == '__main__':
    update = False
    if len(sys.argv) > 1 and sys.argv[1] == '--update':
        update = True

    _setupDirs()
    _setupVimrc()
    _cloneOrUpdatePlugins(update)
