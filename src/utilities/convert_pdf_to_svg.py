import argparse
import xml.etree.ElementTree as ET
from pathlib import Path

import pymupdf


SVG_NS = "http://www.w3.org/2000/svg"


def add_white_page_background(svg: str) -> str:
    ET.register_namespace("", SVG_NS)
    ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
    ET.register_namespace("inkscape", "http://www.inkscape.org/namespaces/inkscape")
    root = ET.fromstring(svg)
    x, y, width, height = map(float, root.attrib["viewBox"].replace(",", " ").split())
    background = ET.Element(
        f"{{{SVG_NS}}}rect",
        {
            "x": str(x),
            "y": str(y),
            "width": str(width),
            "height": str(height),
            "fill": "#ffffff",
        },
    )
    insert_at = 1 if len(root) and root[0].tag == f"{{{SVG_NS}}}defs" else 0
    root.insert(insert_at, background)
    return ET.tostring(root, encoding="unicode")


def convert_pdf_to_svg(
    source: Path,
    output_dir: Path | None = None,
    outline_text: bool = False,
    overwrite: bool = False,
) -> list[Path]:
    output_dir = output_dir or source.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    with pymupdf.open(source) as document:
        page_count = document.page_count
        if page_count == 1:
            destinations = [output_dir / f"{source.stem}.svg"]
        else:
            destinations = [
                output_dir / f"{source.stem}-page-{page_number + 1:03}.svg"
                for page_number in range(page_count)
            ]

        existing = [path for path in destinations if path.exists()]
        if existing and not overwrite:
            names = ", ".join(str(path) for path in existing)
            raise FileExistsError(f"Output file(s) already exist: {names}; use --overwrite to replace them")

        for page_number, destination in enumerate(destinations):
            svg = document.load_page(page_number).get_svg_image(text_as_path=outline_text)
            svg = add_white_page_background(svg)
            destination.write_text(svg, encoding="utf-8")

    return destinations


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert PDF pages to SVG while preserving text when possible."
    )
    parser.add_argument("pdf", type=Path, help="Source PDF file")
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Directory for SVG files (default: next to the PDF)",
    )
    parser.add_argument(
        "--outline-text",
        action="store_true",
        help="Convert text glyphs to vector paths instead of SVG text",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace existing output files",
    )
    args = parser.parse_args()

    if not args.pdf.is_file():
        parser.error(f"PDF file not found: {args.pdf}")

    try:
        destinations = convert_pdf_to_svg(
            args.pdf,
            args.output_dir,
            outline_text=args.outline_text,
            overwrite=args.overwrite,
        )
    except FileExistsError as error:
        parser.error(str(error))

    for destination in destinations:
        print(f"Wrote: {destination}")


if __name__ == "__main__":
    main()