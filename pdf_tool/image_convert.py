import os
import image_class


def make_pdf_file(name, path):
    pdf_img = image_class.image_class()
    list_photo = list(filter(lambda i: i.endswith('.jpg'), list(os.listdir(path))))
    for i in list_photo:
        pdf_img.add_image(path+'\\'+i)
    pdf_img.close(name,path)
