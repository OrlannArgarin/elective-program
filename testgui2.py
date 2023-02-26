from pathlib import Path
from os.path import dirname
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Radiobutton
from tkinter import *
from tkinter import ttk
from formdb import Database

db = Database("mydatabase.db")


OUTPUT_PATH = dirname(__file__)
ASSETS_PATH = OUTPUT_PATH + r"\assets\frame0"


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


print(OUTPUT_PATH)
window = Tk()
window.title("Store Receipt Database")
window.geometry("1055x731")
window.configure(bg="#074A5E")


canvas = Canvas(
    window,
    bg="#074A5E",
    height=731,
    width=1055,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
canvas.create_rectangle(
    35.0,
    35.0,
    631.0,
    357.0,
    fill="#FFFFFF",
    outline="")


itemClicked = StringVar(value="0")
qtyEntry = StringVar()
transaction_id = 0

# program functions

priceList = [8, 50, 10, 45, 10, 8, 8, 8, 5, 5, 18, 8,
             7, 8, 260, 15, 10, 50, 10, 8, 5, 150, 8, 10, 60]
itemList = ["vinegar", "sugar", "soy", "salt", "oil", "egg", "potato", "tomato", "onion", "garlic", "sardines", "biscuit",
            "coffee", "milo", "milk", "ariel", "downy", "bars", "joy", "toothpaste", "mask", "alcohol", "shampoo", "conditioner", "rice"]


def dispalyAll():
    tv2.delete(*tv2.get_children())
    for row in db.fetch():
        tv2.insert("", END, values=row)
        # print(row)


def submitSelection():
    item = itemClicked.get()
    if item == "0":
        messageBox.showinfo("Item Insertion Status",
                            "Please select an item")
        checkError = 1
        return

    price = 0.0
    quantity = qtyEntry.get()
    checkError = 0
    try:
        int(quantity)
    except:
        messageBox.showinfo("Item Insertion Status",
                            "Input whole numbers in 'Quantity'")
        checkError = 1
        return
    else:
        if checkError == 0:
            if item in itemList:
                i = itemList.index(item)
            else:
                messageBox.showinfo("Item Insertion Status",
                                    "There is something wrong with the program")
                return
            price = priceList[i]
            price = price * float(quantity)
            price = "%.2f" % price
            tv.insert("", "end", values=(item, quantity, price))

            addTotal()

            # reset values of radio buttons and qtyentry
            itemClicked.set(False)
            qtyEntry.delete(0, 'end')


def compute():
    checkError = 0
    totalfee = 0.0
    for child in tv.get_children():
        totalfee += float(tv.item(child)["values"][2])
    payment = payment_entry.get()
    if totalfee == 0:
        messageBox.showinfo("Computation Status",
                            "Items need to be ordered first")
        checkError = 1
    elif payment == "":
        messageBox.showinfo("Computation", "No Payment inputted")
        checkError = 1
    else:
        try:
            int(payment)
        except:
            messageBox.showinfo("Computation Status",
                                "Payment inputted is not a number")
            checkError = 1
        else:
            if float(payment) < totalfee:
                messageBox.showinfo("Computation Status",
                                    "Total Fee higher than Payment")
                checkError = 1
            if checkError == 0:
                change = float(payment) - totalfee
                change = "%.2f" % change
                totalfee = "%.2f" % totalfee

                totalEntry.config(state=NORMAL)  # Total Fee Display
                totalEntry.delete(0, 'end')
                totalEntry.insert(0, str(totalfee))
                totalEntry.config(state="readonly")

                change_entry.config(state=NORMAL)   # Change Display
                change_entry.delete(0, 'end')
                change_entry.insert(0, str(change))
                change_entry.config(state="readonly")


def addTotal():
    totalfee = 0.0
    for child in tv.get_children():
        totalfee += float(tv.item(child)["values"][2])

    totalEntry.config(state=NORMAL)  # Total Fee Display
    totalEntry.delete(0, 'end')
    totalEntry.insert(0, str(totalfee))
    totalEntry.config(state="readonly")


def submitReceipt():
    checkError = 0
    try:
        totalFee = float(totalEntry.get())
        payment = float(payment_entry.get())
        change = float(change_entry.get())
    except:
        messageBox.showinfo("Submit to Database Status",
                            "Some fields have invalid characters or contain no data")
        return

    test = change + totalFee

    if test != payment:
        messageBox.showinfo("Submit to Database Status",
                            "Re-compute the data again!")
        checkError = 1
        return

    insertToDB()
    dispalyAll()
    clearFields()


def insertToDB():
    transaction_id = random.randrange(10000000, 99999999)
    if totalEntry.get() == "" or payment_entry.get() == "" or change_entry.get() == "":
        messageBox.showerror("Submit to Database Status",
                             "Some fields have invalid characters or contain no data")
        return

    try:
        db.insert(transaction_id, totalEntry.get(),
                  payment_entry.get(), change_entry.get())
    except:
        messageBox.showerror("Submit to Database Status",
                             "Transaction ID had a duplicate value, try submitting again")
        return

    messageBox.showinfo("Success", "Record Successfully Saved")


def deleteDbSelection():
    selected_items = tv2.selection()
    if selected_items == ():
        messageBox.showinfo("Delete Selection Status",
                            "Select an entry first!")
        return
    delete_stud = messageBox.askyesno(
        "Store Receipt Database", "Are you sure you want to delete this entry?")
    if delete_stud > 0:
        db.remove(tv2.item(selected_items)['values'][0])

    dispalyAll()


def purgeDb():
    messageBox.showinfo("DANGER! DANGER! DANGER! DANGER! DANGER!",
                        "WARNING: Purging database, proceed with caution")
    delete_stud = messageBox.askyesno("DANGER! DANGER! DANGER! DANGER! DANGER!",
                                      "Are you sure you want to PURGE the WHOLE DATABASE?")
    if delete_stud > 0:
        db.purge()

    dispalyAll()


def clearFields():
    tv.delete(*tv.get_children())

    totalEntry.config(state=NORMAL)  # Total Fee Display
    totalEntry.delete(0, 'end')
    totalEntry.config(state="readonly")

    payment_entry.delete(0, 'end')

    change_entry.config(state=NORMAL)   # Change Display
    change_entry.delete(0, 'end')
    change_entry.config(state="readonly")


def deleteSelection():
    selected_items = tv.selection()
    if selected_items == ():
        messageBox.showinfo("Delete Selection Status",
                            "Select an entry first!")
    for selected_item in selected_items:
        tv.delete(selected_item)
    compute()


# program functions

priceList = [8, 50, 10, 45, 10, 8, 8, 8, 5, 5, 18, 8,
             7, 8, 260, 15, 10, 50, 10, 8, 5, 150, 8, 10, 60]
itemList = ["vinegar", "sugar", "soy", "salt", "oil", "egg", "potato", "tomato", "onion", "garlic", "sardines", "biscuit",
            "coffee", "milo", "milk", "ariel", "downy", "bars", "joy", "toothpaste", "mask", "alcohol", "shampoo", "conditioner", "rice"]


def dispalyAll():
    tv2.delete(*tv2.get_children())
    for row in db.fetch():
        tv2.insert("", END, values=row)
        # print(row)


def submitSelection():
    item = itemClicked.get()
    price = 0.0
    if item in itemList:
        i = itemList.index(item)
    price = priceList[i]
    quantity = entry_1.get()
    try:
        int(quantity)
    except:
        messageBox.showinfo("Item Insertion Status", "Input whole numbers in 'Quantity'")
        checkError = 1
    else:
        price = price * float(quantity)
        price = "%.2f" % price
        tv.insert("","end",values=(item, quantity, price))

def submitReceipt():
    checkError =0
    totalfee = 0.0
    for child in tv.get_children():
        totalfee += float(tv.item(child)["values"][2])
    payment = entry_4.get()
    if totalfee == 0 : 
        messageBox.showinfo("Receipt Submission Status", "Items need to be ordered first")
        checkError = 1
    elif payment == "" : 
        messageBox.showinfo("Receipt Submission Status", "No Payment inputted")
        checkError = 1
    else:
        try:
            int(payment)
        except:
            messageBox.showinfo("Receipt Submission Status", "Payment inputted is not a number")
            checkError = 1
        else:
            if float(payment) < totalfee:
                messageBox.showinfo("Receipt Submission Status", "Total Fee higher than Payment")
                checkError = 1
            if checkError == 0:
                change = float(payment) - totalfee
                change = "%.2f" % change
                totalfee = "%.2f" % totalfee

                entry_2.config(state = NORMAL)   #Total Fee Display
                entry_2.insert(0, str(totalfee))
                entry_2.config(state = DISABLED)

                entry_5.config(state = NORMAL) 
                entry_5.insert(0, str(change)) #Total Change Display
                entry_5.config(state = DISABLED)

def deleteReceipt():
    tv.delete(*tv.get_children())

RButton_vinegar = Radiobutton(
    window, text="Vinegar",  variable=itemClicked, value="vinegar", background="#FFFFFF")
RButton_vinegar.place(
    x=60.0,
    y=100.0,
    width=100.0,
    height=30.0)

RButton_sugar = Radiobutton(
    window, text="Sugar",  variable=itemClicked, value="sugar", background="#FFFFFF")
RButton_sugar.place(
    x=57.0,
    y=135.0,
    width=100.0,
    height=30.0)

RButton_soy = Radiobutton(window, text="Soy Sauce",
                          variable=itemClicked, value="soy", background="#FFFFFF")
RButton_soy.place(
    x=57.0,
    y=170.0,
    width=100.0,
    height=30.0)

RButton_salt = Radiobutton(
    window, text="Salt",  variable=itemClicked, value="salt", background="#FFFFFF")
RButton_salt.place(
    x=57.0,
    y=205.0,
    width=100.0,
    height=30.0)

RButton_oil = Radiobutton(
    window, text="Oil",  variable=itemClicked, value="oil", background="#FFFFFF")
RButton_oil.place(
    x=57.0,
    y=240.0,
    width=100.0,
    height=30.0)

RButton_egg = Radiobutton(
    window, text="Egg",  variable=itemClicked, value="egg", background="#FFFFFF")
RButton_egg.place(
    x=165.0,
    y=100.0,
    width=100.0,
    height=30.0)

RButton_potato = Radiobutton(
    window, text="Potato",  variable=itemClicked, value="potato", background="#FFFFFF")
RButton_potato.place(
    x=165.0,
    y=135.0,
    width=100.0,
    height=30.0)

RButton_tomato = Radiobutton(
    window, text="Tomato",  variable=itemClicked, value="tomato", background="#FFFFFF")
RButton_tomato.place(
    x=165.0,
    y=170.0,
    width=100.0,
    height=30.0)

RButton_onion = Radiobutton(
    window, text="Onion",  variable=itemClicked, value="onion", background="#FFFFFF")
RButton_onion.place(
    x=165.0,
    y=205.0,
    width=100.0,
    height=30.0)

RButton_garlic = Radiobutton(
    window, text="Garlic",  variable=itemClicked, value="garlic", background="#FFFFFF")
RButton_garlic.place(
    x=165.0,
    y=240.0,
    width=100.0,
    height=30.0)

RButton_sardines = Radiobutton(
    window, text="Sardines",  variable=itemClicked, value="sardines", background="#FFFFFF")
RButton_sardines.place(
    x=270.0,
    y=100.0,
    width=100.0,
    height=30.0)

RButton_biscuit = Radiobutton(
    window, text="Biscuit",  variable=itemClicked, value="biscuit", background="#FFFFFF")
RButton_biscuit.place(
    x=270.0,
    y=135.0,
    width=100.0,
    height=30.0)

RButton_coffee = Radiobutton(window, text="Instant Coffee",
                             variable=itemClicked, value="coffee", background="#FFFFFF")
RButton_coffee.place(
    x=270.0,
    y=170.0,
    width=100.0,
    height=30.0)

RButton_milo = Radiobutton(
    window, text="Milo",  variable=itemClicked, value="milo", background="#FFFFFF")
RButton_milo.place(
    x=270.0,
    y=205.0,
    width=100.0,
    height=30.0)

RButton_milk = Radiobutton(
    window, text="Milk",  variable=itemClicked, value="milk", background="#FFFFFF")
RButton_milk.place(
    x=270.0,
    y=240.0,
    width=100.0,
    height=30.0)

RButton_ariel = Radiobutton(
    window, text="Ariel",  variable=itemClicked, value="ariel", background="#FFFFFF")
RButton_ariel.place(
    x=375.0,
    y=100.0,
    width=100.0,
    height=30.0)

RButton_downy = Radiobutton(
    window, text="Downy",  variable=itemClicked, value="downy", background="#FFFFFF")
RButton_downy.place(
    x=375.0,
    y=135.0,
    width=100.0,
    height=30.0)

RButton_bars = Radiobutton(window, text="Bar Soap",
                           variable=itemClicked, value="bars", background="#FFFFFF")
RButton_bars.place(
    x=375.0,
    y=170.0,
    width=100.0,
    height=30.0)

RButton_joy = Radiobutton(
    window, text="Joy",  variable=itemClicked, value="joy", background="#FFFFFF")
RButton_joy.place(
    x=375.0,
    y=205.0,
    width=100.0,
    height=30.0)

RButton_toothpaste = Radiobutton(
    window, text="Toothpaste",  variable=itemClicked, value="toothpaste", background="#FFFFFF")
RButton_toothpaste.place(
    x=375.0,
    y=240.0,
    width=100.0,
    height=30.0)

RButton_mask = Radiobutton(
    window, text="Mask",  variable=itemClicked, value="mask", background="#FFFFFF")
RButton_mask.place(
    x=480.0,
    y=100.0,
    width=100.0,
    height=30.0)

RButton_alcohol = Radiobutton(
    window, text="Alcohol",  variable=itemClicked, value="alcohol", background="#FFFFFF")
RButton_alcohol.place(
    x=480.0,
    y=135.0,
    width=100.0,
    height=30.0)

RButton_shampoo = Radiobutton(
    window, text="Shampoo",  variable=itemClicked, value="shampoo", background="#FFFFFF")
RButton_shampoo.place(
    x=480.0,
    y=170.0,
    width=100.0,
    height=30.0)

RButton_conditioner = Radiobutton(
    window, text="Conditioner",  variable=itemClicked, value="conditioner", background="#FFFFFF")
RButton_conditioner.place(
    x=480.0,
    y=205.0,
    width=100.0,
    height=30.0)

RButton_rice = Radiobutton(window, text="Rice",
                           variable=itemClicked, value="rice", background="#FFFFFF")
RButton_rice.place(
    x=480.0,
    y=240.0,
    width=100.0,
    height=30.0)

submitSelection_button_image = PhotoImage(
    file=relative_to_assets("button_1.png"))
submitSelection_button = Button(
    image=submitSelection_button_image,
    borderwidth=0,
    highlightthickness=0,
    command=submitSelection,
    relief="flat"
)
submitSelection_button.place(
    x=349.0,
    y=292.0,
    width=216.0,
    height=39.0
)

deleteDbSelection_button_image = PhotoImage(
    file=relative_to_assets("button_2.png"))
deleteDbSelection_button = Button(
    image=deleteDbSelection_button_image,
    borderwidth=0,
    highlightthickness=0,
    command=deleteDbSelection,
    relief="flat"
)
deleteDbSelection_button.place(
    x=698.0,
    y=584.0,
    width=270.0,
    height=39.0
)

purge_button_image = PhotoImage(
    file=relative_to_assets("button_3.png"))
purge_button = Button(
    image=purge_button_image,
    borderwidth=0,
    highlightthickness=0,
    command=purgeDb,
    relief="flat"
)
purge_button.place(
    x=698.0,
    y=638.0,
    width=270.0,
    height=39.0
)

qtyEntry_image = PhotoImage(
    file=relative_to_assets("entry_1.png"))
qtyEntry_bg = canvas.create_image(
    268.0,
    311.5,
    image=qtyEntry_image
)
qtyEntry = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
qtyEntry.place(
    x=222.0,
    y=297.0,
    width=92.0,
    height=27.0
)

canvas.create_rectangle(
    50.0,
    91.996826171875,
    585.0009765625,
    95.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    50.0,
    279.0,
    585.0009765625,
    282.003173828125,
    fill="#000000",
    outline="")

canvas.create_text(
    51.0,
    56.0,
    anchor="nw",
    text="ITEMS",
    fill="#000000",
    font=("TimesNewRomanPSMT", 25 * -1)
)

canvas.create_text(
    71.0,
    301.0,
    anchor="nw",
    text="QUANTITY",
    fill="#000000",
    font=("TimesNewRomanPSMT", 18 * -1)
)

canvas.create_rectangle(
    35.0,
    374.0,
    631.0,
    696.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    35.0,
    441.0,
    184.0,
    486.0,
    fill="#B8BEC0",
    outline="")

canvas.create_rectangle(
    184.0,
    441.0,
    333.0,
    486.0,
    fill="#B8BEC0",
    outline="")

canvas.create_rectangle(
    333.0,
    441.0,
    482.0,
    486.0,
    fill="#B8BEC0",
    outline="")

canvas.create_rectangle(
    482.0,
    441.0,
    631.0,
    486.0,
    fill="#B8BEC0",
    outline="")

canvas.create_text(
    52.0,
    452.0,
    anchor="nw",
    text="Transaction ID",
    fill="#000000",
    font=("TimesNewRomanPSMT", 18 * -1)
)

canvas.create_text(
    224.0,
    452.0,
    anchor="nw",
    text="Total Fee",
    fill="#000000",
    font=("TimesNewRomanPSMT", 18 * -1)
)

canvas.create_text(
    375.0,
    452.0,
    anchor="nw",
    text="Payment",
    fill="#000000",
    font=("TimesNewRomanPSMT", 18 * -1)
)

canvas.create_text(
    524.0,
    452.0,
    anchor="nw",
    text="Change",
    fill="#000000",
    font=("TimesNewRomanPSMT", 18 * -1)
)

canvas.create_rectangle(
    35.0,
    374.0,
    631.0,
    439.0,
    fill="#8DC1CF",
    outline="")

canvas.create_text(
    264.0,
    391.0,
    anchor="nw",
    text="DATABASE",
    fill="#000000",
    font=("TimesNewRomanPSMT", 27 * -1)
)

canvas.create_rectangle(
    33.0,
    439.0,
    631.0,
    441.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    33.0,
    484.0,
    631.0,
    486.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    181.0,
    439.0,
    183.0,
    486.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    331.0,
    439.0,
    333.0,
    486.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    479.0,
    439.0,
    481.0,
    486.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    648.0,
    35.0,
    1020.0,
    560.0,
    fill="#FFFFFF",
    outline="")

totalEntry_image = PhotoImage(
    file=relative_to_assets("entry_4.png"))
totalEntry_bg = canvas.create_image(
    905.5,
    446.5,
    image=totalEntry_image
)
totalEntry = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    state='readonly'
)
totalEntry.place(
    x=822.0,
    y=434.0,
    width=168.0,
    height=27.0
)
# totalLabel = Label(
#     text="0",
# )
# totalLabel.place(
#     x=905.5,
#     y=446.5

