from lib.pdf_parser import PdfParser
from lib.html_generator import HTMLGenerator

def main():
    parser = PdfParser("docs/doc_max.pdf")
    data = parser.parse(True)
    print(data)
    generator = HTMLGenerator(data)
    generator.save("test.html")

if __name__ == "__main__":
    main()