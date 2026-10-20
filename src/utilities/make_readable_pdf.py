import argparse
from pathlib import Path

import pikepdf


def make_readable_pdf(source: Path, destination: Path) -> None:
    if source.resolve() == destination.resolve():
        raise SystemExit("Output must be a different file from the input PDF.")

    with pikepdf.open(source) as document:
        document.save(
            destination,
            qdf=True,
            object_stream_mode=pikepdf.ObjectStreamMode.disable,
            compress_streams=False,
            stream_decode_level=pikepdf.StreamDecodeLevel.generalized,
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Write a QDF-style PDF copy with streams uncompressed."
    )
    parser.add_argument("pdf", type=Path, help="Source PDF file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output file (default: <source>-readable.pdf)",
    )
    args = parser.parse_args()

    if not args.pdf.is_file():
        parser.error(f"PDF file not found: {args.pdf}")

    destination = args.output or args.pdf.with_name(f"{args.pdf.stem}-readable.pdf")
    make_readable_pdf(args.pdf, destination)
    print(f"Wrote: {destination}")


if __name__ == "__main__":
    main()