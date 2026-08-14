import pdfplumber

class PdfParser:
    def __init__(self, filename):
        self.all_text = ""
        self.all_rows = []
        self.filename = filename
        self.data = {
            "document": {},
            "client": {},
            "expeditor": {},
            "shipper": {},
            "consignee": {},
            "cargo": {"items": []},
            "conditions": {},
            "additional": {}
        }

    def _extract(self, debug):
        with pdfplumber.open(self.filename) as pdf:
            for page in pdf.pages:
                self.all_text = page.extract_text()
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        clear_row = []
                        for cell in row:
                            if cell is not None and cell != "":
                                clear_row.append(cell)
                        if len(clear_row) > 0:
                            self.all_rows.append(clear_row)
        if debug:
            print("EXTRACTED:")
            for i, row in enumerate(self.all_rows):
                print(i, ":", row)

    def parse(self, debug) -> dict:
        self._extract(debug)

        first_client_expeditor = False
        for i, row in enumerate(self.all_rows):

            #============================= Клиент/Экспедитор =============================
            if row[0] == 'Клиент' and first_client_expeditor:
                client = self.all_rows[i + 1][0].split('\n')
                expeditor = self.all_rows[i + 1][1].split('\n')
                self.data["client"]["name"] = client[0]
                self.data["client"]["inn/kpp"] = client[1]
                self.data["client"]["address"] = str(self.all_rows[i + 2][0]).replace('\n', ' ')
                self.data["expeditor"]["name"] = expeditor[0]
                self.data["expeditor"]["inn/kpp"] = expeditor[1]
                self.data["expeditor"]["address"] = str(self.all_rows[i + 2][1]).replace('\n', ' ')
            elif row[0] == 'Клиент' and not first_client_expeditor:
                first_client_expeditor = True
                self.data["document"]["name"] = self.all_rows[i + 2][0]


            #============================= Грузополучатель/Грузоотправитель =============================
            if row[0] == 'Грузоотправитель': # в имя пишется инн/кпп
                shipper = self.all_rows[i + 1][0].split('\n')
                consignee= self.all_rows[i + 1][1].split('\n')

                self.data["shipper"]["name"] = shipper[0]
                self.data["shipper"]["inn/kpp"] = shipper[1]
                self.data["consignee"]["name"] = consignee[0]
                self.data["consignee"]["inn/kpp"] = consignee[1]

                self.data["shipper"]["address"] = str(self.all_rows[i + 2][0]).replace('\n', ' ')
                self.data["consignee"]["address"] = str(self.all_rows[i + 2][1]).replace('\n', ' ')

                self.data["shipper"]["date"] = self.all_rows[i + 3][0]
                self.data["consignee"]["date"] = self.all_rows[i + 3][1]


            #============================= Особые условия =============================
            if row[0] == 'Особые условия\nперевозки':
                self.data["conditions"] = row[1]


            #============================= Грузы =============================
            if row[0] == 'Грузы':
                self.data["cargo"]["total_items"] = self.all_rows[i + 1][1]
                self.data["cargo"]["total_weight"] = self.all_rows[i + 1][3]
                self.data["cargo"]["total_price"] = str(self.all_rows[i + 1][5]).replace('\n', ' ')

                cargo_row = i + 3
                while self.all_rows[cargo_row][0].isdigit():
                    item = {
                        "id": self.all_rows[cargo_row][0],
                        "name": self.all_rows[cargo_row][1],
                        "places": self.all_rows[cargo_row][2],
                        "weight": self.all_rows[cargo_row][3].split('\n'),
                        "volume": self.all_rows[cargo_row][4],
                        "features": self.all_rows[cargo_row][-1].replace('\n', ' ') if self.all_rows[cargo_row][-1] else "",
                    }
                    self.data["cargo"]["items"].append(item)
                    cargo_row += 1


            #============================= Дополнительно =============================
            if row[0] == 'Дополнительно':
                self.data["additional"] = self.all_rows[i + 1]


        return self.data
