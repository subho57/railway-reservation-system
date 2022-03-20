from dotenv import dotenv_values
import mysql.connector as mysql
import os

config = dotenv_values(".env")  # take environment variables from .env.

db = mysql.connect(pool_name="railway_pool", pool_size=30, **config)

def get_cursor(isAssociative: bool = False) -> mysql.cursor:
    return db.cursor(dictionary=isAssociative)

def clear_screen() -> None:
    os.system('cls||clear')

def create_user(name: str) -> int:
    cursor = get_cursor()
    cursor.execute("INSERT INTO user (name) VALUES ('" + name + "')")
    db.commit()
    return cursor.lastrowid

def show_ticket(ticket_id: int) -> None:
    clear_screen()
    cursor = get_cursor(True)
    cursor.execute("SELECT t.id, tr.name, s.name as source, d.name as destination, tr.time, tr.fare, t.amount, tr.addon_type, tr.addon_amount, t.seats, t.payment_mode, t.datetime, u.name as user, u.id as user_id FROM ticket as t, user as u, train as tr, station as s, station as d WHERE t.id = " + str(ticket_id) + " AND t.user = u.id AND t.train = tr.id AND tr.source = s.id AND tr.destination = d.id")
    ticket = cursor.fetchone()
    print("----------------- TICKET DETAILS -----------------")
    print("Ticket ID: #", ticket["id"])
    print("Train: ", ticket["name"])
    print("Source: ", ticket["source"])
    print("Destination: ", ticket["destination"])
    print("Datetime: ", ticket["datetime"])
    print("Seats: ", ticket["seats"])
    print("Fare: ", ticket["fare"])
    if(ticket["addon_type"] != 0):
        print("Addon: ", ticket["addon_type"], ": ", ticket["addon_amount"])
    print("Total Amount: ", ticket["seats"], "x (", ticket["fare"], "+", ticket["addon_amount"], ") = Rs.", ticket["amount"])
    print("Payment Mode: ", ticket["payment_mode"])
    print("User ID: #", ticket["user_id"])
    print("User: ", ticket["user"])
    print("-----------------------------------------------------")
    input("Press enter to continue...")
    
def show_all_tickets(user_id: int) -> None:
    clear_screen()
    cursor = get_cursor(True)
    cursor.execute("SELECT id FROM ticket WHERE user = " + str(user_id) + " ORDER BY booking_time DESC")
    ticket_ids = cursor.fetchall()
    if len(ticket_ids) == 0:
        print("No tickets found!")
        input("Press enter to continue...")
        return
    for ticket_id in ticket_ids:
        show_ticket(ticket_id["id"])

def book_ticket() -> None:
    clear_screen()
    cursor = get_cursor()
    print("----------------- BOOK TICKET -----------------")
    print("Enter the following details:")
    print("Enter User ID or Name (if not registered):")
    id_name = input()
    try:
        uid = int(id_name)
        cursor.execute("SELECT id FROM user WHERE id = " + str(uid))
        if len(cursor.fetchall()) == 0:
            print("User not found!")
            input("Press enter to continue...")
            return
    except:
        uid = create_user(id_name)
    print('Select the train:')
    cursor = get_cursor(True)
    cursor.execute("SELECT t.id, t.name, s.name as source, d.name as destination, time, fare, addon_type, addon_amount FROM train as t, station as s, station as d WHERE t.source = s.id AND t.destination = d.id ORDER BY time")
    train_details = [[], [], [], [], []]
    for train in cursor.fetchall():
        print(train["id"], ": ", train["name"], " from ", train["source"], " to ", train["destination"], " at ", train["time"], " for Rs.", train["fare"], "(", train["addon_type"], ": ", train["addon_amount"], ")")
        train_details[0].append(train["id"])
        train_details[1].append(train["time"])
        train_details[2].append(train["fare"])
        train_details[3].append(train["addon_type"])
        train_details[4].append(train["addon_amount"])
    try:
        tid = int(input("Enter train ID: "))
    except:
        print("Invalid train ID")
        return
    if (tid not in train_details[0]):
        print("Invalid train ID")
        return
    date_input = input("Enter date (YYYY-MM-DD): ")
    selected_train_index = train_details[0].index(tid)
    timestamp = date_input + " " + str(train_details[1][selected_train_index])
    seat_count = int(input("Enter no. of seats: "))
    amount = train_details[2][selected_train_index] * seat_count
    payment_mode = input("Enter payment mode (cash/card/wallet/upi): ")
    print('Avail Addon? (Y/n)')
    ch = input()
    if ch == "y" or ch == "Y" or ch == "yes" or ch == "Yes":
        addon = 1
        amount += train_details[4][selected_train_index] * seat_count
    else:
        addon = 0
    cursor.execute("INSERT INTO ticket (user, train, datetime, seats, payment_mode, amount, addon) VALUES (" + str(uid) + ", " + str(tid) + ", '" + timestamp + "', " + str(seat_count) + ", '" + payment_mode + "', " + str(amount) + ", " + str(addon) + ")")
    db.commit()
    print("Ticket booked successfully!")
    show_ticket(cursor.lastrowid)


def main():
    while(True):
        clear_screen()
        print("----------------- WELCOME TO RAILWAY MANAGEMENT SYSTEM -----------------")
        print("1. Book Ticket")
        print("2. See all tickets")
        print("3. Exit")
        try:
            choice = int(input("Enter your choice[1 - 3]: "))
        except:
            print("Invalid choice")
            continue
        if (choice == 1):
            book_ticket()
        elif (choice == 2):
            user_id = int(input("Enter your User ID: "))
            show_all_tickets(user_id)
        elif (choice == 3):
            print("---------- Thank you for using Railway Management System -----------")
            break
        else:
            print("Invalid choice")
            continue

if __name__ == "__main__":
    main()