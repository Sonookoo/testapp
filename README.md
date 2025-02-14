### deploy
```
# /home/Sonookoo/.local/lib/python3.10/site-packages/pythonanywhere/virtualenvs.py を以下に置き換える

import os
import subprocess
from pathlib import Path
from snakesay import snakesay
class Virtualenv:
    def __init__(self, domain, python_version):
        self.domain = domain
        self.python_version = python_version
        self.path = Path(os.environ["WORKON_HOME"]) / domain
    def __eq__(self, other):
        return self.domain == other.domain and self.python_version == other.python_version
    def create(self, nuke):
        print(snakesay(f"Creating virtualenv with Python{self.python_version}"))
        command = f"mkvirtualenv --python=python{self.python_version} {self.domain}"
        if nuke:
            command = f"rmvirtualenv {self.domain} && {command}"
        subprocess.check_call(["bash", "-c", f"source virtualenvwrapper.sh && {command}"])
        return self
    def pip_install(self, packages):
        print(snakesay(f"Pip installing {packages} (this may take a couple of minutes)"))
        subprocess.check_call([str(self.path / "bin/pip"), "cache", "purge"])
        commands = [str(self.path / "bin/pip"), "install"] + packages.split() + ["--no-cache-dir"]
        subprocess.check_call(commands)
    def get_version(self, package_name):
        commands = [str(self.path / "bin/pip"), "show", package_name]
        output = subprocess.check_output(commands).decode()
        for line in output.splitlines():
            if line.startswith("Version: "):
                return line.split()[1]
```

```
pa_autoconfigure_django.py --python=3.8 https://github.com/Sonookoo/testapp.git --nuke --branch=master
```