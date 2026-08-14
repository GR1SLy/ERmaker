from lib.pdf_parser import PdfParser


def main():
    parser = PdfParser("docs/doc_max.pdf")
    data = parser.parse(False)
    print(data)

if __name__ == "__main__":
    main()