# Dotts, the dotfiles manager from the future
Manage your `dotfiles` in diferent machines with ease and speed

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![PyPi](https://img.shields.io/badge/pypi-%23ececec.svg?style=for-the-badge&logo=pypi&logoColor=1f73b7)

## Features
- dotfiles management via `git`
- .dependencies, the dependencies of your `dotfiles`
- analyze and merge changes
- cool cli looks

## Usage
```bash
# initialize dotts
$ dotts init --recursive --path="~/.config"
INFO: Creating file: '~/.config/.dottsrc'
INFO: Creating file '~/.config/.dependencies'
INFO: Creating file '~/.config/.dotts.list.sh'
INFO: Modifing file '~/.config/.dotts.list.sh' with "chmod +x $FILE"
INFO: Initializing git with "git init $DOTTS_PATH"
INFO: Done.
NOTE: You will need to manually add a remote repository for your dotfiles.
# add dotfiles via dotdependencies
$ dotts dependencies add nvim --install-via-pm="apt"
INFO: Running "yes | sudo apt install neovim"
# This will install neovim via apt
INFO: Scanning for changes in $DOTTS_PATH...
INFO: Found new configuration for program 'nvim'
INFO: Adding nvim:'~/.config/nvim' to ".dependencies"
INFO: Done.
# modify a configuration via formulae
$ dotts dependencies mod nvim --formulae="plugs:lazyvim"
RUN: Formulae Plugins/LazyVim.sh
!git clone $LAZYVIM_REPO $DOTTS_PATH/nvim [done]
!rm -rf $DOTTS_PATH/nvim/.git [done]
INFO: Writing changes to .dependencies [done]
```

> [!NOTE]
> The formulae feature is under development, and with limited support, bugs and anything can be reported as a issue

## Dependencies
- [typer](https://typer.tiangolo.com/)
- [rich](https://github.com/Textualize/rich)
- [pyinstaller](https://pyinstaller.org/en/stable/)

##

Made with ❤ by SufremOak

[![Upload Python Package](https://github.com/SufremOak/dotts/actions/workflows/python-publish.yml/badge.svg)](https://github.com/SufremOak/dotts/actions/workflows/python-publish.yml)
