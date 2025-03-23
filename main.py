import typer
import subprocess

from rich.console import Console

app = typer.Typer()
console = Console()
syncStatus = subprocess.run(['git', 'status', '~/.config'])

@app.command()
def init():
    subprocess.run(['git', 'init', '~/.config'])
    subprocess.run(['touch', '~/.config/.gitignore'])
    subprocess.run(['touch', '~/.config/.dottsrc'])
   console.print(f"Initialized with code: 0")

@app.command()
def sync():
    if():
        # not implemented
    pass
pass

if __name__ == "__main__":
    app()
