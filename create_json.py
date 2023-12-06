import json

# Пример данных
car_data = {
    "name": "Tata Indica Vista Aura 1.2 Safire BSIV",
    "year": 2011,
    "km_driven": 70000,
    "fuel": "Petrol",
    "seller_type": "Individual",
    "transmission": "Manual",
    "owner": "Second Owner",
    "mileage": "16.5 kmpl",
    "engine": "1172 CC",
    "max_power": "65 bhp",
    "torque": "96  Nm at 3000  rpm ",
    "seats": 5.0
}

# Указываем имя файла, в который будем сохранять данные
file_name = "car_data_test2.json"

# Записываем данные в файл в формате JSON
with open(file_name, "w") as json_file:
    json.dump(car_data, json_file, indent=2)

print(f"JSON-файл {file_name} успешно создан и сохранен.")
