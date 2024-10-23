import subprocess
import json

from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.layout import Layout
import keyboard


def get_backend_version() -> str:
    with open('backend/__init__.py', 'r') as f:
        lines = f.readline().strip()
    version = lines.split('=')[1].strip().strip('\'')
    Console().print(f"Current backend version is [b]{version}[/]")
    return version

def set_backend_version(version) -> None:
    Console().print(f"Set backend version to [b]{version}[/]")
    line = f"__version__ = '{version}'\n"
    with open('backend/__init__.py', 'w') as f:
        f.write(line)

def get_frontend_version() -> str:
    j = json.load(open('frontend/package.json'))
    version = j['version']
    Console().print(f"Current frontend version is [b]{version}[/]")
    return version

def set_frontend_version(version) -> None:
    Console().print(f"Set frontend version to [b]{version}[/]")
    j = json.load(open('frontend/package.json'))
    j['version'] = version
    with open('frontend/package.json', 'w') as f:
        json.dump(j, f, indent=4)

def set_git_tag(frontend_version, backend_version) -> None:
    subprocess.run(['git', 'tag', f'v{frontend_version}-{backend_version}'])


class Selection:
    def __init__(self, which: str, version: str, items: list[str]) -> None:
        self.which = which
        self.version = version
        self.items = items
        self.selected_index = 0
        self.running = True
        self.console = Console()

    def render_menu(self) -> Layout:
        table = Table(show_header=False, box=None)
        if self.running:
            for i, item in enumerate(self.items):
                if i == self.selected_index:
                    table.add_row(f"[b green]-> {item:<5}[/] ({self.get_next_version(i)})")
                else:
                    table.add_row(f"   [cyan]{item:<5}[/]")

        return table

    def on_key_event(self, event) -> None:
        if event.name == "up":
            self.selected_index = (self.selected_index - 1) % len(self.items)
        elif event.name == "down":
            self.selected_index = (self.selected_index + 1) % len(self.items)
        elif event.name == "enter":
            self.running = False

    def run(self) -> None:
        keyboard.on_press(self.on_key_event)
        with Live(self.render_menu(), refresh_per_second=60, console=self.console) as live:
            while self.running:
                live.update(self.render_menu())
            live.update(self.render_menu())

    def get_selected(self) -> str:
        return self.get_next_version(self.selected_index)

    def get_next_version(self, index) -> str:
        v1, v2, v3 = self.version.split('.')
        if index == 0:
            v1 = str(int(v1) + 1)
        elif index == 1:
            v2 = str(int(v2) + 1)
        elif index == 2:
            v3 = str(int(v3) + 1)
        return f'{v1}.{v2}.{v3}'


def select_version(which: str, version: str) -> str:
    items = ['Major', 'Minor', 'Patch', 'None']
    selection = Selection(which, version, items)
    selection.run()
    selected = selection.get_selected()
    return selected


if __name__ == "__main__":

    backend_version = get_backend_version()
    backend_version = select_version('backend', backend_version)
    set_backend_version(backend_version)

    frontend_version = get_frontend_version()
    frontend_version = select_version('frontend', frontend_version)
    set_frontend_version(frontend_version)

    set_git_tag(frontend_version, backend_version)