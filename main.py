import tkinter as tk
import sqlite3


class Database:
    def __init__(self, name: str) -> None:
        self.name = name
        self.create_db()

    def create_db(self):
        CREATE_DATA = """
        create table if not exists person (
          id integer primary key,
          name text not null,
          money real default 0.0,
          inventory_id integer not null,
          foreign key (inventory_id) references inventory (id)
        ); 

        create table if not exists inventory (
          id integer not null,
          product_id integer not null,
          amount integer not null,
          foreign key (product_id) references product (id),
          primary key (id, product_id)
        );

        create table if not exists product (
          id integer primary key,
          name text not null,
          description text not null
        );

        """
        sqlite3.connect(self.name).cursor().executescript(CREATE_DATA).close()

    def __run_db_task(self, task: str):
        connection = sqlite3.connect(self.name)
        cursor = connection.cursor()
        cursor.execute(task)
        connection.commit()
        connection.close()

    def add_person(self, person_name: str, cash: float, inventory_id: int):
        task = f'insert into person (name, money, inventory_id) values ("{person_name}", {cash}, {inventory_id});'
        self.__run_db_task(task)

    def add_product(self, product_name: str, product_description: str):
        task = f'insert into product (name, description) values ("{product_name}", "{product_description}");'
        self.__run_db_task(task)

    def add_inventory(self, inventory_id: int, product_id: int, amount: int):
        task = f'insert into inventory (id, product_id, amount) values ' \
               f'({inventory_id}, {product_id}, {amount});'
        self.__run_db_task(task)

    def delete_person(self, person_name: str):
        task = f'delete from person where name = ("{person_name}");'
        self.__run_db_task(task)

    def delete_product(self, product_name: str):
        task = f'delete from product where name = ("{product_name}");'
        self.__run_db_task(task)

    def delete_inventory(self, inventory_id: int, product_id: int):
        task = f'delete from inventory where id = ({inventory_id}) and product_id = ({product_id});'
        self.__run_db_task(task)

    def clear_db_table(self, table_name: str):
        task = f'delete from {table_name}'
        self.__run_db_task(task)

    def get_db_table(self, table_name: str):
        task = f'select * from {table_name}'
        connection = sqlite3.connect(self.name)
        cursor = connection.cursor()
        data = cursor.execute(task).fetchall()
        connection.close()
        return data


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.main_menu = tk.Menu(self.root)
        self.file_menu = None
        self.debug_menu = None

        self.db = Database("my_db.db")
        self.mainframe = tk.Frame(self.root)
        self.open_widgets = []
        self.add_label = tk.Label(self.mainframe, text="Add:")
        self.add_button1 = tk.Button(self.mainframe, text="Person")
        self.add_button2 = tk.Button(self.mainframe, text="Product")
        self.add_button3 = tk.Button(self.mainframe, text="Inventory")
        self.del_label = tk.Label(self.mainframe, text="Delete:")
        self.del_button1 = tk.Button(self.mainframe, text="Person")
        self.del_button2 = tk.Button(self.mainframe, text="Product")
        self.del_button3 = tk.Button(self.mainframe, text="Inventory")
        self.show_button1 = tk.Button(self.mainframe, text="Person")
        self.show_button2 = tk.Button(self.mainframe, text="Product")
        self.show_button3 = tk.Button(self.mainframe, text="Inventory")
        self.show_label = tk.Label(self.mainframe, text="Show:")
        self.build_window()

    def build_window(self):
        w = self.root.winfo_screenwidth() // 2 - 200
        h = self.root.winfo_screenheight() // 2 - 50
        self.root.title("DB for dummies")
        self.root.geometry(f"400x100+{w}+{h}")
        self.build_main_menu()
        self.build_mainframe()
        self.root.mainloop()

    def build_main_menu(self):
        self.root.config(menu=self.main_menu)
        self.file_menu = tk.Menu(self.main_menu, tearoff=0)
        self.debug_menu = tk.Menu(self.main_menu, tearoff=0)

        self.file_menu.add_command(label='empty: Person', command=lambda x="person": self.empty_data(x))
        self.file_menu.add_command(label='empty: Product', command=lambda x="product": self.empty_data(x))
        self.file_menu.add_command(label='empty: Inventory', command=lambda x="inventory": self.empty_data(x))

        self.debug_menu.add_command(label='print: Person', command=lambda x="person": self.print_data(x))
        self.debug_menu.add_command(label='print: Product', command=lambda x="product": self.print_data(x))
        self.debug_menu.add_command(label='print: Inventory', command=lambda x="inventory": self.print_data(x))

        self.main_menu.add_cascade(label='Empty Table', menu=self.file_menu)
        self.main_menu.add_cascade(label='Debug', menu=self.debug_menu)

    def empty_data(self, chosen_type: str):
        self.db.clear_db_table(chosen_type)

    def print_data(self, chosen_type: str):
        print(self.db.get_db_table(chosen_type))

    def build_mainframe(self):
        self.config_buttons()
        self.add_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.add_button1.grid(row=0, column=1, sticky=tk.E)
        self.add_button2.grid(row=0, column=2, sticky=tk.E)
        self.add_button3.grid(row=0, column=3, sticky=tk.E)
        self.del_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.del_button1.grid(row=1, column=1, sticky=tk.E)
        self.del_button2.grid(row=1, column=2, sticky=tk.E)
        self.del_button3.grid(row=1, column=3, sticky=tk.E)
        self.show_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.show_button1.grid(row=2, column=1, sticky=tk.E)
        self.show_button2.grid(row=2, column=2, sticky=tk.E)
        self.show_button3.grid(row=2, column=3, sticky=tk.E)
        self.mainframe.pack()

    def config_buttons(self):
        self.add_button1.bind('<Button-1>', lambda e, f="person": self.create_add_widget(e, f))
        self.add_button2.bind('<Button-1>', lambda e, f="product": self.create_add_widget(e, f))
        self.add_button3.bind('<Button-1>', lambda e, f="inventory": self.create_add_widget(e, f))

        self.del_button1.bind('<Button-1>', lambda e, f="person": self.create_del_widget(e, f))
        self.del_button2.bind('<Button-1>', lambda e, f="product": self.create_del_widget(e, f))
        self.del_button3.bind('<Button-1>', lambda e, f="inventory": self.create_del_widget(e, f))

        self.show_button1.bind('<Button-1>', lambda e, f="person": self.create_show_widget(e, f))
        self.show_button2.bind('<Button-1>', lambda e, f="product": self.create_show_widget(e, f))
        self.show_button3.bind('<Button-1>', lambda e, f="inventory": self.create_show_widget(e, f))

    def create_add_widget(self, event, name: str):
        add_widget = AddWindow(name, self.db)
        self.open_widgets.append(add_widget)

    def create_del_widget(self, event, name: str):
        del_widget = DeleteWindow(name, self.db)
        self.open_widgets.append(del_widget)

    def create_show_widget(self, event, name: str):
        show_widget = ShowWindow(name, self.db)
        self.open_widgets.append(show_widget)


