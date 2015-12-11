scriptencoding utf-8
set encoding=utf-8

" Set 256 colors
set t_Co=256

" Use Vim settings, rather then Vi settings (much better!).
" This must be first, because it changes other options as a side effect.
set nocompatible

" Include Vundle config file
exe "source ".g:dotvim_path."/vundleconfig.vim"

" Enable syntax highlight
syntax on

" Set color scheme
"colorscheme gardener

" Set folding
set foldmethod=syntax
set foldlevel=9999999

" Show matching brace
set showmatch

" Show white spaces and tabs
set list
set listchars=tab:»·,trail:·

" Search options
set hlsearch      " highlight search
set incsearch     " incremental search
set ignorecase    " ignore case in search
set smartcase     " except when an uppercase string is searched

" Misc. options
set showcmd       " mostra o comando digitado (eg: digitando :set filetype neste arquivo, mostra filetype=vim)
set wildmenu      " no modo de comando, ao teclar TAB, completa o que foi escrito mostrando as opções em um menu

" Show current line
"set cursorline

" C identation style
set autoindent
set smartindent
set cindent

" Tab stop
set shiftwidth=4
set tabstop=4
set softtabstop=4
set expandtab

" Allow backspacing over everything in insert mode
set backspace=indent,eol,start

" Do not create backups files
set backup

" Keep N lines of command line history
set history=50

" In many terminal emulators the mouse works just fine, thus enable it.
set mouse=a

" Undoing N changes
set undolevels=1000

" Write swap file to disk after each 20 characters
"set updatecount=100

" Write swap file to disk after 6 inactive seconds
"set updatetime=6000

" Scroll off N lines
set scrolloff=4

"" Status line
hi User1 ctermbg=black ctermfg=yellow
"if g:colors_name == "peaksea"
"    hi StatusLine ctermbg=yellow
"endif

highlight clear SignColumn

" Status line of awesome
" Taken from http://github.com/lrvick/dotvim 
set laststatus=2
set statusline=         " clear statusline for vim reload
set statusline+=%f     " filename/path
set statusline+=%y    " filetype
set statusline+=[%{strlen(&fenc)?&fenc:'none'}, "file encoding
set statusline+=%{&ff}] " file format
set statusline+=%h      " help file flag
set statusline+=%1*
set statusline+=%m      " modified flag
set statusline+=%0*
set statusline+=%r      " read only flag
set statusline+=[%{strftime(\"\%d\/\%m\/\%Y\ \%T\",getftime(expand(\"\%\%\")))}]  " Last Modified
set statusline+=%=      " left/right seperator
"set statusline+=Lines:%L\ \|\ Row:%l\ \|\ Col:%c\ \|\ %p%%
set statusline+=C:%c-    " cursor column
set statusline+=L:%l/%L   " cursor line/total lines

" When editing a file, always jump to the last known cursor position.
" Don't do it when the position is invalid or when inside an event handler
" (happens when dropping a file on gvim).
autocmd BufReadPost *
    \ if line("'\"") > 0 && line("'\"") <= line("$") |
        \   exe "normal g`\"" |
        \ endif

"set paste
set pastetoggle=<F11>
set ignorecase
"set background=light
set shell=bash
"set statusline=File:\ %f\ %r%=\|\ Total\ lines:%L\ \|\ Row:%l\ \|\ Col:%c\ \|\ %p%%\ 
set laststatus=2
set formatoptions+=cro

map <F5> :set list! <enter>

" QML syntax as javascript
au BufRead,BufNewFile *.qml set filetype=javascript

" Copy yanked stuff to clipboard
set clipboard=unnamed

" Show right margin at column 120
set textwidth=120
set colorcolumn=+1
hi ColorColumn guibg=#2d2d2d ctermbg=235

if exists("g:dotvim_backupdir")
    exe "set backupdir=".g:dotvim_backupdir
endif

if exists("g:dotvim_tmpdir")
    exe "set directory=".g:dotvim_tmpdir
endif

" Folding
let javaScript_fold=1         " JavaScript
let perl_fold=1               " Perl
let php_folding=1             " PHP
let r_syntax_folding=1        " R
let ruby_fold=1               " Ruby
let sh_fold_enabled=1         " sh
let vimsyn_folding='af'       " Vim script
let xml_syntax_folding=1      " XML

au! FileType python setl nosmartindent

set wildignore+=*/tmp/*,*.so,*.swp,*.zip,.git,*/build/*,*.jpg,*.png,*.jpg,*.ttf,*.sfont,*.path,*.ico,*.svg,*.bmp,*.wav,*.xpm,*.ogg,*.snd,*.gif,*.jng,*.pdf,*.o,*.obj,*.exe,*.so,*.pem,*.props,*.filters,*.tiff,*.edc,*.po,*.sb,*.xib,*.JPG,*.GIF,*.class,*.vtt,*.mp4,*.mp3,*.dat,*.dtd,*.otf,*.mht,*.woff,*.webarchive,*.frag,*.vert,*.dll,*.lib,*.oga,*.jar,ChangeLog*,*.a,*.strings,*.t,*.pl,*.ogv,*.jpeg,*.aaf,*.gzip,*.pyc

" ctags
:nnoremap <silent><Leader><C-]> <C-w><C-]><C-w>T

" Tab navigation.
nnoremap ) :tabnext<CR>
nnoremap ( :tabprev<CR>

" tab move
nnoremap < :tabmove -1<cr>
nnoremap > :tabmove +1<cr>

" source plugins vimrc
exe "source ".g:dotvim_path."/plugins_vimrc.vim"

" set ctags file based on current dir
exe "set tags=".$HOME."/.tags/".fnamemodify(getcwd(), ":t")."/tags"

function! s:GenCTags()
    let currentDir = getcwd()
    let ctagsDestination = $HOME."/.tags/".fnamemodify(getcwd(), ":t")
    if empty(glob(ctagsDestination))
        echo "will create ".ctagsDestination." directory for tags..."
        execute "silent ! mkdir ".ctagsDestination
    endif
    echo "Generating ctags for ".fnamemodify(getcwd(), ":t")." in ".ctagsDestination
    execute "silent ! find ".currentDir." -name \*.h -print -o -name \*.cpp -print | ctags --fields=+l -f ".ctagsDestination."/tags -L - ".currentDir
    echo "Done!"
    execute ':redraw!'
endfunction

com! -nargs=0 GenerateCtags call <SID>GenCTags()

" do not add new line at end of files
set noeol
