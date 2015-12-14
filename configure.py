#!/usr/bin/env python

import json
import os
import shutil
import subprocess
import sys

def _setupDirsAndFiles():
    if not os.path.exists('plugins'):
        os.makedirs('plugins')
    if not os.path.exists('.backup'):
        os.makedirs('.backup')
    if not os.path.exists('.tmp'):
        os.makedirs('.tmp')

    open('plugins_vimrc.vim', 'w').close()

def _setupVimrc():
    f = open('vimrc', 'w')

    path = os.getcwd()
    f.write('" dotvim path\nlet g:dotvim_path = "%s"\n' % path)
    f.write('" directory to store backup files\nlet g:dotvim_backupdir = "%s"\n' % (os.getcwd() + '/.backup'))
    f.write('" directory to store temp files\nlet g:dotvim_tmpdir = "%s"\n' % (os.getcwd() + '/.tmp/'))
    f.write('" source the real vimrc file\nexe "source ".g:dotvim_path."/dotvimrc.vim"')
    f.close()

def _getVundle():
    os.chdir('plugins')
    vundle = 'vundle'
    if os.path.exists(vundle):
        os.chdir(vundle)
        subprocess.check_call(['git', 'remote', 'update'])
        subprocess.check_call(['git', 'reset', '--hard', 'origin/master'])
        os.chdir('..')
    else:
        subprocess.check_call(['git', 'clone', 'https://github.com/VundleVim/Vundle.vim.git', vundle])

    os.chdir('..')

def _getVundlePluginsList():
    f = open('vundlepluginslist')
    plugins = json.load(f)
    f.close()
    return plugins

def _applyPatches():
    f = open('patches/patches.info')
    patches = json.load(f)
    f.close()
    rootDir = os.getcwd()
    patchesDir = '%s/patches' % rootDir
    for patch in patches:
        os.chdir(patch['dir'])
        patchFile = '%s/%s' % (patchesDir, patch['file'])
        subprocess.check_call('patch -p1 < %s' % patchFile, shell=True)
        os.chdir(rootDir)

def addVimrcCommands(pluginRepo, commands):
    if len(commands) == 0:
        return

    f = open('plugins_vimrc.vim', 'a')
    f.write('" %s\n' % os.path.basename(pluginRepo).split(".git")[0])
    for command in commands:
        f.write('%s\n' % command)

    f.write('\n')
    f.close()

def _createVundleConfigFile():
    plugins = _getVundlePluginsList()
    f = open('vundleconfig.vim', 'w')
    f.write('" set the runtime path to include Vundle\n')
    f.write('exe "set rtp+=".g:dotvim_path."/plugins/vundle"\n')
    f.write('" set the folder to install plugins (we do not want it in ~/.vim\n')
    f.write('call vundle#rc(g:dotvim_path."/plugins/")\n')
    f.write('" start vundle!')
    f.write('call vundle#begin()\n')
    f.write('\n" List of plugins\n')
    for plugin in plugins:
        f.write('Plugin \'%s\'\n' % plugin['repo'])
        addVimrcCommands(plugin['repo'], plugin['vimrc_cmds'])

    f.write('\ncall vundle#end()\n')
    f.write('\nfiletype plugin indent on\n')
    f.close()


if __name__ == '__main__':
    _setupDirsAndFiles()
    _getVundle()
    _applyPatches()
    _setupVimrc()
    _createVundleConfigFile()
