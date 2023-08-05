import argparse
import os

from psd2html import psd2html


def main():
    parser = argparse.ArgumentParser(description='Convert PSD file to HTML')

    parser.add_argument(
        'input', type=str, help='Input PSD file path or URL')
    parser.add_argument(
        'output', type=str, nargs='?', default='',
        help='Output file or directory. When directory is specified, filename'
             ' is automatically inferred from input')

    args = parser.parse_args()

    prefix, ext = os.path.splitext(args.output)
    if ext.lower() != '.html':
        if not prefix:
            prefix, ext = os.path.splitext(args.input)
        if prefix.endswith('/'):
            filename, ext = os.path.splitext(args.input)
            prefix = prefix + filename
        html_file = prefix + ".html"
        psd2html(args.input, html_file)
    else:
        psd2html(args.input, args.output)


if __name__ == '__main__':
    main()
