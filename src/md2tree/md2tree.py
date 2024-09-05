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
    def __init__(self, path: Path) -> None:
        self.path = path
        self.changed_count = 0

    def watch(self) -> None:
        content = self.path.read_text(encoding="utf-8")

        latest_hash = hashlib.md5(content.encode()).hexdigest()

        while True:
            content = self.path.read_text(encoding="utf-8")
            hash = hashlib.md5(content.encode()).hexdigest()

            if hash != latest_hash:
                self.changed_count += 1

            if self.changed_count > 10:
                print("file changed")
                break

            time.sleep(0.1)


def convert(mdpath: Path) -> None:
    mdpath = Path(mdpath)
    pupath = mdpath.with_suffix(".pu")

    while True:
        watcher = FileWatcher(mdpath)

        try:
            watcher.watch()
        except KeyboardInterrupt:
            break

        print("md changed")
        md = mdpath.read_text(encoding="utf-8")
        pu = Md2Pu(md).convert()
        pupath.write_text(pu, encoding="utf-8")
        print("pu generated")

        print("convert to image")
        Pu2Jpg(pupath).convert()
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


class Pu2Jpg:
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
    latest_hash = None

    while True:
        with open("sample.md") as f:
            md = f.read()

        hash = hashlib.md5(md.encode()).hexdigest()

        if hash == latest_hash:
            continue

        print("md changed")

        latest_hash = hash

        pu = Md2Pu(md).convert()
        sample_pu = Path("sample.pu")
        sample_pu.write_text(pu, encoding="utf-8")

        print("pu generated")
        print("convert to jpg")
        Pu2Jpg(sample_pu).convert()
        print("jpg generated")
