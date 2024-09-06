import argparse
import subprocess


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert markdown to tree structure")
    parser.add_argument("input", help="Input markdown file")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    mount_dst = "/tmp/host"
    command = f"docker run --rm -v $PWD:{mount_dst} -t md2tree {mount_dst}/{args.input}"
    try:
        subprocess.run(command, shell=True)
    except KeyboardInterrupt:
        ...


if __name__ == "__main__":
    main()
