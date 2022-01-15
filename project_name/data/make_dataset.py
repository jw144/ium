# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
import json


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    main()


def dummy_sum(a, b):
    """Used exclusively to showcase relative imports in tests. See
       tests/test_make_dataset.py in the repo.
    """
    return a + b


def prepare_data(products_path = "../../data/raw/products.jsonl", sessions_path = "../../data/raw/sessions.jsonl", interim_path = "../../data/interim/interim.jsonl", train_path = "../../data/processed/train.csv", eval_path = "../../data/processed/eval.csv", test_path = "../../data/processed/test.csv"):
    product_categories = {}
    product_prices = {}
    category_set = set()
    products_file = open(products_path, 'r')         #potencjalnie argumenty?
    for line in products_file:
        product_data = json.loads(line)
        product_id = product_data["product_id"]
        product_category = product_data["category_path"].split(';')[-1]
        product_price = product_data["price"]
        product_categories.update({product_id: product_category})
        product_prices.update({product_id: product_price})
        category_set.add(product_category)

    products_file.close()
    sessions_file = open(sessions_path, 'r')
    interim_file = open(interim_path, 'w')

    last_line_buy = False

    month_list = ["error", "100000000000", "010000000000", "001000000000", "000100000000", "000010000000", "000001000000", "000000100000", "000000010000", "000000001000", "000000000100", "000000000010", "000000000001"]
    category_dict = {
        "Okulary 3D": "100000000000000",
        "Zestawy głośnomówiące": "010000000000000",
        "Odtwarzacze DVD": "001000000000000",
        "Anteny RTV": "000100000000000",
        "Monitory LCD": "000010000000000",
        "Gry PlayStation3": "000001000000000",
        "Biurowe urządzenia wielofunkcyjne": "000000100000000",
        "Gry komputerowe": "000000010000000",
        "Zestawy słuchawkowe": "000000001000000",
        "Odtwarzacze mp3 i mp4": "000000000100000",
        "Tablety": "000000000010000",
        "Telefony stacjonarne": "000000000001000",
        "Słuchawki": "000000000000100",
        "Gry Xbox 360": "000000000000010",
        "Telefony komórkowe": "000000000000001"
    }

    for line in sessions_file:
        session_data = json.loads(line)
        if (last_line_buy):
            if (session_data["event_type"] == "RETURN_PRODUCT"):
                returned = "True"
            else:
                returned = "False"

            dataline = {
                "month": month,
                "category": product_category,
                "price": product_price,
                "discount": offered_discount,
                "returned": returned
            }
            interim_file.write(json.dumps(dataline) + "\n")

        if (session_data["event_type"] == "VIEW_PRODUCT"):
            last_line_buy = False
            continue
        elif (session_data["event_type"] == "BUY_PRODUCT"):
            last_line_buy = True
        elif (session_data["event_type"] == "RETURN_PRODUCT"):
            last_line_buy = False
            continue

        month = month_list[int(session_data["timestamp"].split('-')[1])]
        product_category = category_dict[product_categories[session_data["product_id"]]]
        product_price = product_prices[session_data["product_id"]]
        offered_discount = session_data["offered_discount"]

    sessions_file.close()
    interim_file.close()
    interim_file = open(interim_path, 'r')
    line_number = sum(1 for line in interim_file)
    interim_file.close()

    train_file = open(train_path, 'w')
    eval_file = open(eval_path, 'w')
    test_file = open(test_path, 'w')
    interim_file = open(interim_path, 'r')

    train_num = (70*line_number)/100
    eval_num = (15*line_number)/100
    test_num = (15*line_number)/100

    counter = 0

    train_file.write("month,category,price,discount,returned" + "\n")
    eval_file.write("month,category,price,discount,returned" + "\n")
    test_file.write("month,category,price,discount,returned" + "\n")

    for line in interim_file:
        counter = counter + 1
        line_data = json.loads(line)

        if (line_data["category"] == "000000001000000"):
            write_as_CSV(test_file, line_data)
        elif (counter > train_num + eval_num):
            write_as_CSV(test_file, line_data)
        elif (counter > train_num):
            write_as_CSV(eval_file, line_data)
        elif (counter <= train_num):
            write_as_CSV(train_file, line_data)




def write_as_CSV(target_file, line_data):
    target_file.write(line_data["month"] + "," + line_data["category"] + "," + str(line_data["price"]) + "," + str(line_data["discount"]) + "," + line_data["returned"] + "\n")