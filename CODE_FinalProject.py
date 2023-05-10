# CLASS: CIS2348 - 12597
# NAME: ALISSA SHEIKH PSID: 1623953
import csv
from datetime import datetime

# Read ManufacturerList.csv and store the data in a dictionary
manufacturer_data = {}
with open('ManufacturerList.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # skip header row
    for row in csvreader:
        item_id, manufacturer, item_type, damaged = row
        manufacturer_data[item_id] = {
            'manufacturer': manufacturer,
            'item_type': item_type,
            'damaged': damaged,
        }

# Read PriceList.csv and update the dictionary with item prices
with open('PriceList.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # skip header row
    for row in csvreader:
        item_id, price = row
        if item_id in manufacturer_data:
            manufacturer_data[item_id]['price'] = price

# Read ServiceDatesList.csv and update the dictionary with service dates
with open('ServiceDatesList.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # skip header row
    for row in csvreader:
        item_id, service_date_str = row
        if item_id in manufacturer_data:
            service_date = datetime.strptime(service_date_str, '%m/%d/%Y')
            manufacturer_data[item_id]['service_date'] = service_date

# Full inventory report
with open('FullInventory.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['item_id', 'manufacturer', 'item_type', 'price', 'service_date', 'damaged'])
    for item_id in sorted(manufacturer_data.keys()):
        item = manufacturer_data[item_id]
        row = [item_id, item['manufacturer'], item['item_type']]
        if 'price' in item:
            row.append(item['price'])
        else:
            row.append('')
        if 'service_date' in item:
            row.append(item['service_date'])
        else:
            row.append('')
        row.append(item['damaged'])
        csvwriter.writerow(row)

# Item type inventory reports
item_types = set(item['item_type'] for item in manufacturer_data.values())
for item_type in item_types:
    filename = f"{item_type}Inventory.csv"
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['item_id', 'manufacturer', 'price', 'service_date', 'damaged'])
        for item_id in sorted(manufacturer_data.keys()):
            item = manufacturer_data[item_id]
            if item['item_type'] == item_type:
                row = [item_id, item['manufacturer']]
                if 'price' not in item:
                    row.append('')
                else:
                    row.append(item['price'])
                if 'service_date' in item:
                    row.append(item['service_date'])
                else:
                    row.append('')
                row.append(item['damaged'])
                csvwriter.writerow(row)

with open('PastServiceDateInventory.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['item_id', 'manufacturer', 'item_type', 'price', 'service_date', 'damaged'])
    past_service_items = []
    for item_id, item_data in manufacturer_data.items():
        if 'service_date' in item_data and item_data['service_date'].date() < datetime.today().date():
            past_service_items.append((item_id, item_data))


    def get_service_date(item):
        return item[1]['service_date']


    past_service_items.sort(key=get_service_date)

    for item in past_service_items:
        item_id = item[0]
        item_data = item[1]
        row = [item_id, item_data['manufacturer'], item_data['item_type']]
        if 'price' in item_data:
            row.append(item_data['price'])
        else:
            row.append('')
        row.append(item_data['service_date'])
        row.append(item_data['damaged'])
        csvwriter.writerow(row)
with open('DamagedInventory.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['item_id', 'manufacturer', 'item_type', 'price', 'service_date'])
    damaged_items = []
    for item_id, item_data in manufacturer_data.items():
        if item_data['damaged'] == 'damaged':
            damaged_items.append((item_id, item_data))


    def get_price(item):
        return int(item[1]['price'])


    damaged_items.sort(key=get_price, reverse=True)

    for item in damaged_items:
        item_id = item[0]
        item_data = item[1]
        row = [item_id, item_data['manufacturer'], item_data['item_type']]
        if 'price' in item_data:
            row.append(item_data['price'])
        else:
            row.append('')
        if 'service_date' in item_data:
            row.append(item_data['service_date'])
        else:
            row.append('')
        csvwriter.writerow(row)


class Inventory:
    def __init__(self):
        self.items = {}

    def load_items(self, filename):
        with open(filename, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                item_id, manufacturer, item_type, damaged = row
                self.items[item_id.strip()] = {"manufacturer": manufacturer.strip(), "item_type": item_type.strip(),
                                               "damaged": damaged.strip()}

    def load_prices(self, filename):
        with open(filename, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                item_id, price = row
                if item_id in self.items:
                    self.items[item_id.strip()]["price"] = price.strip()

    def load_service_dates(self, filename):
        with open(filename, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                item_id, service_date = row
                if item_id in self.items:
                    self.items[item_id.strip()]["service_date"] = service_date.strip()

    def query_item(self, manufacturer, item_type):
        filtered_items = []
        for item_id, item in self.items.items():
            if item["manufacturer"].lower() == manufacturer.lower() and item[
                "item_type"].lower() == item_type.lower() and not item["damaged"].lower() == "true":
                if "service_date" in item and item["service_date"] != "":
                    # Check if service date is in the future
                    today = datetime.date.today()
                    service_date = datetime.datetime.strptime(item["service_date"], "%m/%d/%Y").date()
                    if service_date < today:
                        continue
                if "price" in item:
                    filtered_items.append(
                        {"item_id": item_id, "manufacturer": item["manufacturer"], "item_type": item["item_type"],
                         "price": float(item["price"])})

        if not filtered_items:
            print("No such item in inventory")
            return None

        def sort_by_price(element):
            return -element["price"]

        filtered_items.sort(key=sort_by_price)
        output_item = filtered_items[0]

        similar_item = None
        min_price_diff = float('inf')
        for item_id, item in self.items.items():
            if item["manufacturer"].lower() != manufacturer.lower() and item["item_type"].lower() == item_type.lower() \
                    and not item["damaged"].lower() == "true":
                if "service_date" in item and item["service_date"] != "":
                    # Check if service date is in the future
                    today = datetime.date.today()
                    service_date = datetime.datetime.strptime(item["service_date"], "%m/%d/%Y").date()
                    if service_date < today:
                        continue
                if "price" in item:
                    price_diff = abs(float(item["price"]) - output_item["price"])
                    if price_diff < min_price_diff:
                        similar_item = {"item_id": item_id, "manufacturer": item["manufacturer"],
                                        "item_type": item["item_type"], "price": float(item["price"])}
                        min_price_diff = price_diff

        print("Your item is: id - {} manufacturer - {} item_type - {} price - ${}".format(output_item["item_id"],
                                                                                          output_item["manufacturer"],
                                                                                          output_item["item_type"],
                                                                                          output_item["price"]))
        if similar_item:
            print("You may also consider: id - {} manufacturer - {} item_type - {} price - ${}".format(
                similar_item["item_id"], similar_item["manufacturer"], similar_item["item_type"],
                similar_item["price"]))


if __name__ == "__main__":
    inventory = Inventory()
    inventory.load_items("ManufacturerList.csv")
    inventory.load_prices("PriceList.csv")
    inventory.load_service_dates("ServiceDatesList.csv")

    while True:
        query = input("Enter manufacturer and item type (q to quit): ")
        if query == "q":
            break

        manufacturer, item_type = query.split()
        inventory.query_item(manufacturer, item_type)