# entry_image_3 = PhotoImage(
#     file=relative_to_assets("entry_3.png"))
# entry_bg_3 = canvas.create_image(
#     945.0,
#     446.5,
#     image=entry_image_3
# )
# entry_3 = Entry(
#     bd=0,
#     bg="#D9D9D9",
#     fg="#000716",
#     highlightthickness=0
# )
# entry_3.place(
#     x=899.0,
#     y=432.0,
#     width=92.0,
#     height=27.0
# )

payment_entry_image = PhotoImage(
    file=relative_to_assets("entry_4.png"))
payment_entry_bg = canvas.create_image(
    907.0,
    486.5,
    image=payment_entry_image
)
payment_entry = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
payment_entry.place(
    x=823.0,
    y=472.0,
    width=168.0,
    height=27.0
)

change_entry_image = PhotoImage(
    file=relative_to_assets("entry_5.png"))
change_entry_bg = canvas.create_image(
    907.0,
    526.5,
    image=change_entry_image
)
change_entry = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    state='readonly'
    # disabledforeground="black"
)
change_entry.place(
    x=823.0,
    y=512.0,
    width=168.0,
    height=27.0
)

canvas.create_rectangle(
    677.0,
    169.0,
    816.0,
    199.0,
    fill="#B8BEC0",
    outline="")

