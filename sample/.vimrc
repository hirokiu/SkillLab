set expandtab tabstop=4 shiftwidth=4 softtabstop=4
set encoding=utf-8
set fileencoding=utf-8


" ステータスを表示
set laststatus=2
" ステータスラインに文字コードと改行文字を表示する
set statusline=%<%f\ %m%r%h%w%{'['.(&fenc!=''?&fenc:&enc).']['.&ff.']'}%=%l,%c%V%8P

" シンタックス
syntax on

" バックアップファイルは作らない
set nobackup
