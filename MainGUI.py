import tkinter as tk
import Database
from tkinter import messagebox

def on_submit():
    # Pulling the text from the UI boxes
    name = entry_name.get()
    price = entry_price.get()
    cat = entry_cat.get()
    
    if name and price and cat:
        Database.add_expense(name, price, cat) # Your existing SQL function!
        messagebox.showinfo("Success", f"Added {name}!")
        entry_name.delete(0, tk.END) # Clear the box
        refresh_total()
    else:
        messagebox.showwarning("Error", "Fill out all fields!")

def delete_row_entry():
    pop = tk.Toplevel(root)
    pop.title("Delete Row")
    pop.geometry("200x150")
    
    tk.Label(pop, text="Enter ID # to delete:").pack(pady=5)
    entry_ID = tk.Entry(pop)
    entry_ID.pack(pady=5)
    
    # We create a small helper function inside to grab the text and call the DB
    def confirm_delete():
        target_id = entry_ID.get()
        if target_id.isdigit():
            Database.delete_row(int(target_id))
            messagebox.showinfo("Deleted", f"Row {target_id} removed.")
            pop.destroy() # Closes the pop-up window
            refresh_total()
        else:
            messagebox.showwarning("Error", "Please enter a valid number ID.")

    tk.Button(pop, text="Confirm Delete", command=confirm_delete).pack(pady=10)
    

def confirm_reset():
    # This creates a standard Windows/Mac alert box
    response = messagebox.askyesno("Confirm Reset", "Are you sure? This will delete ALL data and reset IDs.")
    
    if response: # If they clicked 'Yes'
        Database.reset_table()
        messagebox.showinfo("Reset", "The table has been cleared.")
        refresh_total()
    else:
        messagebox.showinfo("Reset Cancelled")
        

def choose_type():
    pop = tk.Toplevel(root)
    pop.title("Choose type")
    pop.geometry("200x200")
    
    tk.Label(pop, text="Choose a way to calculate").pack(pady=5)
    
    tk.Button(pop, text="Calculate by Item", command=calc_item).pack(pady=5)
    tk.Button(pop, text="Calculate by Category", command=calc_cat).pack(pady=5)
    tk.Button(pop, text="Calculate Total", command=calc_total).pack(pady=5)
    
def calc_item():
    pop = tk.Toplevel(root)
    pop.title("Item Name:")
    pop.geometry("200x200")
    
    tk.Label(pop, text="Enter Item Name:").pack(pady=5)
    item_name = tk.Entry(pop)
    item_name.pack(pady=5)
    
    def submit():
        target_name = item_name.get()
        if len(target_name) > 0:
            total = Database.calculate_spending_by_item(target_name)
            messagebox.showinfo(f"Total Spending", f"Your total spending for {target_name} is: ${total:.2f}")
        else:
            print("Item not found")
    tk.Button(pop, text="Calculate", command=submit).pack(pady=5)


def calc_cat():
    pop = tk.Toplevel(root)
    pop.title("Item Name:")
    pop.geometry("200x200")
    
    tk.Label(pop, text="Enter Category Name:").pack(pady=5)
    cat_name = tk.Entry(pop)
    cat_name.pack(pady=5)
    
    def submit():
        target_name = cat_name.get()
        if len(target_name) > 0:
            total = Database.calculate_spending_by_category(target_name)
            messagebox.showinfo(f"Total Spending", f"Your total spending for {target_name} is: ${total:.2f}")
        else:
            print("Category not Found")
    tk.Button(pop, text="Calculate", command=submit).pack(pady=5)

def calc_total():
    total = Database.calculate_total_spending()
    messagebox.showinfo("Total Spending", f"Your total spending is: ${total:.2f}")
    
def refresh_total():
    current_total = Database.calculate_total_spending()
    total_var.set(f"Total Spending: ${current_total:.2f}")

def view_table():
    table = Database.view_table()
    messagebox.showinfo("Table info", table)
    


# Setup the Window
root = tk.Tk()
root.title("Finance Tracker Pro")
root.geometry("300x400")

# Create UI Elements
tk.Label(root, text="Item Name:").pack()
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Price:").pack()
entry_price = tk.Entry(root)
entry_price.pack()

tk.Label(root, text="Category:").pack()
entry_cat = tk.Entry(root)
entry_cat.pack()

tk.Button(root, text="Add Expense", command=on_submit).pack(pady=5)
tk.Button(root, text="View Table", command=view_table).pack(pady=5)
tk.Button(root, text="Delete Row", command=delete_row_entry).pack(pady=5)
tk.Button(root, text="Reset Table", command=confirm_reset).pack(pady=5)
tk.Button(root, text="Calculate Spending", command=choose_type).pack(pady=5)

# A special Tkinter variable that can be updated easily
total_var = tk.StringVar()
total_var.set("Total Spending: $0.00")

# Create the label and link it to that variable
label_status = tk.Label(root, text="", textvariable=total_var, font=("Arial", 12, "bold"), fg="blue")
label_status.pack(pady=20)
refresh_total()


root.mainloop()