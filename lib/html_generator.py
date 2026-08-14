import re


class HTMLGenerator:
    def __init__(self, data: dict, html_path: str):
        self.data = data
        with open(html_path, 'r', encoding='utf-8') as f:
            self.template = f.read()

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