canvas.create_rectangle(
    823.0,
    169.0,
    892.0,
    199.0,
    fill="#B8BEC0",
    outline="")

canvas.create_rectangle(
    899.0,
    169.0,
    991.0,
    199.0,
    fill="#B8BEC0",
    outline="")

canvas.create_text(
    719.0,
    174.0,
    anchor="nw",
    text="ITEMS",
    fill="#000000",
    font=("TimesNewRomanPSMT", 18 * -1)
)

canvas.create_text(
    839.0,
    174.0,
    anchor="nw",
    text="QTY",
    fill="#000000",
    font=("TimesNewRomanPSMT", 18 * -1)
)

canvas.create_text(
    916.0,
    174.0,
    anchor="nw",
    text="TOTAL",
    fill="#000000",
    font=("TimesNewRomanPSMT", 18 * -1)
)

canvas.create_text(
    682.0,
    56.0,
    anchor="nw",
    text="SALES",
    fill="#000000",
    font=("TimesNewRomanPSMT", 25 * -1)
)

canvas.create_rectangle(
    674.0,
    92.0,
    991.0,
    95.996826171875,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    674.0,
    415.0,
    991.0,
    418.996826171875,
    fill="#000000",
    outline="")

delete_button_image = PhotoImage(
    file=relative_to_assets("button_4.png"))
