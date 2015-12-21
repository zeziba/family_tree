__author__ = 'Charles Engen'

# This import statement imports our custom db manager to use with the GUI
# You always want to keep separate parts from intermingling. This
# prevents bugs.
import database_manager
# This is the GUI manager, it allows us to create all the wonderful
# GUI elements that we need, we just have to program them. I use this
# one because it is built in and I do not want to create OpenGL widgets
# for this type of project.
import tkinter


class ScrolledTextArea:
    """
    This class will be instantiated in our main class. The purpose of this class
    is to create a text area to display the names of our family database.
    """

    def __init__(self, parent):
        """
        This method is always called when our class is used, it creates
        a tkinter frame object and .packs() it. This means that tells tkinter
        to display it on the screen.

        It also sets the text field and creates a textpad(our method) area to work with.
        :param parent: Pass the parent widget
        :return: None
        """
        self.frame = tkinter.Frame(parent)
        self.frame.pack()

        self.text = None

        self.textPad(self.frame)

    def textPad(self, parent):
        """
        This method is a widget framework that is used to create a area
        for use to display our text.
        :param parent: Pass the parent widget
        :return: None
        """
        textPad = tkinter.Frame()

        self.text = tkinter.Text(textPad, height=10, width=20)

        scroll = tkinter.Scrollbar(textPad)
        self.text.configure(yscrollcommand=scroll.set)

        self.text.pack(side='left')
        scroll.pack(side="right", fill='y')
        textPad.pack(side="top")

    def add_text(self, data):
        """
        This method allows us to add text to our widget when needed.
        First it clears the text area and then populates it with the
        passed in data, which can be any iterable data type.
        :param data:
        :return:
        """
        self.text.delete('1.0', tkinter.END)
        for line in data:
            self.text.insert(tkinter.INSERT, line[1], tkinter.END, "\n")


class MainFrame(tkinter.Frame):
    """
    This is the main frame of our GUI, it is what will contin all the other
    widgets and manage trier size and such.

    TODO:
        Add automatic resizing for children widgets
    """

    def __init__(self):
        """
        This method is called every time we use our main frame widget.
        There are several components to it and I have labeled them
        accordingly.
        :return:
        """
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
        """
        This method gives us the ability to set the input box's field before entry.
        :return: None
        """
        self.input_var_name.set("Please enter the Full Name.")

    def update_text_area(self):
        """
        This method updates the input area, it also grabs the input and stores it into the
        database using the manager
        :return: None
        """
        self.text.add_text(database_manager.get_family_members())
        self.set_entry_box()

    def submit_name(self, *args, **kwargs):
        """
        This method gives us the ability to submit our entry box's information into our database,
        it also updates it after 400 milli-secs.
        :param args: Tkinter pass information
        :param kwargs: Tkinter pass information
        :return:
        """
        database_manager.create_family_member(self.input_var_name.get())
        self.after(400, self.update_text_area)

    def clear_text_area(self, *args, **kwargs):
        """
        This method clears the entry widgets text area.
        :param args: Tkinter pass information
        :param kwargs: Tkinter pass information
        :return:
        """
        self.input_var_name.set("")


def mainloop_():
    """
    This function is our mainloop, it will decide what runs when and how.
    :return: None
    """
    root = MainFrame()
    root.mainloop()


# The following code uses the fact that python calls a module
# __main__ if it is being used as the main file, when that is the case
# it runs the code.
if __name__ == "__main__":
    database_manager.create_family_member("John Apple")  # we add these entries to populate our database del of needed
    database_manager.create_family_member("Ruth Anne")
    database_manager.create_family_member("Apple May")
    mainloop_()  # Runs the mainloop