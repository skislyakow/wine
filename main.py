from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime
from pprint import pprint

from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas


excel_file = pandas.read_excel("wine.xlsx")
wine2_file = pandas.read_excel("wine2.xlsx", keep_default_na=False)
wine2_file = wine2_file.replace("NaN", "")
wine2_file = wine2_file.fillna("")
wine_dict = {}
grouped = wine2_file.groupby("Категория")
for category, group in grouped:
    wines_in_category = group.to_dict("records")
    wine_dict[category] = wines_in_category


wines = excel_file.to_dict("records")
# print(wines)
print("Итоговая структура продукции:")
pprint(wine_dict)


def get_years(years):
    last_two_digit = years % 100
    if 11 <= last_two_digit <= 14:
        return "лет"

    last_digit = years % 10
    if last_digit == 1:
        return "год"
    if 2 <= last_digit <= 4:
        return "года"

    return "лет"


env = Environment(
    loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
)

template = env.get_template("template.html")

rendered_page = template.render(
    # cap1_title="Красная кепка",
    # cap1_text="$ 100.00",
    # cap2_title="Чёрная кепка",
    # cap2_text="$ 120.00",
    # cap3_title="Ещё одна чёрная кепка",
    # cap3_text="$ 90.00",
    wines=wines,
    current_year=datetime.now().year,
    get_years=get_years,
)

with open("index.html", "w", encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(("0.0.0.0", 8000), SimpleHTTPRequestHandler)
server.serve_forever()
