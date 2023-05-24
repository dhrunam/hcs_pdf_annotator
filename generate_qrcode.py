from sys import argv
import qrcode
import os
import sys
import urllib
# from PIL import Image
from qrcode.image.pure import PyPNGImage



data = input("enter a string to encode\n")
qr = qrcode.QRCode(
    version = 1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size = 10,
    border = 4,
)
qr.add_data(data)
data = urllib.parse.quote_plus(data)
img = qr.make_image(image_factory= PyPNGImage)
img.save('output/' + data + '.png', ) #can also be .bmp, .jpeg


import fitz

source_pdf = 'source.pdf'
qrcode_png = 'output/' + data + '.png'
output_pdf = 'output/' + data + '.pdf'

target_daocument = fitz.open(source_pdf)

# retrieve the first page of the PDF
file_handle = fitz.open(source_pdf)
# for i in range(file_handle.page_count):
# for page in file_handle:
#     print(page.mediabox_size)
# # define the position (upper-right corner)
page = file_handle[0]
image_rectangle = fitz.Rect(page.mediabox_size[0]-(page.mediabox_size[0]-750)
                                ,page.mediabox_size[1]-(page.mediabox_size[1]-30)
                                ,page.mediabox_size[0]-(page.mediabox_size[0]-850)
                                ,page.mediabox_size[1]-(page.mediabox_size[1]-130)
                                )

    # add the image
    # page.insert_image(image_rectangle, filename=qrcode_png)
# add_freetext_annot(rect, text, fontsize=12, fontname='helv', border_color=None, text_color=0, fill_color=1, rotate=0, align=TEXT_ALIGN_LEFT)

page.add_freetext_annot(image_rectangle, 'testing...and testing', fontsize=12, fontname='helv', border_color=None, text_color=0, fill_color=1, rotate=0)
page.insert_image(image_rectangle, filename=qrcode_png)


file_handle.save(output_pdf)
