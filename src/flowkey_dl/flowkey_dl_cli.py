import argparse
from flowkey_dl import flowkey_dl, arange_image, save_pdf


def main():
    parser = argparse.ArgumentParser(
        description="Sheet Music downloader for flowkey")
    parser.add_argument(
        "baseurl", help="Flowkey sheet music base url (url of first image)"
    )
    parser.add_argument(
        "output_path",
        nargs="?",
        help="Output path for pdf",
        default="output.pdf",
    )
    parser.add_argument("-t", "--title", help="Title of the flowkey song")
    parser.add_argument(
        "-a",
        "--artist",
        action="store",
        type=str,
        help="Artist of the provided title",
    )

    args = parser.parse_args()

    pdf_path = args.output_path  # TODO: Check if input is filepath
    artist = args.artist if args.artist is not None else ""
    title = args.title if args.title is not None else ""
    image, _, _ = flowkey_dl(args.baseurl)
    processed_image = arange_image(image, title, artist)
    save_pdf(processed_image, pdf_path)


if __name__ == "__main__":
    main()
