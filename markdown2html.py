#!/usr/bin/env python3
import sys
import os
import re
import hashlib

def convert_markdown_to_html(input_file, output_file):
    # Read the Markdown file
    with open(input_file, 'r') as file:
        content = file.read()

    # Replace headings
    content = re.sub(r'^###### (.*)', r'<h6>\1</h6>', content, flags=re.MULTILINE)
    content = re.sub(r'^##### (.*)', r'<h5>\1</h5>', content, flags=re.MULTILINE)
    content = re.sub(r'^#### (.*)', r'<h4>\1</h4>', content, flags=re.MULTILINE)
    content = re.sub(r'^### (.*)', r'<h3>\1</h3>', content, flags=re.MULTILINE)
    content = re.sub(r'^## (.*)', r'<h2>\1</h2>', content, flags=re.MULTILINE)
    content = re.sub(r'^# (.*)', r'<h1>\1</h1>', content, flags=re.MULTILINE)

    # Replace unordered lists
    content = re.sub(r'^\- (.*)', r'<li>\1</li>', content, flags=re.MULTILINE)
    content = re.sub(r'(<li>.*</li>)', r'<ul>\1</ul>', content, flags=re.DOTALL)

    # Replace ordered lists
    content = re.sub(r'^\* (.*)', r'<li>\1</li>', content, flags=re.MULTILINE)
    content = re.sub(r'(<li>.*</li>)', r'<ol>\1</ol>', content, flags=re.DOTALL)

    # Replace paragraphs and line breaks
    content = re.sub(r'(\n\n)', r'</p>\n<p>', content)
    content = re.sub(r'(\n)', r'<br/>', content)

    # Replace bold and emphasis text
    content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', content)
    content = re.sub(r'__(.*?)__', r'<em>\1</em>', content)

    # Handle special syntax
    content = re.sub(r'\[\[(.*?)\]\]', lambda m: hashlib.md5(m.group(1).encode()).hexdigest(), content)
    content = re.sub(r'\(\((.*?)\)\)', lambda m: m.group(1).replace('c', '').replace('C', ''), content)

    # Write to the output HTML file
    with open(output_file, 'w') as file:
        file.write(f"<html>\n<body>\n{content}\n</body>\n</html>")

def main():
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    markdown_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    convert_markdown_to_html(markdown_file, output_file)
    sys.exit(0)

if __name__ == "__main__":
    main()