class AddWindow(tk.Toplevel):
    def __init__(self, chosen_type: str, database):
        super().__init__()
        self.db = database
        self.type = chosen_type

        self.frame = tk.Frame(self)
        self.label1 = tk.Label(self.frame)
        self.label2 = tk.Label(self.frame)
        self.label3 = tk.Label(self.frame)
        self.empty_label = tk.Label(self.frame)
        self.entry1 = tk.Entry(self.frame)
        self.entry2 = tk.Entry(self.frame)
        self.entry3 = tk.Entry(self.frame)
        self.spinbox1 = tk.Spinbox(self.frame)
        self.spinbox2 = tk.Spinbox(self.frame)
        self.spinbox3 = tk.Spinbox(self.frame)
        self.save_button = tk.Button(self.frame)
        self.log_label = tk.Label(self.frame)
        self.close_button = tk.Button(self.frame)
        self.text = tk.Text(self.frame)
        self.run()

    def run(self):
        if self.type == 'person':
            self.person_frame()
        elif self.type == 'product':
            self.product_frame()
        elif self.type == 'inventory':
            self.inventory_frame()
        else:
            self.destroy()

    def person_frame(self):
        self.label1.config(text="Name:")
        self.entry1.config(width=30)
        self.label2.config(text="Cash:")
        self.entry2.config(width=10)
        self.label3.config(text="Inventory ID:")
        self.spinbox1.config(from_=1, to=10000, width=5)
        self.save_button.config(text="Save")
        self.log_label.config(width=20, bg='grey', fg='white')
        self.close_button.config(text="Close")

        self.label1.grid(row=0, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        self.entry1.grid(row=0, column=2, sticky=tk.W)
        self.empty_label.grid(row=0, column=3)
        self.label2.grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        self.entry2.grid(row=1, column=2, sticky=tk.W)
        self.label3.grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        self.spinbox1.grid(row=2, column=2, sticky=tk.W)
        self.save_button.grid(row=3, column=0, sticky=tk.E, pady=5, padx=5)
        self.log_label.grid(row=3, column=1, padx=5)
        self.close_button.grid(row=3, column=2, sticky=tk.E)

        self.person_event_listeners()
        self.frame.pack()

    def product_frame(self):
        self.label1.config(text="Name:")
        self.entry1.config(width=30)
        self.label2.config(text="Description:")
        self.text.config(width=30, height=3)
        self.save_button.config(text="Save")
        self.log_label.config(width=20, bg='grey', fg='white')
        self.close_button.config(text="Close")

        self.label1.grid(row=0, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        self.entry1.grid(row=0, column=2, sticky=tk.W)
        self.empty_label.grid(row=0, column=3)
        self.label2.grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        self.text.grid(row=1, column=2, sticky=tk.W)
        self.save_button.grid(row=2, column=0, sticky=tk.E, pady=5, padx=5)
        self.log_label.grid(row=2, column=1, padx=5)
        self.close_button.grid(row=2, column=2, sticky=tk.E)

        self.product_event_listeners()
        self.frame.pack()

    def inventory_frame(self):
        self.label1.config(text="Inventory ID:")
        self.spinbox1.config(width=5, from_=1, to=99999)
        self.label2.config(text="Product ID:")
        self.spinbox2.config(width=5, from_=1, to=99999)
        self.label3.config(text="Amount:")
        self.spinbox3.config(width=5, from_=1, to=1000)
        self.save_button.config(text="Save")
        self.log_label.config(width=20, bg='grey', fg='white')
        self.close_button.config(text="Close")

        self.label1.grid(row=0, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        self.spinbox1.grid(row=0, column=2, sticky=tk.W)
        self.empty_label.grid(row=0, column=3)
        self.label2.grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        self.spinbox2.grid(row=1, column=2, sticky=tk.W)
        self.label3.grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        self.spinbox3.grid(row=2, column=2, sticky=tk.W)
        self.save_button.grid(row=3, column=0, sticky=tk.E, pady=5, padx=5)
        self.log_label.grid(row=3, column=1, padx=5)
        self.close_button.grid(row=3, column=2, sticky=tk.E)

        self.inventory_event_listeners()
        self.frame.pack()

    def person_event_listeners(self):
        self.save_button.bind('<Button-1>', lambda e: self.check_person_input(e))
        self.close_button.bind('<Button-1>', lambda e: self.destroy())

    def product_event_listeners(self):
        self.save_button.bind('<Button-1>', lambda e: self.check_product_input(e))
        self.close_button.bind('<Button-1>', lambda e: self.destroy())

    def inventory_event_listeners(self):
        self.save_button.bind('<Button-1>', lambda e: self.check_inventory_input(e))
        self.close_button.bind('<Button-1>', lambda e: self.destroy())

    def check_person_input(self, event):
        try:
            name_input = str(self.entry1.get())
            cash_input = float(self.entry2.get())
            inventory_id_input = int(self.spinbox1.get())
        except ValueError:
            self.log_label.config(bg='red', text='NOT Saved: Bad input')
        else:
            self.db.add_person(name_input, cash_input, inventory_id_input)
            self.log_label.config(bg='green', text='Saved')

    def check_product_input(self, event):
        name_input = str(self.entry1.get())
        text_input = str(self.text.get('1.0', tk.END))
        if len(name_input) >= 2 and len(text_input) > 1:
            self.db.add_product(name_input, text_input)
            self.log_label.config(bg='green', text='Saved')
        else:
            self.log_label.config(bg='red', text='NOT Saved: Bad input')

    def check_inventory_input(self, event):
        inventory_id_input = int(self.spinbox1.get())
        product_id_input = int(self.spinbox2.get())
        amount_input = int(self.spinbox3.get())
        if 1 <= inventory_id_input <= 99999 and 1 <= product_id_input <= 99999 and 1 <= amount_input <= 1000:
            self.db.add_inventory(inventory_id_input, product_id_input, amount_input)
            self.log_label.config(bg='green', text='Saved')
        else:
            self.log_label.config(bg='red', text='NOT Saved: Bad input')


class DeleteWindow(tk.Toplevel):
    def __init__(self, chosen_type: str, database):
        super().__init__()
        self.db = database
        self.type = chosen_type
        self.frame = tk.Frame(self)

        self.label1 = tk.Label(self.frame)
        self.label2 = tk.Label(self.frame)
        self.empty_label = tk.Label(self.frame)
        self.entry = tk.Entry(self.frame)

        self.spinbox1 = tk.Spinbox(self.frame)
        self.spinbox2 = tk.Spinbox(self.frame)

        self.delete_button = tk.Button(self.frame)
        self.log_label = tk.Label(self.frame)
        self.close_button = tk.Button(self.frame)

        self.run()

    def run(self):
        if self.type == 'person':
            self.person_frame()
        elif self.type == 'product':
            self.product_frame()
        elif self.type == 'inventory':
            self.inventory_frame()
        else:
            self.destroy()

    def person_frame(self):
        self.label1.config(text="Name:")
        self.entry.config(width=30)
        self.delete_button.config(text="Delete")
        self.log_label.config(width=20, bg='grey', fg='white')
        self.close_button.config(text="Close")

        self.label1.grid(row=0, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        self.entry.grid(row=0, column=2, sticky=tk.W)
        self.empty_label.grid(row=0, column=3)
        self.delete_button.grid(row=1, column=0, sticky=tk.E, pady=5, padx=5)
        self.log_label.grid(row=1, column=1, padx=5)
        self.close_button.grid(row=1, column=2, sticky=tk.E)

        self.person_event_listeners()
        self.frame.pack()

    def product_frame(self):
        self.label1.config(text="Name:")
        self.entry.config(width=30)
        self.delete_button.config(text="Delete")
        self.log_label.config(width=20, bg='grey', fg='white')
        self.close_button.config(text="Close")

        self.label1.grid(row=0, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        self.entry.grid(row=0, column=2, sticky=tk.W)
        self.empty_label.grid(row=0, column=3)
        self.delete_button.grid(row=1, column=0, sticky=tk.E, pady=5, padx=5)
        self.log_label.grid(row=1, column=1, padx=5)
        self.close_button.grid(row=1, column=2, sticky=tk.E)

        self.product_event_listeners()
        self.frame.pack()

    def inventory_frame(self):
        self.label1.config(text="Inventory ID:")
        self.spinbox1.config(width=5, from_=1, to=99999)
        self.label2.config(text="Product ID:")
        self.spinbox2.config(width=5, from_=1, to=99999)
        self.delete_button.config(text="Delete")
        self.log_label.config(width=20, bg='grey', fg='white')
        self.close_button.config(text="Close")

        self.label1.grid(row=0, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        self.spinbox1.grid(row=0, column=2, sticky=tk.W)
        self.empty_label.grid(row=0, column=3)
        self.label2.grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        self.spinbox2.grid(row=1, column=2, sticky=tk.W)
        self.delete_button.grid(row=2, column=0, sticky=tk.E, pady=5, padx=5)
        self.log_label.grid(row=2, column=1, padx=5)
        self.close_button.grid(row=2, column=2, sticky=tk.E)

        self.inventory_event_listeners()
        self.frame.pack()

    def person_event_listeners(self):
        self.delete_button.bind('<Button-1>', lambda e: self.check_person_input(e))
        self.close_button.bind('<Button-1>', lambda e: self.destroy())

    def product_event_listeners(self):
        self.delete_button.bind('<Button-1>', lambda e: self.check_product_input(e))
        self.close_button.bind('<Button-1>', lambda e: self.destroy())

    def inventory_event_listeners(self):
        self.delete_button.bind('<Button-1>', lambda e: self.check_inventory_input(e))
        self.close_button.bind('<Button-1>', lambda e: self.destroy())

    def check_person_input(self, event):
        name_input = str(self.entry.get())
        if len(name_input) < 2:
            self.log_label.config(bg='red', text='NOT Deleted: Bad input')
        else:
            self.db.delete_person(name_input)
            self.log_label.config(bg='green', text='Deleted')

    def check_product_input(self, event):
        name_input = str(self.entry.get())
        if len(name_input) >= 2:
            self.db.delete_product(name_input)
            self.log_label.config(bg='green', text='Deleted')
        else:
            self.log_label.config(bg='red', text='NOT Deleted: Bad input')

    def check_inventory_input(self, event):
        inventory_id_input = int(self.spinbox1.get())
        product_id_input = int(self.spinbox2.get())
        if 1 <= inventory_id_input <= 99999 and 1 <= product_id_input <= 99999:
            self.db.delete_inventory(inventory_id_input, product_id_input)
            self.log_label.config(bg='green', text='Deleted')
        else:
            self.log_label.config(bg='red', text='NOT Deleted: Bad input')


class ShowWindow(tk.Toplevel):
    def __init__(self, chosen_type: str, database):
        super().__init__()
        self.db = database
        self.type = chosen_type
        self.frame = tk.Frame(self)

        self.label1 = tk.Label(self.frame)
        self.label2 = tk.Label(self.frame)
        self.label3 = tk.Label(self.frame)
        self.label4 = tk.Label(self.frame)
        self.empty_label = tk.Label(self.frame)
        self.text = tk.Text(self.frame)
        self.close_button = tk.Button(self.frame)

        self.run()

    def run(self):
        if self.type == 'person':
            self.person_frame()
        elif self.type == 'product':
            self.product_frame()
        elif self.type == 'inventory':
            self.inventory_frame()
        else:
            self.destroy()

    def create_person_entries(self, data: list):
        total_elements = len(data)
        for i in range(0, total_elements):
            self.text.insert(tk.END, '\t' + str(data[i][0])+'\t'*2 + '*' + '\t'*2)
            self.text.insert(tk.END, str(data[i][1])+'\t'*2 + '*' + '\t'*2)
            self.text.insert(tk.END, str(data[i][2])+'\t'*2 + '*' + '\t'*2)
            self.text.insert(tk.END, str(data[i][3])+'\n')

    def create_product_entries(self, data: list):
        total_elements = len(data)
        for i in range(0, total_elements):
            self.text.insert(tk.END, str(data[i][2])+'\t'*5)
            self.text.insert(tk.END, str(data[i][1])+'\t'*5)
            self.text.insert(tk.END, str(data[i][0])+'\n' + '*'*90 + '\n')

    def create_inventory_entries(self, data: list):
        total_elements = len(data)
        for i in range(0, total_elements):
            self.text.insert(tk.END, str(data[i][0])+'\t'*5)
            self.text.insert(tk.END, str(data[i][1])+'\t'*5)
            self.text.insert(tk.END, str(data[i][2])+'\n' + '\"'*90 + '\n')

    def person_frame(self):
        self.label1.config(text="ID")
        self.label2.config(text="NAME")
        self.label3.config(text="MONEY")
        self.label4.config(text="INVENTORY_ID")
        self.text.config(width=120, height=24, wrap=tk.WORD)
        self.close_button.config(text="Close")
        data = self.db.get_db_table("person")

        self.label1.grid(row=0, column=0, padx=5, pady=5)
        self.label2.grid(row=0, column=1, padx=5, pady=5)
        self.label3.grid(row=0, column=2, padx=5, pady=5)
        self.label4.grid(row=0, column=3, padx=5, pady=5)
        self.empty_label.grid(row=0, column=4)

        self.create_person_entries(data)
        self.text.grid(row=1, column=0, columnspan=4)

        self.close_button.grid(row=2, column=3, sticky=tk.E)

        self.person_event_listeners()
        self.frame.pack()

    def product_frame(self):
        self.label1.config(text="DESCRIPTION")
        self.label2.config(text="NAME")
        self.label3.config(text="ID")

        self.text.config(width=90, height=24)
        self.close_button.config(text="Close")
        data = self.db.get_db_table("product")

        self.label1.grid(row=0, column=0, padx=5, pady=5)
        self.label2.grid(row=0, column=1, padx=5)
        self.label3.grid(row=0, column=2, padx=5)

        self.create_product_entries(data)
        self.text.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        self.close_button.grid(row=2, column=2, sticky=tk.E)

        self.product_event_listeners()
        self.frame.pack()

    def inventory_frame(self):
        self.label1.config(text="ID")
        self.label2.config(text="PRODUCT ID")
        self.label3.config(text="AMOUNT")
        self.text.config(width=90, height=24)
        self.close_button.config(text="Close")
        data = self.db.get_db_table("inventory")

        self.label1.grid(row=0, column=0, padx=5, pady=5)
        self.label2.grid(row=0, column=1, padx=5, pady=5)
        self.label3.grid(row=0, column=2, padx=5, pady=5)
        self.empty_label.grid(row=0, column=3)

        self.create_inventory_entries(data)
        self.text.grid(row=1, column=0, columnspan=3)
        self.close_button.grid(row=2, column=2, sticky=tk.E)

        self.inventory_event_listeners()
        self.frame.pack()

    def person_event_listeners(self):
        self.close_button.bind('<Button-1>', lambda e: self.destroy())

    def product_event_listeners(self):
        self.close_button.bind('<Button-1>', lambda e: self.destroy())

    def inventory_event_listeners(self):
        self.close_button.bind('<Button-1>', lambda e: self.destroy())


if __name__ == '__main__':
    window = MainWindow()
