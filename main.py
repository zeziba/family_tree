__author__ = 'Charles Engen'

import database_manager
import tkinter


class ScrolledTextArea:

    def __init__(self, parent):
        self.frame = tkinter.Frame(parent)
        self.frame.pack()

        self.text = None

        self.textPad(self.frame)

    def textPad(self, parent):
        textPad = tkinter.Frame()

        self.text = tkinter.Text(textPad, height=10, width=20)

        scroll = tkinter.Scrollbar(textPad)
        self.text.configure(yscrollcommand=scroll.set)

        self.text.pack(side='left')
        scroll.pack(side="right", fill='y')
        textPad.pack(side="top")

    def add_text(self, data):
        self.text.delete('1.0', tkinter.END)
        for line in data:
            self.text.insert(tkinter.INSERT, line[1], tkinter.END, "\n")


class MainFrame(tkinter.Frame):

    def __init__(self):
        tkinter.Frame.__init__(self)
        # Font Data
        self.font_data_display = ('times', 16)
        self.font_data_menu = ('times', 14)

        # This is the text area where the names will be displayed
        self.display_text = tkinter.Label(self, text="")

        self.text = ScrolledTextArea(self)
        # End text area

        # This is the Input area
        self.input_var_name = tkinter.StringVar()
        self.input_widget = tkinter.Entry(self, textvariable=self.input_var_name,
                                          font=self.font_data_display, relief=tkinter.SUNKEN)

        # Here we bind the enter key to the entry widgets submit option
        self.input_widget.bind('<Return>', self.submit_name)
        self.input_widget.bind('<Button-1>', self.clear_text_area)

        # This packs all the widgets so they will get displayed
        self.display_text.pack(side="top")
        self.pack(side="right")
        self.input_widget.pack(side="left")

        # This will update the text box
        self.update_text_area()

    def set_entry_box(self):
        self.input_var_name.set("Please enter the Full Name.")

    def update_text_area(self):
        self.text.add_text(database_manager.get_family_members())
        self.set_entry_box()

    def submit_name(self, *args, **kwargs):
        database_manager.create_family_member(self.input_var_name.get())
        self.after(400, self.update_text_area)

    def clear_text_area(self, *args, **kwargs):
        self.input_var_name.set("")


def mainloop_():
    root = MainFrame()
    root.mainloop()


if __name__ == "__main__":
    database_manager.create_family_member("John Apple")
    database_manager.create_family_member("Ruth Anne")
    database_manager.create_family_member("Apple May")
    mainloop_()