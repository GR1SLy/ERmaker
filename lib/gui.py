import tkinter as tk
import traceback
from tkinter import ttk, filedialog, messagebox
from lib.html_generator import HTMLGenerator
from lib.num_counter import NumCounter
from lib.pdf_maker import PDFMaker
from lib.pdf_parser import PdfParser
from tkcalendar import DateEntry

month_names = {
    1: 'января',
    2: 'февраля',
    3: 'марта',
    4: 'апреля',
    5: 'мая',
    6: 'июня',
    7: 'июля',
    8: 'августа',
    9: 'сентября',
    10: 'октября',
    11: 'ноября',
    12: 'декабря'
}

class App:
    def __init__(self, root):
        self.parsed_data = None
        self.root = root
        self.root.title("СОЗДАНИЕ РАСПИСКИ by GR1SLy")
        x = (root.winfo_screenwidth() - 600) // 2
        y = (root.winfo_screenheight() - 400) // 2
        self.root.geometry(f"600x400+{x}+{y}")
        self.root.resizable(False, False)

        # Переменные для хранения данных
        self.client_phone = tk.StringVar()
        self.expeditor_phone = tk.StringVar()
        self.shipper_phone = tk.StringVar()
        self.consignee_phone = tk.StringVar()

        # Создание фреймов
        left_frame = ttk.Frame(root, padding=10)
        left_frame.grid(row=0, column=0, sticky="nsew")

        right_frame = ttk.Frame(root, padding=10)
        right_frame.grid(row=0, column=1, sticky="nsew")

        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(0, weight=1)

        # Левая часть
        ttk.Button(left_frame, text="Загрузить поручение", command=self.load_file).pack(fill='x', pady=5)

        ttk.Label(left_frame, text="Дата создания расписки").pack(anchor='w')
        # Виджет выбора даты с календарём
        self.date_entry = DateEntry(
            left_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='dd.mm.yyyy',   # формат отображения
            locale='ru_RU'                # русская локаль (если поддерживается)
        )
        self.date_entry.pack(fill='x', pady=5)

        ttk.Button(left_frame, text="Обнулить нумерацию", command=self.__confirm_zeroize).pack(fill='x', pady=5)
        ttk.Button(left_frame, text="Создать расписку", command=self.save_file).pack(fill='x', pady=5)

        # Правая часть
        ttk.Label(right_frame, text="Телефон заказчика").pack(anchor='w')
        ttk.Entry(right_frame, textvariable=self.client_phone).pack(fill='x', pady=5)

        ttk.Label(right_frame, text="Телефон экспедитора").pack(anchor='w')
        ttk.Entry(right_frame, textvariable=self.expeditor_phone).pack(fill='x', pady=5)

        ttk.Label(right_frame, text="Телефон грузоотправителя").pack(anchor='w')
        ttk.Entry(right_frame, textvariable=self.shipper_phone).pack(fill='x', pady=5)

        ttk.Label(right_frame, text="Телефон грузополучателя").pack(anchor='w')
        ttk.Entry(right_frame, textvariable=self.consignee_phone).pack(fill='x', pady=5)

    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Выберите файл поручения",
            filetypes=[("PDF файлы", "*.pdf"), ("Все файлы", "*.*")]
        )
        if file_path:
            self.load(file_path)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(
            title="Сохранить расписку как",
            defaultextension=".pdf",
            filetypes=[("PDF файлы", "*.pdf"), ("Все файлы", "*.*")],
            initialfile=f"Экспедиторская расписка №{NumCounter.read()}"
        )
        if file_path:
            self.save(file_path)

    def __confirm_zeroize(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите обнулить нумерацию?"):
            self.__zeroize()

    def load(self, path):
        try:
            pdf_parser = PdfParser(path)
            self.parsed_data = pdf_parser.parse(False)
            messagebox.showinfo("Успех", "Поручение загружено.")
        except Exception as e:
            messagebox.showerror("Ошибка", "Не удалось загрузить файл.")
            with open("../logs.txt", "a", encoding='utf-8') as f:
                f.write(f"Failed loading file {path}\nTraceback:\n{traceback.format_exc()}\nError: {e}\n")

    def save(self, path):
        selected_date = self.date_entry.get_date()
        self.parsed_data["document"]["day"] = selected_date.day
        self.parsed_data["document"]["month"] = month_names[int(selected_date.month)]
        self.parsed_data["document"]["year"] = selected_date.year
        self.parsed_data["client"]["phone"] = self.client_phone.get() if self.client_phone.get() != "" else "________________________"
        self.parsed_data["expeditor"]["phone"] = self.expeditor_phone.get() if self.expeditor_phone.get() != "" else "________________________"
        self.parsed_data["shipper"]["phone"] = self.shipper_phone.get() if self.shipper_phone.get() != "" else "________________________"
        self.parsed_data["consignee"]["phone"] = self.consignee_phone.get() if self.consignee_phone.get() != "" else "________________________"
        try:
            generator = HTMLGenerator(self.parsed_data, "template.html")
            filenum = NumCounter.read()
            generator.save(f"temp/file{filenum}.html")
            pdf_maker = PDFMaker(f"temp/file{filenum}.html")
            pdf_maker.save_pdf(path)
            messagebox.showinfo("Успех", "Расписка сохранена.")
        except Exception as e:
            with open("../logs.txt", "a", encoding='utf-8') as f:
                messagebox.showerror("Ошибка", "Не удалось сохранить расписку.")
                f.write(f"Failed saving file {path}\nHTML #{NumCounter.read()}\nTraceback:\n{traceback.format_exc()}\nError: {e}\n")

    @staticmethod
    def __zeroize():
        NumCounter.zeroize()
        messagebox.showinfo("Готово", "Нумерация обнулена.")

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = App(root)
#     root.mainloop()