import re


class HTMLGenerator:
    def __init__(self, data):
        self.data = data
        self.template = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Экспедиторская расписка</title>
    <style>
        body {
            font-family: "Arial", sans-serif;
            font-size: 11px;
            line-height: 1.3;
            color: #000;
            background-color: #f0f0f0;
            margin: 0;
            padding: 20px;
        }
        .page {
            max-width: 900px;
            margin: 0 auto 30px auto;
            background: #fff;
            padding: 30px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h2 {
            text-align: center;
            font-size: 16px;
            margin-top: 0;
            margin-bottom: 20px;
            text-transform: uppercase;
        }
        .text-center { text-align: center; }
        .text-right { text-align: right; }
        .bold { font-weight: bold; }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 15px;
        }
        th, td {
            border: 1px solid #000;
            padding: 6px;
            vertical-align: top;
        }
        th {
            background-color: #e9ecef;
            text-align: center;
            font-weight: bold;
        }
        .no-border-bottom { border-bottom: none; }
        .no-border-top { border-top: none; }

        .flex-row {
            display: flex;
            justify-content: space-between;
            gap: 10px;
            margin-bottom: 15px;
        }
        .flex-col {
            flex: 1;
            border: 1px solid #000;
            padding: 8px;
        }
        .section-title {
            background-color: #d6d8db;
            text-align: center;
            font-weight: bold;
            padding: 4px;
            border: 1px solid #000;
            border-bottom: none;
            margin-top: 15px;
        }

        .signature-block {
            margin-top: 20px;
        }
        .signature-line {
            display: inline-block;
            border-bottom: 1px solid #000;
            width: 150px;
        }

        @media print {
            body { background: none; padding: 0; }
            .page { box-shadow: none; padding: 0; margin-bottom: 0; page-break-after: always; }
        }
    </style>
</head>
<body>

    <!-- ШАБЛОН  -->
    <div class="page">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <h2 style="margin: 0;">Экспедиторская расписка № _ от «__» ____ 202_ г.</h2>
            <!-- IMG LOGO -->
        </div>

        <!-- Стороны: Экспедитор и Клиент -->
        <div class="flex-row" style="margin-bottom: 5px;">
            <div class="flex-col">
                <div class="bold text-center" style="border-bottom: 1px solid #000; margin-bottom: 5px; padding-bottom: 5px;">ИСПОЛНИТЕЛЬ (ЭКСПЕДИТОР)</div>
                <div><b>Организация:</b> {data[expeditor][name]}</div>
                <div>{data[expeditor][inn/kpp]}</div>
                <div><b>Юр. Адрес:</b> {data[expeditor][address]}</div>
                <div><b>Контактное лицо (тел):</b> ________________________</div>
            </div>
            <div class="flex-col">
                <div class="bold text-center" style="border-bottom: 1px solid #000; margin-bottom: 5px; padding-bottom: 5px;">ЗАКАЗЧИК (КЛИЕНТ)</div>
                <div><b>Организация:</b> {data[client][name]}</div>
                <div>{data[client][inn/kpp]}</div>
                <div><b>Юр. Адрес:</b> {data[client][address]}</div>
                <div><b>Контактное лицо (тел):</b> ________________________</div>
            </div>
        </div>

        <!-- Стороны: Отправитель и Получатель -->
        <div class="flex-row">
            <div class="flex-col">
                <div class="bold text-center" style="border-bottom: 1px solid #000; margin-bottom: 5px; padding-bottom: 5px;">ГРУЗООТПРАВИТЕЛЬ (ЗАГРУЗКА)</div>
                <div><b>Организация:</b> {data[shipper][name]}</div>
                <div>{data[shipper][inn/kpp]}</div>
                <div><b>Адрес:</b> {data[shipper][address]}</div>
                <div><b>Время прибытия:</b> {data[shipper][date]}</div>
                <div><b>Контактное лицо (тел):</b> ________________________</div>
            </div>
            <div class="flex-col">
                <div class="bold text-center" style="border-bottom: 1px solid #000; margin-bottom: 5px; padding-bottom: 5px;">ГРУЗОПОЛУЧАТЕЛЬ (ВЫГРУЗКА)</div>
                <div><b>Организация:</b> {data[consignee][name]}</div>
                <div>{data[consignee][inn/kpp]}</div>
                <div><b>Адрес:</b> {data[consignee][address]}</div>
                <div><b>Время прибытия:</b> {data[consignee][date]}</div>
                <div><b>Контактное лицо (тел):</b> ________________________</div>
            </div>
        </div>

        <div class="section-title">ЭКСПЕДИТОРУ ДЛЯ ОРГАНИЗАЦИИ ПЕРЕВОЗКИ ВЫДАЕТСЯ СЛЕДУЮЩИЙ ГРУЗ</div>
        <table>
            <thead>
                <tr>
                    <th>№</th>
                    <th>Груз</th>
                    <th>Кол-во мест</th>
                    <th>
                        <div>Вес</div>
                        <div>брутто, кг</div>
                        <div>нетто. кг</div>
                        <div>тара, кг</div>
                    </th>
                    <th>Вид упаковки</th>
                    <th>Объем, м³</th>
                    <th>Особенности</th>
                </tr>
            </thead>
            <!-- for item in data["cargos"]["items"] -->
            <tbody>
                <tr>
                    <td class="text-right">item["id"]</td>
                    <td class="text-right">item["name"]</td>
                    <td class="text-right">item["places"]</td>
                    <td class="text-right">item["weight"]</td>
                    <td class="text-right"></td>
                    <td class="text-right">item["volume"]</td>
                    <td class="text-right">item["features"]</td>
                </tr>
            </tbody>
        </table>

        <div class="section-title">ОБЪЯВЛЕННАЯ ЦЕННОСТЬ ГРУЗА</div>
        <div class="text-center" style="border: 1px solid #000; border-top: none; padding: 10px;">{data[cargo][total_price]}</div>

        <div class="section-title">ОСОБЫЕ УСЛОВИЯ ПЕРЕВОЗКИ</div>
        <div style="border: 1px solid #000; border-top: none; padding: 10px;">{data[conditions]}</div>

        <div class="section-title">ДОПОЛНИТЕЛЬНО</div>
        <div style="border: 1px solid #000; border-top: none; padding: 10px; margin-bottom: 15px">{data[additional]}</div>

        <div class="flex-row" style="margin-bottom: 15px;">
            <div class="flex-col">
                <div class="bold text-center" style="border-bottom: 1px solid #000; margin-bottom: 5px; padding-bottom: 5px;">СДАЛ (ГРУЗООТПРАВИТЕЛЬ)</div>
                <div style="font-size: 10px; margin-bottom: 10px;">Я подтверждаю, что отправление не содержит предметов, запрещенных к перевозке. С правилами упаковки, условиями оплаты и доставки ознакомлен. С условиями оплаты и доставки согласен</div>
                <div style="margin-bottom: 10px"><b>Ф.И.О.:</b> _________________________________</div>
                <div><b>Подпись:</b> __________________ <b>Дата:</b> ________ <b>М.П.</b></div>
            </div>
            <div class="flex-col">
                <div class="bold text-center" style="border-bottom: 1px solid #000; margin-bottom: 5px; padding-bottom: 5px;">ПРИНЯЛ (ЭКСПЕДИТОР)</div>
                <div style="font-size: 10px; margin-bottom: 20px;">Груз и поручения на обработку приняты к исполнению в соответствии с Федеральным Законом и Договором Транспортной экспедиции.</div>
                <div style="margin-bottom: 10px"><b>Ф.И.О.:</b> _________________________________</div>
                <div><b>Подпись:</b> __________________ <b>Дата:</b> ________ <b>М.П.</b></div>
            </div>
        </div>

        <div class="section-title">АКТ ПРИЕМА-ПЕРЕДАЧИ (ЗАПОЛНЯЕТСЯ ПРИ ВЫГРУЗКЕ ПОЛУЧАТЕЛЮ)</div>
        <div style="border: 1px solid #000; border-top: none; padding: 10px;">
            <p>Мы, нижеподписавшиеся, составили настоящий акт о том, что груз принят <b>без претензий к внешнему виду и весу</b>.<br>
            Принято в количестве: ______ мест, общим весом: ______ кг.</p>
            <p>Документ, удостоверяющий полномочия получателя: ______________________________________________________________</p>

            <div style="display: flex; justify-content: space-between; margin-top: 20px;">
                <div><b>От лица Экспедитора:</b> __________________ <b>М.П.</b> <br><br><b>Дата сдачи:</b> «___» ________ 202_ г.</div>
                <div><b>От лица Получателя:</b> __________________ <b>М.П.</b><br><br><b>Ф.И.О.:</b> ___________________________________</div>
            </div>
        </div>
    </div>

