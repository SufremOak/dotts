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

# Configure logging
fmt = jsonlogger.JsonFormatter(
    "%(name)s %(asctime)s %(levelname)s %(filename)s %(lineno)s %(process)d %(message)s",
    rename_fields={"levelname": "severity", "asctime": "timestamp"},
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(fmt)
logger.addHandler(handler)

DEPENDENCIES_FILE = os.path.expanduser('~/.config/.dependencies')

def run_command(command):
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode().strip()
    except subprocess.CalledProcessError as e:
        logger.error(f"Command '{' '.join(command)}' failed with error: {e.stderr.decode().strip()}")
        sys.exit(1)

def checkGitInstallation():
    run_command(['git', '--version'])
    print(f"[green]Git is installed.[/green]")

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, complex):
            return [obj.real, obj.imag]
        return json.JSONEncoder.default(self, obj)

def AppInit():
    print(f"[green]Reading from {os.path.expanduser('~/.config/.dottsrc')}[/green]")
    with open('~/.config/.dottsrc', 'r') as f:
        json.loads(f.read())

@app.command(help="Initialize the dotfiles manager and create necessary files.")
def init():
    run_command(['git', 'init', '~/.config'])
    run_command(['touch', '~/.config/.gitignore'])
    run_command(['touch', '~/.config/.dottsrc'])
    print(f"[green]Initialized with code: 0[/green]")

@app.command(help="Synchronize the dotfiles with the remote repository.")
def sync():
    status = run_command(['git', 'status', '--porcelain'])
    if status:
        run_command(['git', 'pull', '~/.config'])
    else:
        print(f"[green]Up to date![/green]")

@app.command(help="Show the current status of the git repository.")
def status():
    # Get the current branch name
    branch = run_command(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
    print(f"[green]Current branch:[/green] {branch}")

    # Check for uncommitted changes
    changes = run_command(['git', 'status', '--porcelain'])
    if changes:
        print("[yellow]You have uncommitted changes:[/yellow]")
        for change in changes.splitlines():
            print(f"  - {change}")
    else:
        print("[green]No uncommitted changes.[/green]")

    # Check if the branch is ahead or behind the remote
    remote_status = run_command(['git', 'rev-list', '--left-only', '--count', f'origin/{branch}...{branch}'])
    ahead, behind = map(int, remote_status.split())
    if ahead > 0:
        print(f"[green]Your branch is ahead by {ahead} commit(s).[/green]")
    if behind > 0:
        print(f"[red]Your branch is behind by {behind} commit(s).[/red]")

@app.command(help="Add a specific file or directory to the git repository.")
def dependency(dep: str):
    run_command(['git', 'add', dep])
    print(f"Added {dep}")
    run_command(['git', 'commit', '-m', f"Added {dep}"])
    print(f"Committed {dep}")
    run_command(['git', 'push', '~/.config'])
    print(f"Pushed {dep}")
    print(f"Done!")

@app.command(help="Manage dependencies for your dotfiles. Actions: add, mod, list.")
def dependencies(action: str, name: str = None, install_via_pm: str = None):
    if action == "add":
        if not name or not install_via_pm:
            print("[bold red]Error: You must provide a name and installation method.[/bold red]")
            return
        add_dependency(name, install_via_pm)
    elif action == "mod":
        if not name or not install_via_pm:
            print("[bold red]Error: You must provide a name and formulae to modify.[/bold red]")
            return
        modify_dependency(name, install_via_pm)
    elif action == "list":
        list_dependencies()
    else:
        print("[bold red]Error: Invalid action. Use 'add', 'mod', or 'list'.[/bold red]")

def add_dependency(name: str, install_via_pm: str):
    dependencies = load_dependencies()
    dependencies[name] = install_via_pm
    save_dependencies(dependencies)
    print(f"[green]Added dependency: {name} with installation method: {install_via_pm}[/green]")

def modify_dependency(name: str, install_via_pm: str):
    dependencies = load_dependencies()
    if name in dependencies:
        dependencies[name] = install_via_pm
        save_dependencies(dependencies)
        print(f"[green]Modified dependency: {name} to installation method: {install_via_pm}[/green]")
    else:
        print(f"[bold red]Error: Dependency '{name}' not found.[/bold red]")

def list_dependencies():
    dependencies = load_dependencies()
    if dependencies:
        print("[green]Current dependencies:[/green]")
        for name, method in dependencies.items():
            print(f"- {name}: {method}")
    else:
        print("[yellow]No dependencies found.[/yellow]")

def load_dependencies():
    if os.path.exists(DEPENDENCIES_FILE):
        with open(DEPENDENCIES_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_dependencies(dependencies):
    with open(DEPENDENCIES_FILE, 'w') as f:
        json.dump(dependencies, f, indent=4)

@app.command(help="Modify a configuration via formulae.")
def formulae(name: str, formula: str):
    # Example: Run a specific formula script based on the name
    if name == "nvim":
        if formula == "plugs:lazyvim":
            run_command(['git', 'clone', 'https://github.com/username/LazyVim.git', '~/.config/nvim'])
            print(f"[green]Formulae applied for {name}: {formula}[/green]")
            # Additional commands to set up LazyVim can be added here
        else:
            print(f"[bold red]Error: Unknown formula '{formula}' for {name}.[/bold red]")
    else:
        print(f"[bold red]Error: Unknown configuration '{name}'.[/bold red]")

if __name__ == "__main__":
    app()