delete_button = Button(
    image=delete_button_image,
    borderwidth=0,
    highlightthickness=0,
    command=deleteSelection,
    relief="flat"
)
delete_button.place(
    x=875.0,
    y=110.0,
    width=116.0,
    height=39.0
)

submitReceipt_button_image = PhotoImage(
    file=relative_to_assets("button_5.png"))
submitReceipt_button = Button(
    image=submitReceipt_button_image,
    borderwidth=0,
    highlightthickness=0,
    command=submitReceipt,
    relief="flat"
)
submitReceipt_button.place(
    x=677.0,
    y=110.0,
    width=183.0,
    height=39.0
)

compute_button_image = PhotoImage(
    file=relative_to_assets("compute_button.png"))
compute_button = Button(
    image=compute_button_image,
    borderwidth=0,
    highlightthickness=0,
    command=compute,
    relief="flat"
)
compute_button.place(
    x=740.0,
    y=371.0,
    width=183.0,
    height=39.0
)

canvas.create_text(
    698.0,
    436.0,
    anchor="nw",
    text="TOTAL",
    fill="#000000",
    font=("TimesNewRomanPSMT", 18 * -1)
)

canvas.create_text(
    698.0,
    476.0,
    anchor="nw",
    text="PAYMENT",
    fill="#000000",
    font=("TimesNewRomanPSMT", 18 * -1)
)

