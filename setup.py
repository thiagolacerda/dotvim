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
    f.write('" set the folder to install plugins (we do not want it in ~/.vim\n')
    f.write('call vundle#rc(g:dotvim_path."/plugins/")\n')
    f.write('" start vundle!')
    f.write('call vundle#begin()\n')
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

def _install():
    vimrcPath = os.path.expanduser('~/.vimrc')
    if os.path.islink(vimrcPath) or os.path.isfile(vimrcPath):
        raise Exception('~/.vimrc already exists, please remove it before installing dotvim')

    dotvimVimrcPath = '%s/vimrc' % os.getcwd()
    os.symlink(dotvimVimrcPath, vimrcPath)
    print 'dotvim installed!'

def _uninstall():
    vimrcPath = os.path.expanduser('~/.vimrc')
    if os.path.islink(vimrcPath) or os.path.isfile(vimrcPath):
        os.remove(vimrcPath)

    print 'dotvim uninstalled!'

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
    if len(sys.argv) >= 2:
        arg = sys.argv[1]
        if arg == 'uninstall':
            _uninstall()
        elif arg == 'clean':
            _clean()
        elif arg == 'install':
            _setup()
            _install()
        else:
            print 'unknown argument: %s' % arg
    else:
        _setup()
