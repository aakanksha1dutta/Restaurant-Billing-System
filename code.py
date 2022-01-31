import pymysql

db=pymysql.connect(host="localhost", user="binod",password = "mysql") 
MyCur = db.cursor()

databaseName = 'restaurantdb'
orderTableName = "ordersfood"
order_id = 0
billsTableName = "orders"
menuTableName = "menu"

# User Defined Functions/Methods
def initialise():
    """
    Initialise values into the database
    """
    global db
    exec(f"create database {databaseName};")
    exec(f"use {databaseName};")

    exec(f"drop table if exists {billsTableName};")
    exec(f"drop table if exists {orderTableName};")
    exec(f"drop table if exists {menuTableName};")

    exec(f"CREATE TABLE {billsTableName}(ORDERID INT, CUSTOMER_NAME CHAR(100))")
    exec(f"CREATE TABLE {orderTableName}(S_NO INT, FoodID INT, QTY INT, OrderID INT)")
    exec(f"CREATE TABLE {menuTableName} (FoodID INT, Food_Name CHAR(100), Price DECIMAL(7,2))")

    exec(f"INSERT INTO {menuTableName} VALUES (1, 'Chicken Tacos', 570),(2, 'Cheese Pizza', 850),(3, 'Apple Pie', 340),(4, 'Veg Lasagna', 680),(5, 'Dark Mousse', 360)")
    db.commit()

def iinput(text,accept_float=False):
    """
    A separate function for saving only numerical values from the user. 
    """
    while True:
        try:
            if accept_float:
                ret = float(input(text))
            else:
                ret = int(input(text))
            if ret < 0:
                print("Input number is negative!")
                continue
        except ValueError:
            print("Input value is not a number")
        except:
            print("Error during input!")
        else:
            break
    return ret

def select_from_menu():
    """
    Function for requesting list of items from the menu.
    """


    print("*"*10,"Menu","*"*10)
    MyCur.execute("SELECT * FROM menu;")
    data = MyCur.fetchall()

    print("FoodId\t\t Item Name\t\t Price")
    for row in data:
        print(*row,sep="\t\t")
    print()
    while True:
        choice = iinput("Pick food item [Enter FoodId]: ")
        quantity = iinput("Enter Quantity: ")
        for row in data:
            if choice == row[0]:
                break
        else:
            print("Food Item not in List")
            continue
        break
    return choice, quantity


def input_list(function):
    """
    A separate function to input values as list from the user. This function was created to minimize code organization.
    """

    ret = []

    cont = 'y'
    while cont in 'yY':
        item = function()
        ret.append(item)

        cont = input("Do you want to add more items? [Y/n] ")

        while cont not in 'YyNn':
            print('Wrong Input')
            cont = input("Do you want to add more items? [Y/n] ")
    return ret

def exec(command):
    """
    Useful for debugging mysql functions, and reduces redundant code.
    """
    # print(command) # for debugging
    MyCur.execute(command)

def createorder():
    """
    Function to make an order in the database.
    """
    global order_id, orderTableName, billsTableName
    
    customer_name = input("Customer Name: ").strip()
    food_items = input_list(function=select_from_menu) #list of foodids
    
    food_dict = {}
    for food, qty in food_items:
        if food in food_dict:
            food_dict[food] += qty 
        else:
            food_dict[food] = qty
    while True:
        
        exec(f"SELECT EXISTS(SELECT * FROM {orderTableName} WHERE orderid={order_id}) AS EXIST;") # Checks whether the input orderid exists?
        data = MyCur.fetchall()[0][0]
        if data == 0:
            exec(f'INSERT INTO {billsTableName} VALUES ({order_id},"{customer_name}");')
            break
        order_id += 1
    print(f"Your order id is {order_id}") 
    for i, (food, qty) in enumerate(food_dict.items()):
        exec(f'INSERT INTO {orderTableName} VALUES ({i},"{food}",{qty},{order_id});')

    db.commit()


def editorder():
    """
    Function to edit current orders in the database.
    """
    orderid = showorder(return_values="orderid")
    exec(f"SELECT a.FoodId, QTY from {orderTableName} a, {menuTableName} b where a.FoodId = b.FoodId and a.orderid = {orderid};")
    food_items = MyCur.fetchall()

    food_dict = {}
    for food, qty in food_items:
        if food in food_dict:
            food_dict[food] += qty 
        else:
            food_dict[food] = qty

    
    food_items = input_list(function=select_from_menu) #list of foodids
    for food, qty in food_items:
        if food in food_dict:
            food_dict[food] += qty 
        else:
            food_dict[food] = qty
    
    exec(f"DELETE FROM {orderTableName} WHERE orderid = {orderid}")

    for i, (food, qty) in enumerate(food_dict.items()):
        if qty <= 0:
            continue
        exec(f'INSERT INTO {orderTableName} VALUES ({i},"{food}",{qty},{orderid});')

    db.commit()
    

def showorder(return_values=None):
    """
    Shows all the current orders from the database
    """
    print("Select OrderId from the database:")
    exec(f"SELECT * from {billsTableName};")
    data = MyCur.fetchall()
    print("OrderId\t Name")
    for row in data:
        orderid, name  = row
        print(orderid, name,sep="\t")

    while True:
        order_condition = iinput("Enter ORDERID: ")

        exec(f"SELECT EXISTS(SELECT * FROM {orderTableName} WHERE orderid={order_condition}) AS EXIST;") # Checks whether the input orderid exists?
        data = MyCur.fetchall()[0][0]
        if data == 0:
            print("OrderId doesn't exists")
            continue
        
        exec(f"SELECT Food_Name, QTY, Price from {orderTableName} a, {menuTableName} b where a.FoodId = b.FoodId and a.orderid = {order_condition};")
        data = MyCur.fetchall()

        print("Name\t Qty.\t Cost\t Price")
        amount = 0
        for food, qty, price in data:
            print(food,qty, price, price*qty,sep="\t")
            amount+=price*qty
        print(f"Total amount: {amount}")
        break
    
    if return_values == "amount":
        return amount
    elif return_values == "orderid":
        return order_condition
    else:
        input("Press Enter to continue: ")


def finalbill():
    """
    Function to proceed with the transcation.
    """
    amount = showorder(return_values="amount")
    print("\n"*2)
    print(f"\tYour total amount is {amount}")

    while True:
        paid = iinput("\tHow much did customer pay? ",accept_float=True)
        if paid < amount:
            print("Cash paid is less than total amount") 
            continue
        break
    print(f"Change: {(paid)-float(amount)}")
    print("Transaction Successful!!")


def main_menu():
    """
    Navigate through all the functions using a simple menu-based system.
    """
    print("Welcome to AutoRestro- your very own automated restaurant billing system.")
    print("Choose your desired task for today—------->")

    while True:
        print("""
        1. Make an Order
        2. Show Customer's Order
        3. Edit Existing Orders
        4. Print Customer's Bill
        5. Exit
        """)
        choice = iinput("Enter Choice: ")
        first = choice
        if choice == 1:
            createorder()
        elif choice == 2:
            showorder()
        elif choice == 3:
            editorder()
        elif choice == 4:
            finalbill()
        elif choice == 5:
            print("Have a wonderful day ahead! Exiting…") 
            return
        else:
            print("Wrong input!")


# Main Code
initialise()
main_menu()

print("Bye!")