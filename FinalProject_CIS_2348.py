# Joshua Chan
# 1588459
import datetime

items_list = []
manufacturer_file = input("Enter the filename of Manufacturers List")
with open(manufacturer_file) as file:
    data = file.readlines()
    for row in data:
        row_dict = dict()
        fields = row.split(',')
        row_dict['item_id'] = fields[0]
        row_dict['manufacturer_name'] = fields[1]
        row_dict['item_type'] = fields[2]
        row_dict['damaged_ind'] = fields[3].replace('\n', '')
        items_list.append(row_dict)
# The code above will accept the input and open the corresponding file and add items to a dictionary
price_file = input("Enter the filename with Price data:")
with open(price_file) as file:
    data = file.readlines()
    for row in data:
        fields = row.split(',')
        for item in items_list:
            if item['item_id'] == fields[0]:
                item['price'] = int(fields[1].replace('\n', ''))
# The code above will accept the input and open the corresponding file and add items to a dictionary
service_file = input("Enter the filename of Service Date List")
with open(service_file) as file:
    data = file.readlines()
    for row in data:
        fields = row.split(',')
        for item in items_list:
            if item['item_id'] == fields[0]:
                item['service_date'] = fields[1].replace('\n', '')
# The code above will accept the input and open the corresponding file and add items to a dictionary
items_list = sorted(items_list, key=lambda i: i['manufacturer_name'])

with open('FullInventory.csv', 'w') as inventory_file:
    for item in items_list:
        inventory_file.write(
            item['item_id'] + ',' + item['manufacturer_name'] + ',' + item['item_type'] + ',' + str(
                item['price']) + ',' +
            item['service_date'] + ',' + item['damaged_ind'] + '\n')
# The code above will create the FullInventory file and add the item ID, Manufacturer name, type, price, service date, and if it is damaged
items_by_their_types = dict()

for item in items_list:
    if item['item_type'] not in items_by_their_types:
        items_by_their_types[item['item_type']] = []


for type in items_by_their_types:
    file_name = type + 'Inventory.csv'
    with open(file_name, 'w') as file:
        for item in items_list:
            if item['item_type'] == type:
                items_by_their_types[item['item_type']].append(item)
                file.write(
                    item['item_id'] + ',' + item['manufacturer_name'] + ',' + str(item[
                                                                                      'price']) + ',' + item[
                        'service_date'] + ',' + item['damaged_ind'] + '\n')

CurrentDate = str(datetime.datetime.now())[:10]
CurrentDate = datetime.datetime.strptime(CurrentDate, "%Y-%m-%d")

items_expired = []
with open('PastServiceDateInventory.csv', 'w') as file:
    sorted_by_date = sorted(items_list, key=lambda i: i['service_date'])
    for item in sorted_by_date:
        ExpectedDate = item['service_date']
        ExpectedDate = datetime.datetime.strptime(ExpectedDate, "%m/%d/%Y")
        if ExpectedDate <= CurrentDate:
            items_expired.append(item['item_id'])
            file.write(
                item['item_id'] + ',' + item['manufacturer_name'] + ',' + item['item_type'] + ',' + str(item[
                                                                                                            'price']) + ',' +
                item['service_date'] + ',' + item['damaged_ind'] + '\n')
# Above will create a file for items that are past their service date
print(items_expired)

with open('DamagedInveentory.csv', 'w') as file:
    sorted_by_price = sorted(items_list, key=lambda i: i['price'], reverse=True)
    for item in sorted_by_price:
        if item['damaged_ind'] == 'damaged':
            file.write(
                item['item_id'] + ',' + item['manufacturer_name'] + ',' + item['item_type'] + ',' + str(item[
                                                                                                            'price']) + ',' +
                item['service_date'] + '\n')
# Above will create a file for damaged items
while 1:
    manufacturer = input("Enter the manufacturer: ")
    item_type = input("Enter the item_type: ")

    items_list = sorted(items_list, key=lambda i: i['price'], reverse=True)
    found = False
    found_item = None
    for item in items_list:
        if manufacturer in item['manufacturer_name'] and item_type == item['item_type'] and item[
            'damaged_ind'] != 'damaged' and item['item_id'] not in items_expired:
            found = True
            found_item = item
            print('Your Item is:',item['item_id'],item['manufacturer_name'],item['item_type'], item['price'])
# The inputs above will take the user's requirements and find a product for them
    if not found:
        print('No such Item in inventory')
    elif item_type in items_by_their_types:
        closest_item = items_by_their_types[item_type][0]
        for item in items_by_their_types[item_type]:
            if item['damaged_ind'] != 'damaged' and item['item_id'] not in items_expired and item['price']-found_item['price']<closest_item['price']:
                print('Your may consider:',item['item_id'],item['manufacturer_name'],item['item_type'], item['price'])
                break
# If a product is not found then it will print no such item in inventory, a recommendation will be given as well which is similar to the first
    choice = input("'q' to quit")
    if choice == 'q':
        break
# q will terminate the program