</body>
</html>"""

    def save(self, filename):
        """Обрабатывает шаблон и сохраняет результат в HTML-файл."""
        html = self.template
        html = self._process_loop(html)
        html = self._replace_placeholders(html)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)

    def _process_loop(self, template):
        """Находит блок с циклом по грузам и заменяет его на множество строк <tr>."""
        start = template.find("<!-- for")
        if start == -1:
            return template

        end = template.find("</tbody>", start)
        if end == -1:
            return template
        end += len("</tbody>")

        block = template[start:end]

        # Извлекаем шаблон одной строки <tr> ... </tr>
        tr_start = block.find("<tr>")
        tr_end = block.rfind("</tr>") + len("</tr>")
        tr_template = block[tr_start:tr_end]

        items = self.data["cargo"]["items"]
        rows = []
        for item in items:
            row = tr_template
            # Заменяем все вхождения item["ключ"] на значение из текущего элемента
            def repl_item(match):
                key = match.group(1)
                return str(item.get(key, ''))
            row = re.sub(r'item\["([^"]+)"\]', repl_item, row)
            rows.append(row)

        rows_str = "\n".join(rows)
        new_block = "<tbody>\n" + rows_str + "\n</tbody>"
        return template.replace(block, new_block)

    def _replace_placeholders(self, template):
        """Заменяет все плейсхолдеры вида {data[ключ]} и {data[ключ][подключ]}."""
        # Двухуровневые
        def repl_two(match):
            outer = match.group(1)
            inner = match.group(2)
            return str(self.data[outer][inner]) if self.data[outer][inner] else "—"
        template = re.sub(r'\{data\[([^\]]+)\]\[([^\]]+)\]\}', repl_two, template)

        # Одноуровневые
        def repl_one(match):
            key = match.group(1)
            return str(self.data[key]) if self.data[key] else "—"
        template = re.sub(r'\{data\[([^\]]+)\]\}', repl_one, template)

        return template