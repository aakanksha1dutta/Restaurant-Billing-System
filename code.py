import pymysql

db=pymysql.connect(host="localhost", user="binod",password = "mysql") 
MyCur = db.cursor()

databaseName = 'restaurantdb'
orderTableName = "ordersfood"
order_id = 0
billsTableName = "orders"
menuTableName = "menu"

MyCur.execute("use "+databaseName+";")
def select_from_menu():
    # Print everything from the menu
    # Choose from the menu

    print("___Menu___")
    MyCur.execute("select * from menu;")
    data = MyCur.fetchall()

    print("FoodId, Food Name")
    for row in data:
        print(row)

    while True:
        choice = int(input("Pick food item [Enter FoodId]:"))
        for row in data:
            if choice == row[0]:
                break
        else:
            print("Food Item not in List")
            continue
        break
    return choice

def input_list(function):
    ret = []

    cont = 'y'
    while cont in 'yY':
        item = function()
        ret.append(item)

        cont = input("Do you want to continue? [Y/n]")
        while cont not in 'YyNn':
            print('Wrong Input')
            cont = input("Do you want to continue? [Y/n]")
    return ret

def exec(command):
    MyCur.execute(command)# Print everything from the menu
    # Choose from the menu

def add_order():
    global order_id, orderTableName, billsTableName
    # TODO: Customer Name
    customer_name = input("Customer Name:")
    food_items = input_list(function=select_from_menu)
    order_id += 1
    
    exec('INSERT INTO '+billsTableName+' VALUES ('+str(order_id)+',"'+customer_name+'",0);')
    
    for i, food in enumerate(food_items):
        exec("INSERT INTO "+orderTableName+" VALUES ("+str(i)+","+str(food)+","+str(order_id)+");")
    


def main_menu():
    # TODO: Print Starting Text like 'Welcome to Game' + 'To Continue:....
    
    print("1. Add an Order")
    print("2. Show Current Orders")
    print("2. Exit")
    choice  = input("Enter Choice:")
    first = choice[0]
    if choice[0] in 'Aa':
       add_order()
    elif choice[0] in 'Ee':
        print("Thanks for seeing us!") # TODO
        exit()
main_menu()