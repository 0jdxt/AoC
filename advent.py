#!/usr/bin/env python3.7
import os
from pathlib import Path
from glob import glob
from subprocess import run, DEVNULL
import linecache
import cmd
import time
import readline


class AdventShell(cmd.Cmd):
    intro = "Advent of Code shell.   Type help or ? to list commands.\n"
    home_path = Path().cwd()
    histfile = home_path / ".advent_history"
    histfile_size = 100
    path = home_path / glob("*/")[-1]

    def title(self, text: str):
        print(f"\33]0;{text}\a", end="")

    def preloop(self):
        global refresh
        refresh = False
        os.chdir(self.path)
        self.title(f"AoC {self.path.name}")

        if self.histfile.exists():
            readline.read_history_file(self.histfile)

    def postloop(self):
        readline.set_history_length(self.histfile_size)
        readline.write_history_file(self.histfile)

    def precmd(self, line):
        self.title(f"AoC {line}")
        return line

    def postcmd(self, stop, line):
        self.title(f"AoC {self.path.name}")
        return stop

    def emptyline(self):
        pass

    def run_once(self, day, timed=False):
        if not day or not day.isdigit():
            return

        file = Path(f"day_{day}.py")
        if file.exists():

            if not timed:
                print(linecache.getline(str(file), 2).strip('\n"'))

            start = time.time()
            try:
                run(["python3.7", file.name], stdout=DEVNULL if timed else None)
            except KeyboardInterrupt:
                return print(f"Aborted after {time.time() - start:g}s")

            return time.time() - start

        if input(f"Create {file}? [y/N]") == "y":
            title = input("Enter title: ")
            file.write_text(templ % (day, title, file.stem))

            data_file = Path() / "input_data" / file.stem
            data_file.touch()

            run(["subl", data_file, file.name])
            print(f"Files {file.name} and {data_file} created")

    def do_run(self, day):
        """Usage: run DAY. Run day_{DAY}.py."""
        t = self.run_once(day)
        if t:
            print(f"[Finished after {t:g}s]")

    def complete_run(self, text, line, i0, i1):
        return [f.name[4:-3] for f in self.path.glob(f"day_{text}*.py")]

    def do_time(self, arg):
        """Usage: time DAY N. Time N runs of day_{DAY}.py"""
        args = arg.split()
        day = args[0]
        if len(args) < 2:
            n = 1
        elif args[1].isdigit():
            n = int(args[1])
        else:
            return self.do_help("time")

        tot = 0
        for _ in range(n):
            t = self.run_once(day, True)
            tot += t
            print(f"{t:g}")
        print("avg:", f"{tot / n:g}")

    def complete_time(self, text, line, i0, i1):
        if i0 == len("time "):  # only first arg
            return self.complete_run(text, line, i0, i1)

    def do_year(self, year):
        """Usage: year XXXX. Chdir into year XXXX"""
        yr = self.home_path / year
        if yr.samefile(self.path):
            print(f"Already in {year}!")
        elif yr.exists():
            os.chdir(yr)
            self.path = Path().cwd()
        else:
            print(f"no directory found for {year}")

    def complete_year(self, text, line, i0, i1):
        return [f.name for f in self.home_path.glob(f"{text}*") if f.is_dir()]

    def do_refresh(self, _):
        """Refresh linecache."""
        global refresh
        refresh = True
        os.chdir(self.home_path)
        return True

    def do_q(self, _):
        """Exit the shell."""
        return True

    def do_shell(self, arg):
        """Run commands on the shell"""
        run(arg.split())

    @property
    def prompt(self):
        return f"{self.path.name} AoC> "


templ = """#!/usr/bin/env python3.7
\"""--- Day %s: %s ---\"""

if __name__ == "__main__":
    with open('input_data/%s') as f:
        data = f.read()
    print(data)
"""

refresh = True
if __name__ == "__main__":
    while refresh:
        linecache.clearcache()
        try:
            AdventShell().cmdloop()
        except KeyboardInterrupt:
            readline.write_history_file(AdventShell.histfile)
