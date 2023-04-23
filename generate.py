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

from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.pdfdoc import PDFPageLabel
from PIL import Image
import math
import os
import sys
import toml

dimensions = toml.load("dimensions.toml")
names = toml.load("names.toml")

pc = int(sys.argv[1])
qual = int(sys.argv[2])
width = math.ceil(dimensions["width"] * pc / 100)
height = math.ceil(dimensions["height"] * pc / 100)
prefix = f"s{pc}_q{qual}_"
dpi = dimensions["dpi"]
scale = 72 / dpi

subset = ""
if len(sys.argv) >= 4:
	subset = "_subset_" + "_".join(sys.argv[3:])
out_filename = f"{prefix}output{subset}.pdf"
canvas = Canvas(f"{out_filename}~", pagesize=(width * scale, height * scale))

prev_page_num = 0
prev_page_style = PDFPageLabel.ARABIC
prev_page_prefix = None

bookmarks = set()

def add_page(canvas, filename, page_num, page_style=PDFPageLabel.ARABIC, page_prefix=None):
	global prev_page_num, prev_page_style, prev_page_prefix

	if len(sys.argv) >= 4 and filename not in sys.argv[3:]:
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

for key, value in names.items():
	if key in bookmarks:
		canvas.addOutlineEntry(value, key, 0, True)

canvas.save()
os.rename(f"{out_filename}~", f"{out_filename}")
