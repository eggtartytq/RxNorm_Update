import time
import tkinter as tk
from tkinter import *


class SelectedDBMS(tk.Tk):
    def __init__(self, default_dbms='postgresql'):
        super().__init__()
        self.selectedDBMSName = tk.StringVar()
        self.selectedDBMSName.set(default_dbms)
        DBMS_config = ['PostgreSQL', 'MySQL']
        ''' Provide a dialog depends on DBMS Names provided above, convient users to select DBMS to import files in'''
        self.deiconify()
        self.title("DBMS Selection")
        Label(self, text="Select the DBMS you are using:", font=("Arial", 18), height=2).pack()
        for DBMSName in DBMS_config:
            Radiobutton(self, text=DBMSName,
                        variable=self.selectedDBMSName, value=DBMSName.lower(),
                        font=("Arial", 13), padx=20, height=1, justify='left', anchor="w").pack()
        Button(self, text="Confirm", command=self.click_confirm, pady=7, font=("Arial", 13), width=15).pack()

    def click_confirm(self):
        """ Callback Function of Select DBMS Dialog
        """
        self.withdraw()
        self.quit()
        self.destroy()

    def get_target_dbms(self):
        # Description of the table
        self.mainloop()
        return str(self.selectedDBMSName.get())


if __name__ == "__main__":
    app = SelectedDBMS(default_dbms='mysql')
    dbms = app.get_target_dbms()
    print("[Test]DBMS Selected:{}".format(dbms))
