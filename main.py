from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime

from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas


excel_file = pandas.read_excel("wine.xlsx")
wines = excel_file.to_dict("records")
print(wines)


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
    current_year=datetime.now().year,
    get_years=get_years,
)

with open("index.html", "w", encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(("0.0.0.0", 8000), SimpleHTTPRequestHandler)
server.serve_forever()
