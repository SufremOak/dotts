import typer
import subprocess
import json
import sys
import logging
import os

from rich.console import Console
from io import StringIO
from pythonjsonlogger import jsonlogger
from rich import print

app = typer.Typer()
console = Console()
syncStatus = subprocess.run(['git', 'status', '~/.config'])
# logger = logging.getLogger(__name__)
fmt = jsonlogger.JsonFormatter(
    "%(name)s %(asctime)s %(levelname)s %(filename)s %(lineno)s %(process)d %(message)s",
    rename_fields={"levelname": "severity", "asctime": "timestamp"},
)

# stdoutHandler.setFormatter(fmt)
# errHandler.setFormatter(fmt)

def checkGitInstallation():
    def check(exit):
        subprocess.run(['git', '--version'])
        return exit
    if(check.exit == "0"):
        exit(0)
    else:
        print(f"[bold red]Git is not installed, install git and try again[/bold red]")
        exit(1)
    
class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, complex):
            return [obj.real, obj.imag]
        return json.JSONEncoder.default(self, obj)

def AppInit():
    print(f"[green]Reading from {os.path.expanduser('~/.config/.dottsrc')}[/green]")
    json.loads(open('~/.config/.dottsrc', 'r').read())

@app.command()
def init():
    subprocess.run(['git', 'init', '~/.config'])
    subprocess.run(['touch', '~/.config/.gitignore'])
    subprocess.run(['touch', '~/.config/.dottsrc'])
    print(f"[green]Initialized with code: 0[/green]")

@app.command()
def sync():
    if(syncStatus == "pendent"):
        subprocess.run(['git', 'pull', '~/.config'])
    else:
        print(f"[green]Up to date![/green]")

@app.command()
def status():
    print(f"{syncStatus}")

@app.command()
def dependency(dep: str):
    subprocess.run(['git', 'add', dep])
    print(f"Added {dep}")
    subprocess.run(['git', 'commit', '-m', f"Added {dep}"])
    print(f"Committed {dep}")
    subprocess.run(['git', 'push', '~/.config'])
    print(f"Pushed {dep}")
    print(f"Done!")
    exit(0)
if __name__ == "__main__":
    app()
