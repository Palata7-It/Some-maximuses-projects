from fpdf import FPDF


class image_class():
    def __init__(self):
        self.pdf = FPDF()

    def add_image(self, image_path):
        self.pdf.add_page()
        self.pdf.image(image_path, w=150)

    def close(self, name,path):
        self.pdf.output("{}.pdf".format(path+'\\'+name))
