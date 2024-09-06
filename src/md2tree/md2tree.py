import hashlib
import subprocess
import time
from pathlib import Path

HEADER = """@startmindmap
top to bottom direction

"""

FOOTER = """@endmindmap
"""


class FileWatcher:
    def __init__(self, path: Path, latest_hash: str) -> None:
        self.path = path
        self.changed_count = 0
        self.latest_hash = latest_hash

    def watch(self) -> None:
        while True:
            content = self.path.read_text(encoding="utf-8")
            hash = hashlib.md5(content.encode()).hexdigest()

            if hash != self.latest_hash:
                self.changed_count += 1

            if self.changed_count > 10:
                print("file changed")
                self.latest_hash = hash
                break

            time.sleep(0.1)

    def get_latest_hash(self) -> str:
        return self.latest_hash


def convert(mdpath: Path) -> None:
    mdpath = Path(mdpath)
    pupath = mdpath.with_suffix(".pu")
    latest_hash = ''

    while True:
        watcher = FileWatcher(mdpath, latest_hash)
        
        try:
            watcher.watch()
            latest_hash = watcher.get_latest_hash()
        except KeyboardInterrupt:
            break

        print("md changed")
        md = mdpath.read_text(encoding="utf-8")
        pu = Md2Pu(md).convert()
        pupath.write_text(pu, encoding="utf-8")
        print("pu generated")

        print("convert to image")
        Pu2Png(pupath).convert()
        print("image generated")
        pupath.unlink()


class Md2Pu:
    def __init__(self, md: str) -> None:
        self.md = md

    def convert(self) -> str:
        return HEADER + self.convert_md() + FOOTER

    def convert_md(self) -> str:
        pu = ""
        for line in self.md.split("\n"):
            pu += self.convert_md_line(line) + "\n"
        return pu

    def convert_md_line(self, line: str) -> str:
        line = line.replace("- ", "* ")
        line = line.replace("  ", "*")
        return line


class Pu2Png:
    def __init__(self, pupath: Path) -> None:
        self.pupath = pupath

    def convert(self) -> None:
        # java -jar .\plantuml.jar .\test.pu -charset UTF-8
        command: list[str] = [
            "java",
            "-jar",
            "plantuml.jar",
            str(self.pupath),
            "-charset",
            "UTF-8",
        ]

        subprocess.run(command)


if __name__ == "__main__":
    convert(Path("sample.md"))
