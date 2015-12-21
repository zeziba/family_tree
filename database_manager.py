__author__ = 'Charles Engen'

# SQLite is a bd manager, it is something you will want to learn
import sqlite3
# Tempfile is a built-in method which finds the tempfile no matter the system
import tempfile
# Makedirs creates directories, getvwd gets the current working directory
from os import makedirs, getcwd
# Join takes any amount of inputs and gives back a single string to use for drive location
from os.path import join

# This try statement looks to see if there is a mainpath.txt
# if it cannot find said file it will create the db in the temp directory
# else it creates it where the main_path file says to. Change it as
# necessary.
try:
    with open(join(getcwd(), "main_path.txt"), 'r') as file:
        file.seek(0)
        _path_ = file.readline()
    print("Pass")
except FileNotFoundError:
    _path_ = join(tempfile.gettempdir(), "Family_Database")

# This try statement creates the main path for the db to use,
# depending on the previous statement. It creates a directory to store the
# database in.
try:
    makedirs(_path_)
except FileExistsError:
    try:
        makedirs(join(_path_, "Family_Database"))
        _path_ = join(_path_, "Family_Database")
    except FileExistsError:
        _path_ = join(_path_, "Family_Database")

# This try statement checks the SQLite version, you might have to add more
# code here if you use version specific code. You will then have
# to tell the user that they failed to meet your requirements.
try:
    with sqlite3.connect(join(_path_, 'family_tree.db')) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT SQLITE_VERSION()')
        data = cursor.fetchone()
        print("SQLite Version: %s" % data)
        cursor.execute("CREATE TABLE IF NOT EXISTS FAMILIES "
                       "(ID integer primary key, name text)")
except:
    print("Failed to load Database")


def _give_db_command(command):
    """
    This function allows us to communicate basic commands with SQLite.
    :param command: Pass the command you want to execute.
    :return: None
    """
    with sqlite3.connect(join(_path_, 'family_tree.db')) as CONN:
        c = CONN.cursor()
        c.execute(command)


def set_path(path__):
    """
    This function sets the path to store the database, change when needed.
    :param path__: Pass the path to save the database at.
    :return: None
    """
    global _path_
    _path_ = path__


def create_family_member(name):
    """
    This function allows us to create family member entries in our database.
    :param name: Pass the full name of the family member.
    :return: Gives back a string that details completion or failure.
    """
    _give_db_command("CREATE TABLE IF NOT EXISTS FAMILIES "
                     "(ID integer primary key, name text)")
    with sqlite3.connect(join(_path_, 'family_tree.db')) as CONN:
        print(name)
        c = CONN.cursor()
        c.execute("SELECT rowid FROM FAMILIES WHERE name = ?", (name,))
        data_ = c.fetchall()
        if len(data_) == 0:
            c.execute("INSERT INTO FAMILIES(name) values('%s')" % name)
            return '%s was added to the Families Database' % name
        else:
            return '%s is already in the database with an id: %s' % (name, data_)


def get_family_members():
    """
    This returns a set of family members, we will use this data to display
    on the screen.
    :return: Family member data.
    """
    with sqlite3.connect(join(_path_, 'family_tree.db')) as CONN:
        c = CONN.cursor()
        c.execute("SELECT * FROM FAMILIES")
        return c.fetchall()


def _remove_member(memberID=None, memberName=None):
    """
    This function allows us to delete entries from the family members
    based off of the name or ID.
    :param memberID: ID of family member
    :param memberName: Full name of family member
    :return: String telling what was deleted.
    """
    if memberID is not None:
        _give_db_command("DELETE FROM FAMILIES IF EXISTS WHERE ID = %s" % memberID)
    if memberName is not None:
        _give_db_command("DELETE FROM FAMILIES IF EXISTS WHERE name = '%s'" % memberName)
    return "%s was deleted"


# The following code uses the fact that python calls a module
# __main__ if it is being used as the main file, when that is the case
# it runs the code.
if __name__ == "__main__":
    _give_db_command("CREATE TABLE IF NOT EXISTS FAMILIES "
                     "(ID integer primary key, name text)")
    print(create_family_member("John Bad Man"))
    print(get_family_members())
    _give_db_command("DROP TABLE IF EXISTS FAMILIES")