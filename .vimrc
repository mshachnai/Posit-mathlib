" Matan settings for vim

"------Colors -------
"colorscheme default
colo desert

"set t_Co=256

set ffs=unix,dos

"enable syntax processing
syntax enable 
:highlight Comment ctermfg=lightmagenta
:highlight Include ctermfg=magenta
:highlight Define ctermfg=magenta
:highlight Macro ctermfg=magenta
:hi ErrorMsg ctermbg=red ctermfg=cyan
:hi Error ctermbg=none ctermfg=red
:hi IncSearch ctermbg=cyan ctermfg=blue

"change colors of menus (scroll and popup menus)
:hi Special ctermfg=green
:hi Pmenu ctermbg=none ctermfg=brown
:hi PmenuSel cterm=underline ctermbg=none ctermfg=green
:hi Wildmenu ctermbg=none ctermfg=green
:hi StatusLine ctermbg=cyan ctermfg=none
:highlight MatchParen cterm=bold ctermbg=none ctermfg=yellow

set clipboard=unnamed

" ----- UI CONFIG -------
"show line numbers
set number

"disable errorbells
set noerrorbells t_vb=

" load filetype-specific indent files
filetype indent on
set smarttab

"scroll with mouse in vim program
set mouse=a
set go+=a

"show command in botton bar
set showcmd

"show current position
set ruler

" tab is == 4 spaces
set ts=4
set shiftwidth=4
set noexpandtab

"auto indent/smart indent/ wrap lines
set linebreak
set breakindent
"autocmd VimResized * | set columns=90
set colorcolumn=85
set textwidth=85
set wrap
set si
set ai

"highlight current line
set cursorline

"visual autocomplete command menu
set wildmenu

" highligh matching paranthesis
set showmatch

"search like in modern browser
set incsearch

"----- Key mapping-------
"move to beginning/end of line
nnoremap B ^
nnoremap E $

"highlight last inserted txt 
nnoremap gV '[v']

"turn off search highlight (leader key is backslash)
nnoremap <leader><space> :nohlsearch<CR>

"copy with ctrl c (only works in visual mode)
:vmap <C-C> "+y

if has("mousr_sgr")
    set ttymouse=sgr
else
    set ttymouse=xterm2
end

"disables bell
set visualbell

