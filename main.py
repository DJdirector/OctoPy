import os
import subprocess
import platform
import threading
from datetime import datetime
from collections import defaultdict

from textual.app import App, ComposeResult
from textual.widgets import Static, Label, Tree, Input
from textual.containers import Horizontal, Vertical, VerticalScroll


class OctoPy(App):
    """🐍 OctoPy 🐙 — Universal Responsive Script Dashboard."""

    CSS_PATH = "style.tcss"
    BINDINGS = [("ctrl+c", "kill_script", "Kill Running Script")]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.log_lock = threading.Lock()  # Prevents race conditions in markup
        self.output_buffer = ""
        self.active_process = None
        self.last_script_state = None  # Stores the previous state of the scripts folder

    def get_scripts(self, base_dir="./scripts"):
        """Scans the directory and returns a dictionary of categories and files."""
        categories = defaultdict(list)
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        for root, _, files in os.walk(base_dir):
            rel = os.path.relpath(root, base_dir)
            category = "GENERAL" if rel == "." else rel.upper()
            for file in sorted(files):
                categories[category].append(os.path.join(root, file))
        return dict(categories)

    def compose(self) -> ComposeResult:
        with Horizontal(id="header-bar"):
            yield Label(" OctoPy - Universal Responsive Script Dashboard.")
            yield Label("", id="clock")

        with Horizontal(id="main-body"):
            with Vertical(id="file-panel"):
                tree = Tree("", id="file-tree")
                tree.show_root = False
                tree.root.expand()
                yield tree

            with Vertical(id="output-panel"):
                yield Label(" | Output (Ctrl+C to Kill)", classes="status-header")
                with VerticalScroll(id="log-scroll"):
                    yield Static("System ready.", id="log-text")
                yield Input(placeholder="Type input here and press Enter...", id="user-input")

        with Horizontal(id="footer-bar"):
            yield Label("V0.1 - EXPERIMENTAL", id="version")

    def on_mount(self) -> None:
        """Initializes timers for the clock and filesystem polling."""
        self.set_interval(1, self.update_clock)
        # Poll for file changes every 2 seconds
        self.set_interval(2, self.check_for_file_changes)
        self.refresh_tree_display()

    def update_clock(self) -> None:
        try:
            self.query_one("#clock", Label).update(
                datetime.now().strftime("%H:%M:%S"))
        except:
            pass

    def check_for_file_changes(self) -> None:
        """Compares current disk state to last known state and updates if needed."""
        current_scripts = self.get_scripts()
        # Only refresh the UI if the file structure has actually changed
        if current_scripts != self.last_script_state:
            self.refresh_tree_display(current_scripts)

    def refresh_tree_display(self, scripts=None):
        """Rebuilds the tree widget nodes from scratch."""
        if scripts is None:
            scripts = self.get_scripts()

        tree = self.query_one("#file-tree", Tree)
        tree.clear()  # Correct way to empty the tree

        for cat in sorted(scripts):
            cat_node = tree.root.add(f"[bold]{cat}[/bold]")
            cat_node.expand()
            for path in scripts[cat]:
                cat_node.add_leaf(os.path.basename(path), data=path)

        self.last_script_state = scripts

    def action_kill_script(self) -> None:
        if self.active_process and self.active_process.poll() is None:
            self.active_process.terminate()
            with self.log_lock:
                self.output_buffer += "\n[bold red]❱ PROCESS TERMINATED BY USER[/bold red]\n"
                self.update_log_ui()

    def update_log_ui(self):
        log_text = self.query_one("#log-text", Static)
        log_scroll = self.query_one("#log-scroll", VerticalScroll)
        log_text.update(self.output_buffer)
        # Auto-follow bottom like a terminal
        log_scroll.scroll_end(animate=False)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if self.active_process and self.active_process.poll() is None:
            # Send input to process
            self.active_process.stdin.write(event.value + "\n")
            self.active_process.stdin.flush()

            # Update buffer safely
            with self.log_lock:
                self.output_buffer += f"[bold yellow]> {event.value}[/bold yellow]\n"
                self.update_log_ui()

            event.input.value = ""

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        path = event.node.data
        if not path:
            return

        self.query_one("#user-input").focus()

        with self.log_lock:
            self.output_buffer = f"❱ Running: [bold cyan]{os.path.basename(path)}[/bold cyan]...\n\n"
            self.update_log_ui()

        def run_and_stream():
            try:
                if platform.system() == "Windows":
                    cmd = ["python", "-u",
                           path] if path.endswith(".py") else ["cmd", "/c", path]
                    shell_mode = True
                else:
                    cmd = ["python3", "-u",
                           path] if path.endswith(".py") else ["bash", path]
                    shell_mode = False

                self.active_process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    bufsize=0,
                    shell=shell_mode
                )

                while True:
                    char = self.active_process.stdout.read(1)
                    if not char and self.active_process.poll() is not None:
                        break
                    if char:
                        with self.log_lock:
                            self.output_buffer += char
                            self.call_from_thread(self.update_log_ui)

                self.active_process.wait()

                with self.log_lock:
                    if self.active_process.returncode == 0:
                        self.output_buffer += "\n[bold green]STATUS: SUCCESS[/bold green]"
                    elif self.active_process.returncode != -15:  # Not killed by user
                        self.output_buffer += f"\n[bold red]STATUS: FAILED ({self.active_process.returncode})[/bold red]"
                    self.call_from_thread(self.update_log_ui)

            except Exception as e:
                with self.log_lock:
                    self.output_buffer += f"\n[bold red]EXECUTION ERROR:[/bold red] {str(e)}"
                    self.call_from_thread(self.update_log_ui)

        threading.Thread(target=run_and_stream, daemon=True).start()


if __name__ == "__main__":
    OctoPy().run()
