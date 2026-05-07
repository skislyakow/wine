import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime
from collections import defaultdict

from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas


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


def main():
    parser = argparse.ArgumentParser(description="Wine site")
    parser.add_argument(
        "--excel",
        default="wine.xlsx",
        help="Path to the Excel file with wine data (default: wine.xlsx)",
    )
    args = parser.parse_args()

    wine_data = pandas.read_excel(args.excel, keep_default_na=False)
    wine_data = wine_data.replace("NaN", "")
    wine_data = wine_data.fillna("")
    wine_dict = defaultdict(list)

    for index, row in wine_data.iterrows():
        wine_item = row.to_dict()
        wine_dict[row["Категория"]].append(wine_item)

    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html", "xml"]),
    )

    template = env.get_template("template.html")

    rendered_page = template.render(
        wines=wine_dict,
        current_year=datetime.now().year,
        get_years=get_years,
    )

    with open("index.html", "w", encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(("0.0.0.0", 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
