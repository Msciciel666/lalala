"""Core CLI entry point."""

from argparse import ArgumentParser
from typing import Iterable

from utils.helpers import normalize_url
from scanner import loader


def crawl(url: str) -> None:
    """Run crawler on given URL and apply loaded plugins."""
    normalized = normalize_url(url)
    print(f"Crawling {normalized}")
    plugins = loader.load_plugins()
    for name, plugin in plugins.items():
        result = plugin.scan(normalized)
        if result:
            print(f"{name}: {result}")


def parse_dump(path: str) -> None:
    """Parse dump file using loaded plugins."""
    print(f"Parsing {path}")
    with open(path, "r", encoding="utf-8", errors="ignore") as fh:
        data = fh.read()
    plugins = loader.load_plugins()
    for name, plugin in plugins.items():
        result = plugin.scan(data)
        if result:
            print(f"{name}: {result}")


    def main(argv: Iterable[str] | None = None) -> None:
    """Entry point for the core CLI."""
   parser = ArgumentParser(description="darkweb666 core CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    crawl_p = sub.add_parser("crawl", help="Crawl a URL")
    crawl_p.add_argument("url")

    dump_p = sub.add_parser("parse-dump", help="Parse a dump file")
    dump_p.add_argument("path")

    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.command == "crawl":
        crawl(args.url)
    elif args.command == "parse-dump":
        parse_dump(args.path)


if __name__ == "__main__":
    main()
