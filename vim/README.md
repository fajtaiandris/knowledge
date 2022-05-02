# 📝 Vim

Konfiguráció
------------
Nvim [vimrc](./init.vim) helye: `~/.config/nvim/init.vim`  

Vágólap
--------
Ha a `vim --help` nem mutatja, hogy `+xterm_clipboard`, akkor ettől jó lesz:

	$ sudo apt-get install vim-gtk

Parancsok
---------
```
gqq                    - sor tördelése
[SHIFT]j               - sor visszaegyesítése
>iB                    - kódblokk belsejének tabulálása
>%                     - kódblokk tabulálása (kurzor a zárójelen)
:'<,'> >               - kódblokk belsejének tabulálása vizuális módban
:w !python - [args]    - Python futtatása mentés nélkül
:%!python -m json.tool - json szépítés
:set tw=80             - tördelés hossz beállítása
:%s/ezt/erre/g         - keresés és csere az egész fájlban
:scriptnames           - betöltött scriptek elérési útvonala
zc                     - fold összecsukása
zo                     - fold kinyitása
za                     - fold toggle
```
