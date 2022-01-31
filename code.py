import pymysql

db=pymysql.connect(host="localhost", user="binod",password = "mysql") 
MyCur = db.cursor()

databaseName = 'restaurantdb'
orderTableName = "ordersfood"
order_id = 0
billsTableName = "orders"
menuTableName = "menu"

MyCur.execute("use "+databaseName+";")

#sql code for the tables
exec(f"CREATE TABLE {billsTableName}(ORDERID INT, CUSTOMER_NAME CHAR(10)")
exec(f"CREATE TABLE {orderTableName}(S_NO INT, FoodID INT, QTY INT, OrderID INT)")
exec(f"CREATE TABLE {menuTableName} (FoodID INT, Food_Name CHAR(10), Price DECIMAL(7,2)")


#menudata
exec(f"INSERT INTO {menuTableName} VALUES (),(),(),(),(),()") #entertabledata

def select_from_menu():
    # Print everything from the menu
    # Choose from the menu

    print("___Menu___")
    MyCur.execute("select * from menu;")
    data = MyCur.fetchall()

    print("FoodId, Food Name, Price")
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
    return choice #returns foodid


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
    food_items = input_list(function=select_from_menu) #list of foodids
    order_id += 1
    
    exec('INSERT INTO '+billsTableName+' VALUES ('+str(order_id)+',"'+customer_name+'",0);')
    
    for i, food in enumerate(food_items):
        exec("INSERT INTO "+orderTableName+" VALUES ("+str(i)+","+str(food)+","+str(order_id)+");")

def finalbill():
    MyCur.execute("select * from {billsTableName};")
    data = MyCur.fetchall()
    for row in data:
        print(row)

    while True:
        order_condition = input("Enter ORDERID:")
        for row in data:
            if order_condition == row[0]:
                exec(f"SELECT foodID, FoodName,QTY, Price from {orderTableName} a,{menuTableName} b where a.orderid = b.orderid group by a.orderid having orderid = {order_condition}")
                for row in MyCur.fetchall:
                    print(row)
                break
        else:
            print("OrderID not in List")
            continue
        break

    

def main_menu():
    # TODO: Print Starting Text like 'Welcome to Game' + 'To Continue:....
    
    print("1. Add an Order")
    print("2. Show Current Orders")
    print("3. Print Bill")
    print("4. Exit")
    choice  = input("Enter Choice:")
    first = choice
    if choice == '1':
       add_order()
    elif choice == '2':
        #show current orders
    elif choice == '3':
        #print final bill
    elif choice == '4' :
        print("Thanks for seeing us!") # TODO
        exit()
main_menu()