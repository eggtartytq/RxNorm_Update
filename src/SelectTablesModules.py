import tkinter as tk
from tkinter import *
import pandas as pd

root = tk.Tk()
root.withdraw()


def click_confirm():
    """ Callback Function of Select Tables Dialog
    """
    root.withdraw()
    root.quit()
    root.destroy()


def select_tables(table_selected):
    """ Provide a dialog depends on tableNames provides, convient users to seleted tables to inport files in"""
    root.deiconify()
    root.title("Table Selection")
    label = tk.Label(root, text="Select the tables that you want to import:", font=("Arial", 18), height=2)
    label.pack()
    for i in table_selected.index:
        table_selected.loc[i, 'isSelected'] = IntVar()
        check_button = tk.Checkbutton(root,
                                      text=table_selected.loc[i, 'tableName'] + " (" + table_selected.loc[i][
                                          'tableDescription'] + ")",
                                      variable=table_selected.loc[i, 'isSelected'],
                                      onvalue=1, offvalue=0,
                                      font=("Arial", 13), padx=20, height=1, justify='left', width=72, anchor="w")
        table_selected.loc[i, 'button'] = check_button
        table_selected.loc[i, 'button'].pack()
    b = tk.Button(root, text="Confirm", command=click_confirm, pady=7, font=("Arial", 13), width=15)
    b.pack(pady=24)
    root.mainloop()


def gather_table_selected(table_selected):
    selected_table_set = set()
    for i in table_selected.index:
        if table_selected.loc[i]['isSelected'].get():
            selected_table_set.add(table_selected.loc[i]['tableName'])
    return selected_table_set


def get_selected_table_set(table_names):
    table_selected = pd.DataFrame(columns=['tableName', 'tableDescription', 'button', 'isSelected'])
    table_selected['tableName'] = table_names
    # Description of the table
    table_desc_dict = {
        'RXNCONSO': 'Concept Names and Sources in RxNorm',
        'RXNSAT': 'Simple Concept and Atom Attributes - that do not have a sub-element structure',
        'RXNSTY': 'The Semantic Type assigned to each concept',
        'RXNREL': 'Relationship between concepts or atoms known to RxNorm',
        'RXNCUICHANGES': 'Changes to the concept_id (RXCUI) for all atoms in RxNorm'
    }
    table_selected['tableDescription'] = table_desc_dict.values()
    select_tables(table_selected)
    selected_table_set = gather_table_selected(table_selected)
    if len(selected_table_set) == 0:
        raise ValueError('Select at least one table!')
    print("Selected Tables: {}".format(selected_table_set))
    return selected_table_set


if __name__ == "__main__":
    table_set = {
        'RXNCONSO', 'RXNSAT', 'RXNSTY', 'RXNREL', 'RXNCUICHANGES'
    }
    selected_table_set = get_selected_table_set(list(table_set))
