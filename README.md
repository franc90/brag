# brag

```
usage: brag [-h] {new,n,list,l,edit,e,data_dir,dd} ...

Brag about work you've done today.

positional arguments:
  {new,n,list,l,edit,e,data_dir,dd}
    new (n)             create a new note
    list (l)            list selected note(s) content
    edit (e)            edit selected note
    data_dir (dd)       open directory where notes are stored

optional arguments:
  -h, --help            show this help message and exit
```

### Installation

Requirements:
* python 3.x
* fzf on path  

To install run `./install.sh`. Or if you want to install globally, then in `brag` directory run `pip3 install .`
