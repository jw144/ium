import json
from project_name.data.make_dataset import prepare_data, create_CSV_string


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


def take_and_format_user_input():
    month = int(input("Enter month (1-12): "))
    category = input("Enter category (name with polish letters): ")
    price = float(input("Enter price: "))
    discount = int(input("Enter discount: "))
    data = {
        "month": month,
        "category": category,
        "price": price,
        "discount": discount,
        "returned": "False"
    }
    record = create_CSV_string(data, category_dict)
    return record


def take_input_file_data():
    filepath = input("Enter path to file: ")
    records = prepare_data("", True, filepath)
    return records


def choice_1():
    record = take_and_format_user_input()
    records = []
    records.append(record)
    result = model_placeholder_1(records)
    print("Model classification: ")
    print(result)

def choice_2():
    record = take_and_format_user_input()
    records = []
    records.append(record)
    result = model_placeholder_2(records)
    print("Model classification: ")
    print(result)

def choice_3():
    return 0

def choice_4():
    return 0

def choice_5():
    return 0

def model_placeholder_1(records):
    return "model 1"

def model_placeholder_2(records):
    return "model 2"


user_response = 0


while (user_response != 6):
    user_response = int(input("What would you like to do?\n1) Make a single prediction using model 1\n2) Make a single prediction using model 2\n3) Make multiple predictions with data from file using model 1\n4) Make multiple predictions with data from file using model 2\n5) Run comparison test and show performance data\n6) Exit the program\n\n"))

    if(user_response == 1):
        choice_1()
    elif(user_response == 2):
        choice_2()
    elif(user_response == 3):
        choice_3()
    elif(user_response == 4):
        choice_4()
    elif(user_response == 5):
        choice_5()

