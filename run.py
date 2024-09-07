import argparse
import os
import subprocess

if os.name == "nt":
    current_dirname = r"%cd%"
else:
    current_dirname = "$PWD"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert markdown to tree structure")
    parser.add_argument("input", help="Input markdown file")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    mount_dst = "/tmp/host"
    mdname = os.path.basename(args.input)
    command = f"docker run --rm -v {current_dirname}:{mount_dst} -t md2tree {mount_dst}/{mdname}"

    try:
        subprocess.run(command, shell=True)
    except KeyboardInterrupt:
        ...


if __name__ == "__main__":
    main()
