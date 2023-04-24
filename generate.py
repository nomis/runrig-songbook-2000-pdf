#!/usr/bin/env python3
# Copyright 2023  Simon Arlott
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from argparse import ArgumentParser
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.pdfdoc import PDFPageLabel
from PIL import Image
import os
import toml

parser = ArgumentParser()
parser.add_argument("size", type=int, help="Size in %%")
parser.add_argument("quality", type=int, help="Quality in %%")
parser.add_argument("dpi", type=int, help="Dots per inch")
parser.add_argument("--subset", type=str, metavar="PAGE", nargs="+", help="Output only a subset of pages")
args = parser.parse_args()

metadata = toml.load("metadata.toml")

prefix = f"s{args.size}_q{args.quality}_"
scale = 72 / args.dpi

suffix = ""
if args.subset:
	suffix = "_subset_" + "_".join(args.subset)
out_filename = f"output_{prefix}d{args.dpi}{suffix}.pdf"
canvas = Canvas(f"{out_filename}~")

prev_page_num = 0
prev_page_style = PDFPageLabel.ARABIC
prev_page_prefix = None

bookmarks = set()

canvas.setTitle(metadata["title"])
canvas.setAuthor(metadata["author"])
canvas.setSubject(metadata["subject"])

def add_page(canvas, filename, page_num, page_style=PDFPageLabel.ARABIC, page_prefix=None):
	global prev_page_num, prev_page_style, prev_page_prefix

	if args.subset and filename not in args.subset:
		return

	img_filename = f"pages/{prefix}{filename}.jpg"

	if os.path.exists(img_filename):
		pdf_page_index = canvas.getPageNumber() - 1
		if page_style != prev_page_style or page_prefix != prev_page_prefix or page_num != prev_page_num + 1:
			canvas.addPageLabel(pdf_page_index, start=page_num, style=page_style, prefix=page_prefix)

		with Image.open(img_filename) as im:
			canvas.setPageSize((im.width * scale, im.height * scale))
			canvas.scale(scale, scale)
			canvas.drawInlineImage(im, 0, 0)
		del im

		canvas.bookmarkPage(filename)
		bookmarks.add(filename)
		canvas.showPage()

		prev_page_num = page_num
		prev_page_style = page_style
		prev_page_prefix = page_prefix

add_page(canvas, f"000a", 1, page_prefix="F")
add_page(canvas, f"000b", 2, page_prefix="F")

for page in range(1, 297):
	add_page(canvas, f"{page:03d}", page)

add_page(canvas, f"297a", 1, page_prefix="B")
add_page(canvas, f"297b", 2, page_prefix="B")

for key, value in metadata["page_names"].items():
	if key in bookmarks:
		canvas.addOutlineEntry(value, key, 0, True)

canvas.save()
os.rename(f"{out_filename}~", f"{out_filename}")
