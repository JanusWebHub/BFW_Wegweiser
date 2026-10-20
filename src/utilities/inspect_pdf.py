import argparse
import json
from pathlib import Path

import pymupdf


def inspect_pdf(pdf_path: Path) -> None:
    with pymupdf.open(pdf_path) as document:
        print(f"File: {pdf_path}")
        print(f"Pages: {document.page_count}")
        print(f"Encrypted: {document.is_encrypted}")
        print("Metadata:")
        print(json.dumps(document.metadata, indent=2, ensure_ascii=False))

        for page_number in range(document.page_count):
            page = document.load_page(page_number)
            print(f"\n--- Page {page_number + 1} ---")
            print(f"Size: {page.rect.width:.2f} x {page.rect.height:.2f} pt")

            images = page.get_image_info(xrefs=True)
            print(f"Images: {len(images)}")
            for image in images:
                print(
                    "  "
                    f"xref={image.get('xref', 0)} "
                    f"size={image.get('width')}x{image.get('height')} "
                    f"bbox={image.get('bbox')}"
                )

            fonts = document.get_page_fonts(page_number, full=True)
            print(f"Fonts: {len(fonts)}")
            for font in fonts:
                print(f"  {font}")

            text_result = page.get_text("text", sort=True)
            text = text_result.strip() if isinstance(text_result, str) else ""
            print("Extracted text:")
            print(text if text else "  [No extractable text]")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Report PDF metadata, page content, images, fonts, and text."
    )
    parser.add_argument("pdf", type=Path, help="PDF file to inspect")
    args = parser.parse_args()

    if not args.pdf.is_file():
        parser.error(f"PDF file not found: {args.pdf}")

    inspect_pdf(args.pdf)


if __name__ == "__main__":
    main()