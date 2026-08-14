import tkinter

from lib.gui import App
from lib.num_counter import NumCounter
from lib.pdf_parser import PdfParser
from lib.html_generator import HTMLGenerator
from lib.pdf_maker import PDFMaker

# def main():
#     parser = PdfParser("docs/doc_max.pdf")
#     data = parser.parse(True)
#     #print(data)
#     generator = HTMLGenerator(data, "template.html")
#     generator.save("test.html")
#     #pdf = PDFMaker("test.html")
#     #pdf.save_pdf("test.pdf")

if __name__ == "__main__":
    root = tkinter.Tk()
    app = App(root)
    root.mainloop()