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

@app.command(help="Install a plugin for a specific application.")
def install_plugin(app_name: str, plugin_name: str):
    if app_name == "nvim":
        # Example: Install a Neovim plugin using a package manager
        run_command(['git', 'clone', f'https://github.com/{plugin_name}.git', '~/.config/nvim/plugins/{plugin_name}'])
        print(f"[green]Installed plugin '{plugin_name}' for {app_name}.[/green]")
    else:
        print(f"[bold red]Error: Unsupported application '{app_name}'.[/bold red]")

@app.command(help="List installed plugins for a specific application.")
def list_plugins(app_name: str):
    if app_name == "nvim":
        plugins_dir = os.path.expanduser('~/.config/nvim/plugins/')
        if os.path.exists(plugins_dir):
            plugins = os.listdir(plugins_dir)
            if plugins:
                print(f"[green]Installed plugins for {app_name}:[/green]")
                for plugin in plugins:
                    print(f"- {plugin}")
            else:
                print("[yellow]No plugins installed.[/yellow]")
        else:
            print(f"[bold red]Error: No plugins directory found for {app_name}.[/bold red]")
    else:
        print(f"[bold red]Error: Unsupported application '{app_name}'.[/bold red]")

@app.command(help="Modify a configuration via formulae.")
def formulae(name: str, formula: str):
    if name == "nvim":
        if formula == "plugs:lazyvim":
            run_command(['git', 'clone', 'https://github.com/username/LazyVim.git', '~/.config/nvim'])
            print(f"[green]Formulae applied for {name}: {formula}[/green]")
        else:
            print(f"[bold red]Error: Unknown formula '{formula}' for {name}.[/bold red]")
    else:
        print(f"[bold red]Error: Unknown configuration '{name}'.[/bold red]")

@app.command(help="Manage plugins for your dotfiles. Actions: add, remove, list.")
def plugins(action: str, name: str = None, install_via_pm: str = None):
    if action == "add":
        if not name or not install_via_pm:
            print("[bold red]Error: You must provide a name and installation method.[/bold red]")
            return
        add_plugin(name, install_via_pm)
    elif action == "remove":
        if not name:
            print("[bold red]Error: You must provide a name of the plugin to remove.[/bold red]")
            return
        remove_plugin(name)
    elif action == "list":
        list_plugins()
    else:
        print("[bold red]Error: Invalid action. Use 'add', 'remove', or 'list'.[/bold red]")

def add_plugin(name: str, install_via_pm: str):
    plugins = load_plugins()
    plugins[name] = install_via_pm
    save_plugins(plugins)
    print(f"[green]Added plugin: {name} with installation method: {install_via_pm}[/green]")

def remove_plugin(name: str):
    plugins = load_plugins()
    if name in plugins:
        del plugins[name]
        save_plugins(plugins)
        print(f"[green]Removed plugin: {name}[/green]")
    else:
        print(f"[bold red]Error: Plugin '{name}' not found.[/bold red]")

def list_plugins():
    plugins = load_plugins()
    if plugins:
        print("[green]Current plugins:[/green]")
        for name, method in plugins.items():
            print(f"- {name}: {method}")
    else:
        print("[yellow]No plugins found.[/yellow]")

def load_plugins():
    plugins_file = os.path.expanduser('~/.config/.plugins.json')
    if os.path.exists(plugins_file):
        with open(plugins_file, 'r') as f:
            return json.load(f)
    return {}

def save_plugins(plugins):
    plugins_file = os.path.expanduser('~/.config/.plugins.json')
    with open(plugins_file, 'w') as f:
        json.dump(plugins, f, indent=4)

@app.command(help="Manage environment variables. Actions: add, remove, list.")
def env(action: str, name: str = None, value: str = None):
    if action == "add":
        if not name or value is None:
            print("[bold red]Error: You must provide a name and value for the environment variable.[/bold red]")
            return
        add_env_variable(name, value)
    elif action == "remove":
        if not name:
            print("[bold red]Error: You must provide a name of the environment variable to remove.[/bold red]")
            return
        remove_env_variable(name)
    elif action == "list":
        list_env_variables()
    else:
        print("[bold red]Error: Invalid action. Use 'add', 'remove', or 'list'.[/bold red]")

def add_env_variable(name: str, value: str):
    env_vars = load_env_variables()
    env_vars[name] = value
    save_env_variables(env_vars)
    print(f"[green]Added environment variable: {name} with value: {value}[/green]")

def remove_env_variable(name: str):
    env_vars = load_env_variables()
    if name in env_vars:
        del env_vars[name]
        save_env_variables(env_vars)
        print(f"[green]Removed environment variable: {name}[/green]")
    else:
        print(f"[bold red]Error: Environment variable '{name}' not found.[/bold red]")

def list_env_variables():
    env_vars = load_env_variables()
    if env_vars:
        print("[green]Current environment variables:[/green]")
        for name, value in env_vars.items():
            print(f"- {name}: {value}")
    else:
        print("[yellow]No environment variables found.[/yellow]")

def load_env_variables():
    env_file = os.path.expanduser('~/.config/.env.json')
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            return json.load(f)
    return {}

def save_env_variables(env_vars):
    env_file = os.path.expanduser('~/.config/.env.json')
    with open(env_file, 'w') as f:
        json.dump(env_vars, f, indent=4)

@app.command(help="Manage machines for your dotfiles. Actions: add, remove, list.")
def machines(action: str, name: str = None):
    if action == "add":
        if not name:
            print("[bold red]Error: You must provide a name for the machine.[/bold red]")
            return
        add_machine(name)
    elif action == "remove":
        if not name:
            print("[bold red]Error: You must provide a name of the machine to remove.[/bold red]")
            return
        remove_machine(name)
    elif action == "list":
        list_machines()
    else:
        print("[bold red]Error: Invalid action. Use 'add', 'remove', or 'list'.[/bold red]")

def add_machine(name: str):
    machines = load_machines()
    if name in machines:
        print(f"[bold red]Error: Machine '{name}' already exists.[/bold red]")
        return
    machines[name] = {}
    save_machines(machines)
    print(f"[green]Added machine: {name}[/green]")

def remove_machine(name: str):
    machines = load_machines()
    if name in machines:
        del machines[name]
        save_machines(machines)
        print(f"[green]Removed machine: {name}[/green]")
    else:
        print(f"[bold red]Error: Machine '{name}' not found.[/bold red]")

def list_machines():
    machines = load_machines()
    if machines:
        print("[green]Current machines:[/green]")
        for name in machines.keys():
            print(f"- {name}")
    else:
        print("[yellow]No machines found.[/yellow]")

def load_machines():
    machines_file = os.path.expanduser('~/.config/.machines.json')
    if os.path.exists(machines_file):
        with open(machines_file, 'r') as f:
            return json.load(f)
    return {}

def save_machines(machines):
    machines_file = os.path.expanduser('~/.config/.machines.json')
    with open(machines_file, 'w') as f:
        json.dump(machines, f, indent=4)

if __name__ == "__main__":
    app()
