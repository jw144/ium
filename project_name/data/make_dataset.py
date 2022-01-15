# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
import json
import os



def prepare_data(base_data_path, products_path = "/raw/products.jsonl", sessions_path = "/raw/sessions.jsonl", interim_path = "/interim/interim.jsonl", train_path = "/processed/train.csv", eval_path = "/processed/eval.csv", test_path = "/processed/test.csv"):
    products_path = base_data_path + products_path
    sessions_path = base_data_path + sessions_path
    interim_path = base_data_path + interim_path
    train_path = base_data_path + train_path
    eval_path = base_data_path + eval_path
    test_path = base_data_path + test_path

    Path(base_data_path + "/interim").mkdir(exist_ok=True)
    Path(base_data_path + "/processed").mkdir(exist_ok=True)

    product_categories = {}
    product_prices = {}
    category_set = set()
    products_file = open(products_path, 'r')
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

    category_dict = {
        "Okulary 3D": 1,
        "Zestawy głośnomówiące": 2,
        "Odtwarzacze DVD": 3,
        "Anteny RTV": 4,
        "Monitory LCD": 5,
        "Gry PlayStation3": 6,
        "Biurowe urządzenia wielofunkcyjne": 7,
        "Gry komputerowe": 8,
        "Zestawy słuchawkowe": 9,
        "Odtwarzacze mp3 i mp4": 10,
        "Tablety": 11,
        "Telefony stacjonarne": 12,
        "Słuchawki": 13,
        "Gry Xbox 360": 14,
        "Telefony komórkowe": 15
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

        month = int(session_data["timestamp"].split('-')[1])
        product_category = product_categories[session_data["product_id"]]
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

    train_num = (80*line_number)/100
    eval_num = (10*line_number)/100
    test_num = (10*line_number)/100

    counter = 0

    train_file.write("january,february,march,april,may,june,july,august,september,october,november,december,Okulary 3D,Zestawy głośnomówiące,Odtwarzacze DVD,Anteny RTV,Monitory LCD,Gry PlayStation3,Biurowe urządzenia wielofunkcyjne,Gry komputerowe,Zestawy słuchawkowe,Odtwarzacze mp3 i mp4,Tablety,Telefony stacjonarne,Słuchawki,Gry Xbox 360,Telefony komórkowe,price,discount,returned" + "\n")
    eval_file.write("january,february,march,april,may,june,july,august,september,october,november,december,Okulary 3D,Zestawy głośnomówiące,Odtwarzacze DVD,Anteny RTV,Monitory LCD,Gry PlayStation3,Biurowe urządzenia wielofunkcyjne,Gry komputerowe,Zestawy słuchawkowe,Odtwarzacze mp3 i mp4,Tablety,Telefony stacjonarne,Słuchawki,Gry Xbox 360,Telefony komórkowe,price,discount,returned" + "\n")
    test_file.write("january,february,march,april,may,june,july,august,september,october,november,december,Okulary 3D,Zestawy głośnomówiące,Odtwarzacze DVD,Anteny RTV,Monitory LCD,Gry PlayStation3,Biurowe urządzenia wielofunkcyjne,Gry komputerowe,Zestawy słuchawkowe,Odtwarzacze mp3 i mp4,Tablety,Telefony stacjonarne,Słuchawki,Gry Xbox 360,Telefony komórkowe,price,discount,returned" + "\n")

    for line in interim_file:
        counter = counter + 1
        line_data = json.loads(line)

        if (category_dict[line_data["category"]] == 9):
            write_as_CSV(test_file, line_data, category_dict)
        elif (counter > train_num + eval_num):
            write_as_CSV(test_file, line_data, category_dict)
        elif (counter > train_num):
            write_as_CSV(eval_file, line_data, category_dict)
        elif (counter <= train_num):
            write_as_CSV(train_file, line_data, category_dict)




def write_as_CSV(target_file, line_data, category_dict):
    month_one_hot = ["0" if i != line_data["month"]-1 else "1" for i in range(12)]
    target_file.write(','.join(month_one_hot))
    target_file.write(",")
    category_one_hot = ["0" if i != category_dict[line_data["category"]]-1 else "1" for i in range(15)]
    target_file.write(','.join(category_one_hot))
    target_file.write(",")
    target_file.write(str(line_data["price"]) + "," + str(line_data["discount"]) + "," + line_data["returned"] + "\n")







@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
#@click.argument('output_filepath', type=click.Path())
def main(input_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    prepare_data(input_filepath)


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