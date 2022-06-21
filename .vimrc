" Display line numbers
:set number
" Highlight line lengths over 80 characters
:set colorcolumn=80
" Turn on auto indentation
:set ai
" Tabkey is interpreted as 4 spaces
set tabstop=4
set shiftwidth=4
set expandtab

" highlight trailing whitespace
:highlight ExtraWhitespace ctermbg=red guibg=red
:match ExtraWhitespace /\s\+$/

" Automatically wrap git commit message body to 72 chars
au FileType gitcommit setlocal tw=72
