import os
from playwright.sync_api import sync_playwright


class PDFMaker:
    def __init__(self, html_path: str):
        self.html_path = os.path.abspath(html_path)

    def save_pdf(self, pdf_path: str):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()

            # Преобразуем путь в file:/// URL (корректно для Windows)
            url = f'file:///{self.html_path.replace(os.sep, "/")}'

            # Загружаем страницу и ждём все ресурсы (включая изображения)
            page.goto(url, wait_until='networkidle')

            # Генерируем PDF
            page.pdf(
                path=pdf_path,
                format='A4',
                print_background=True,
                margin={
                    'top': '10mm',
                    'bottom': '10mm',
                    'left': '10mm',
                    'right': '10mm'
                }
            )
            browser.close()