#!/usr/bin/env python

import argparse
import json
import os
import shutil
import subprocess
import sys

is_neovim = True

def _setupDirsAndFiles():
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

def _addVimrcPluginCommands(plugins):
    f = open('plugins_vimrc.vim', 'w')
    for plugin in plugins:
        commands = plugin['vimrc_cmds']
        if len(commands) == 0:
            continue

        f.write('" %s\n' % os.path.basename(plugin['repo']))
        for command in commands:
            f.write('%s\n' % command)

        f.write('\n')

    f.close()

def _createVundleConfigFile(plugins):
    f = open('vundleconfig.vim', 'w')
    f.write('" set the runtime path to include Vundle\n')
    f.write('exe "set rtp+=".g:dotvim_path."/plugins/vundle"\n')
    f.write('" start vundle, passing the folder to install plugins (we do not want it in ~/.vim)!\n')
    f.write('call vundle#begin(g:dotvim_path."/plugins/")\n')
    f.write('\n" List of plugins\n')
    for plugin in plugins:
        f.write('Plugin \'%s\'\n' % plugin['repo'])

    f.write('\ncall vundle#end()\n')
    f.write('\nfiletype plugin indent on\n')
    f.close()

def _generateVundleConfigArtifacts():
    plugins = _getVundlePluginsList()

    _createVundleConfigFile(plugins)
    _addVimrcPluginCommands(plugins)

def _setup():
    _setupDirsAndFiles()
    _getVundle()
    _applyPatches()
    _setupVimrc()
    _generateVundleConfigArtifacts()

def _confFile():
    return '~/.config/nvim/init.vim' if is_neovim else '~/.vimrc'

def _install():
    confFilePath = os.path.expanduser(_confFile())
    if os.path.islink(confFilePath) or os.path.isfile(confFilePath):
        raise Exception('%s already exists, please remove it before installing dotvim' % confFile)

    if is_neovim and not os.path.exists(os.path.dirname(confFilePath)):
        os.makedirs(os.path.dirname(confFilePath))

    dotvimVimrcPath = '%s/vimrc' % os.getcwd()
    os.symlink(dotvimVimrcPath, confFilePath)
    print 'dotvim installed!'

def _uninstall():
    confFilePath = os.path.expanduser(_confFile())
    if os.path.islink(confFilePath) and os.path.realpath(confFilePath) == '%s/vimrc' % os.getcwd():
        os.remove(confFilePath)
        print 'dotvim uninstalled!'
    else:
        raise Exception('Could not uninstall dotvim. Either because it is not installed or %s does not point to dotvim configuration' % confFilePath)

def _clean():
    _uninstall()
    if (os.path.exists('plugins')):
        shutil.rmtree('plugins')
    if (os.path.exists('vundleconfig.vim')):
        os.remove('vundleconfig.vim')
    if (os.path.exists('plugins_vimrc.vim')):
        os.remove('plugins_vimrc.vim')
    if (os.path.exists('vimrc')):
        os.remove('vimrc')

    print 'dotvim cleaned!'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--uninstall", help="uninstall dotvim", action="store_true")
    parser.add_argument("--clean", help="uninstall dot vim and clean everything", action="store_true")
    parser.add_argument("--setup", help="setup dotvim structure and update plugins (default action)", action="store_true")
    parser.add_argument("--install", help="setup dotvim structure, update plugins and install (includes --setup)", action="store_true")
    parser.add_argument("-v", help="setup for vim (neovim used by default)", action="store_true")
    args = parser.parse_args()

    if args.v:
        is_neovim = False;

    if args.install:
        _setup()
        _install()
    elif args.uninstall:
        _uninstall()
    elif args.clean:
        _clean()
    else:
        _setup()
