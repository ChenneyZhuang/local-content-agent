"""CLI entry point for Local Content Agent."""

import sys
import argparse
from lca.pipeline import run


def main():
    parser = argparse.ArgumentParser(
        prog="lca",
        description="Local Content Agent — AI-powered social media content for local businesses",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # lca run "Business Name"
    run_parser = sub.add_parser("run", help="Generate content for a business")
    run_parser.add_argument("name", help="Business name")
    run_parser.add_argument(
        "--website", "-w", help="Website URL (auto-detected if omitted)"
    )
    run_parser.add_argument("--facebook", "-f", help="Facebook page URL")

    args = parser.parse_args()

    if args.command == "run":
        print(f"\n{'=' * 60}")
        print("  Local Content Agent")
        print(f"  Business: {args.name}")
        print(f"{'=' * 60}\n")

        try:
            result = run(args.name, website=args.website, facebook=args.facebook)
            print(f"\n{'=' * 60}")
            print(f"  ✅ {len(result.posts)} posts generated")
            print(f"  📁 {result.business.name}")
            print(f"{'=' * 60}")
        except Exception as e:
            print(f"\n❌ Error: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
