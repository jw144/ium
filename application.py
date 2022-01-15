import json
from project_name.data.make_dataset import prepare_data, create_CSV_list
import pickle
from project_name.models.predict_model import predict

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
    record = create_CSV_list(data, category_dict)
    return record


def take_input_file_data():
    filepath = input("Enter path to file: ")
    records = prepare_data("", True, filepath)
    return records


def choice_1():
    record = take_and_format_user_input()
    records = []
    records.append(record)
    result = predict(model1, records)
    print("Model classification: ")
    print(result[1])

def choice_2():
    record = take_and_format_user_input()
    records = []
    records.append(record)
    result = predict(model2, records)
    print("Model classification: ")
    print(result[1])

def choice_3():
    records = take_input_file_data()
    results = predict(model1, records)
    print("Model classification: ")
    print(results[1])

def choice_4():
    records = take_input_file_data()
    results = predict(model2, records)
    print("Model classification: ")
    print(results[1])

def choice_5():
    return 0



user_response = 0

with open("models/bayes.pkl", 'rb') as file:
    model1 = pickle.load(file)

with open("models/forest.pkl", 'rb') as file:
    model2 = pickle.load(file)

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

