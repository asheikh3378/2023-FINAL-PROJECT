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