canvas.create_text(
    698.0,
    517.0,
    anchor="nw",
    text="CHANGE",
    fill="#000000",
    font=("TimesNewRomanPSMT", 18 * -1)
)

# sales treeview
tv = ttk.Treeview(columns=(1, 2, 3), style="mystyle.Treeview")
tv.place(
    x=675.0,
    y=165.0,
    width=320,
    height=200)

scrolly = Scrollbar(tv, orient="vertical")
scrolly.pack(side="right", fill="y")

tv.config(yscrollcommand=scrolly.set)

tv.heading("1", text="ITEM")
tv.column("1", width=1)
tv.heading("2", text="QTY")
tv.column("2", width=1)
tv.heading("3", text="SUBTOTAL")
tv.column("3", width=1)
tv['show'] = 'headings'

scrolly.config(command=tv.yview)

# database treeview
tv2 = ttk.Treeview(columns=(1, 2, 3, 4), style="mystyle.Treeview")
tv2.place(
    x=35.0,
    y=440.0,
    width=596,
    height=256)
tv2.heading("1", text="Transaction ID")
tv2.column("1", width=50)
tv2.heading("2", text="Total Fee")
tv2.column("2", width=50)
tv2.heading("3", text="Payment")
tv2.column("3", width=50)
tv2.heading("4", text="Change")
tv2.column("4", width=50)
tv2['show'] = 'headings'


window.resizable(False, False)


dispalyAll()
window.mainloop()
