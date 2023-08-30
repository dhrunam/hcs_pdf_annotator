from sys import argv
import qrcode
import os
import sys
import urllib
# from PIL import Image
from qrcode.image.pure import PyPNGImage



def GenerateQrCode(data):
    # data = input("enter a string to encode\n")
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

def annotate_pdf(annotation, file_name):

    # source_pdf = '/home/vpnscript/Desktop/hg_orders_baqckup/' + file_name
    
    # output_pdf = '/home/vpnscript/Desktop/hg_orders_backup/' + file_name

    source_pdf = '/source/' + file_name
    
    output_pdf = '/destination/' + file_name

    # retrieve the first page of the PDF
    try:
        file_handle = fitz.open(source_pdf)
        if file_handle:
            for page in file_handle:

                # page = file_handle[0]
                # print(page.mediabox_size)
                image_rectangle = fitz.Rect(page.mediabox_size[0]-(page.mediabox_size[0]-500)
                                            ,page.mediabox_size[1]-(page.mediabox_size[1]-10)
                                            ,page.mediabox_size[0]-(page.mediabox_size[0]-620)
                                            ,page.mediabox_size[1]-(page.mediabox_size[1]-40)
                                            )

                # Add annotation to the page
                page.add_freetext_annot(image_rectangle, annotation, fontsize=10, fontname='helv', border_color=None, text_color=0, fill_color=1, rotate=0)
            
            file_handle.save(output_pdf)

    except:
        pass

import pandas as pd

def annotat_from_excel():
    sheet1 = pd.read_excel('guide.xlsx', sheet_name='Sheet1')

    for index, row in sheet1.iterrows():
        print (index,row["sl_no"], row["citation_number"], row['file_path'])
        annotate_pdf(row["citation_number"], row['file_path'])

def annotat_from_csv():
    sheet1 = pd.read_csv('guide.csv')

    for index, row in sheet1.iterrows():
        print (index,row["sl_no"], row["citation_number"], row['file_path'])
        annotate_pdf(row["citation_number"], row['file_path'])

'''
    Comment or uncomment the following line according to your requirement. This function
    use to read from excel file
'''
# annotat_from_excel()
'''
    Comment or uncomment the following line according to your requirement. This function
    use to read from csv file
'''
annotat_from_csv()