from sys import argv
import qrcode
import os
import sys
import urllib
import io
# from PIL import Image
from qrcode.image.pure import PyPNGImage



def GenerateQrCode(data):
    # data = input("enter a string to encode\n")

    # data="test"
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

def GetQrCode(data):
    qr = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    fp = io.BytesIO()
    img.save(fp, "PNG", )
    return fp



import fitz

def annotate_pdf(annotation, file_name):
    data="https://hcs.gov.in/hcs/hg_judgements/"+file_name
    qr_code=GetQrCode(data)

    source_pdf = 'hg_judgments/' + file_name
    
    output_pdf = 'output/' + file_name

    # retrieve the first page of the PDF
    try:
        file_handle = fitz.open(source_pdf)
        if file_handle:
            for page in file_handle:

                # page = file_handle[0]
                # print(page.mediabox_size)
                nc_rectangle = fitz.Rect(page.mediabox_size[0]-(page.mediabox_size[0]-510)
                                            ,page.mediabox_size[1]-(page.mediabox_size[1]-10)
                                            ,page.mediabox_size[0]-(page.mediabox_size[0]-650)
                                            ,page.mediabox_size[1]-(page.mediabox_size[1]-50)
                                            )
                image_rectangle = fitz.Rect(page.mediabox_size[0]-(page.mediabox_size[0]-10)
                                            ,page.mediabox_size[1]-(page.mediabox_size[1]-10)
                                            ,page.mediabox_size[0]-(page.mediabox_size[0]-90)
                                            ,page.mediabox_size[1]-(page.mediabox_size[1]-90)
                                            )
                # rect = fitz.Rect(15, 15, 135, 135)
                # Add annotation to the page
                # page.add_freetext_annot(image_rectangle, annotation, fontsize=10, fontname='helv', border_color=None, text_color=0, fill_color=1, rotate=0)
                
                # Add image from path
                # page.insert_image(image_rectangle, filename=qr_code)
                page.insert_image(image_rectangle, stream=qr_code)
                page.add_freetext_annot(nc_rectangle, annotation)
            
            file_handle.save(output_pdf)

    except Exception as e:
        print("An error occurred: {}".format(e))
import pandas as pd

def annotat_from_excel():
    sheet1 = pd.read_excel('guide.xlsx', sheet_name='Sheet1')

    for index, row in sheet1.iterrows():
        # print (index,row["sl_no"], row["citation_number"], row['file_path'])
        annotate_pdf(row["citation_number"], row['file_path'])

def annotat_from_csv():
    sheet1 = pd.read_csv('data-judgement_list.csv')

    for index, row in sheet1.iterrows():
        print (index, row["judgementfile"], row['nc'])
        annotate_pdf(row["nc"], row['judgementfile'])

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

# GenerateQrCode()