# brag

```
usage: brag [-h] {new,n,list,l,edit,e,search,s,data_dir,dd} ...

Brag about work you've done today.

positional arguments:
  {new,n,list,l,edit,e,search,s,data_dir,dd}
    new (n)             create a new note
    list (l)            list selected note(s) content
    edit (e)            edit selected note
    search (s)          search notes with text
    data_dir (dd)       open directory where notes are stored

optional arguments:
  -h, --help            show this help message and exit
```

### Installation

Requirements:
* python 3.x
 * fzf
* grep
* python3-venv (for dev)

To install globally run `pip3 install .` in project's root folder.  
Script `install.sh` can be used to install in a separate virtual env instead.
