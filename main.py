# A rebuilt version of the database handler class.
#         | Only the handler class will be rebuilt here
#         | All other functions that interact with the handler class will be rebuilt af
#         | I've been having issues trying to map out how I want the handler to work with all other functions. So i said, fuck everything else, i'll rebuild those after and work around a good working hanlder
# Use of instances will be used for each database

class db_Handler:
    '''An extremely simple, but yet thought out hanlder. :)-'''
    def __init__(self) -> None:
        # Active Status, 
        self.info = [True]
        # Global Temp Var Identifier
        self.tag = [1]
        # Data
        self.columnStorage = []
        # List Storage
        self.listStorage = []

        # Initialize self amoung classes
        self.edit = self.Edit(self)
        self.data = self.Data(self)
        self.meta = self.Meta(self)
        self.save = self.Save(self)
        self.mods = self.Mods(self)
    def assignTemp(self, value):
        var = ('TempVar'+str(self.tag))
        globals()[var] = value
    def returnTemp(self):
        var = ('TempVar'+str(self.tag))
        return globals()[var]
    def mkGlobalTempVars(self):
        newVar = ('TempVar'+str(self.tag))
        globals()[newVar] = None
    def create(self):
        self.mkGlobalTempVars()
    class Edit:
        def __init__(self, handler):
            self.handler = handler
        def addColumn(self, column):
            '''Add a new column to the database!
            
            Args:
            - Column(str): The name of the column'''
            if type(column) == str:
                self.handler.columnStorage.append(column)
            else:
                raise Exception('\n\nCall Function: --> db_Handler.Edit.addColumn()\nColumn must be a string. Please and thank you.')
        def removeColumn(self, column):
            '''Removes a column from the database!
            
            Args:
            - Column(str): The name of the column
            
            Note: This does not remove the data in rows for this column. Use mods.RemoveEmptyColumnData() to remove empty data from rows.'''
            if type(column) == str:
                if column in self.handler.columnStorage:
                    self.handler.assignTemp(value=column) # Assign column to temp var
                    self.handler.mods.RemoveEmptyColumnData(innerFunction=True) # Remove empty data from rows
                    self.handler.columnStorage.remove(column) # Remove column
                    return
                else:
                    raise Exception('\n\nCall Function: --> db_Handler.edit.removeColumn()\nColumn does not exist in database.')
                # Just incase, u know? Stuff happens.
                raise Exception('\n\nCall Function: --> db_Handler.edit.removeColumn()\nAn unknown error happened :(')
            else:
                raise Exception('\n\nCall Function: --> db_Handler.edit.removeColumn()\nColumn must be a string. Please and thank you.')
        def removeRow(self):
            pass
        def addRow(self, row):
            '''Add a new row to the database! Give me a list of data to add. The list cannot be longer or shorter than the column count.'''
            if len(row) == len(self.handler.columnStorage):
                if type(row) == list:
                    self.handler.listStorage.append(row)
                    return
                else:
                    raise Exception('\n\nCall Function: --> db_Handler.Edit.addRow()\nRow must be a list. Please and thank you.')
                raise Exception('\n\nCall Function: --> db_Handler.Edit.addRow()\nAn unknown error happened :(')
            else:
                raise Exception('\n\nCall Function: --> db_Handler.Edit.addRow()\nRow length must be the same as the column length.')
    class Mods:
        '''Things I personally would love to have built into a handler. But done simply! None of that complicated shit.'''
        def __init__(self, handler):
            self.handler = handler
        def RemoveEmptyColumnData(self, column=None, innerFunction=False):
            '''Want to remove all the data from rows with a column that has been deleted? Well just use me! This function is used within edit.removeColumn() already. But if you manually remove a column within the data files i'm here to help.
            
            Args:
            - column(int or str): The index of the column name removed. Starting from 0+, not 1+. If your a function calling, specify name, then remove column.'''
            column = self.handler.returnTemp()
            self.handler.assignTemp(value=None)
            varType = type(column)
            if varType == str:
                # Get index of column
                for i in range(len(self.handler.columnStorage)):
                    if self.handler.columnStorage[i] == column:
                        # set index
                        column = i
                        # Now alter varType to int and return to run
                        varType = int
                        break
            if varType == int:
                for x in range(len(self.handler.listStorage)):
                    self.handler.listStorage[x].pop(column)
                return
            else:
                raise Exception('\n\nCall Function: --> db_Handler.mods.RemoveEmptyColumnData()\nColumn must be either int or str.')
        def EmptyEntryFill(self, column, value):
            '''Used after creating a new column to fill all rows with no value to have a value.
            
            Args:
            - column: The column to fill empty values with
            - value: The value to fill the empty values with'''
            pass
    class Data:
        def __init__(self, handler):
            self.handler = handler
        def returnStatus(self):
            return self.handler.info[0]
        def columns(self):
            return self.handler.columnStorage
    class Save:
        def __init__(self, handler):
            self.handler = handler
        '''Saves the entire db instance'''
        # You can save a database even if it's empty. Allows for an easy setup of hundreds of databases.
        # Vars saved: tag, columnStorage, listStorage
        pass
    def load(self):
        '''Loads data from a saved database. Requires this database instance to be empty.'''
        if self.handler.columnStorage != [] or self.handler.listStorage != []:
            raise Exception('\n\nCall Function: --> db_Handler.load()\nData already exists in this database. Cannot load data into an existing database.')
        else:
            # Load data
            pass
    class Meta:
        def __init__(self, handler):
            self.handler = handler

        '''Add of Modify meta data of the database.'''
        def status(self, newStatus=None):
            '''Change the status of the database. Doesn\'t disable the handler. Used as a marker.
            Args:
            - True: Yes, this handler is still used
            - False: Nah, we don\'t use this one anymore'''
            if type(newStatus) == bool:
                self.handler.info[0] = newStatus
                return None
            raise Exception('Invalid status type. Must be a boolean.')
        

# -----------------------------------------------------------------
# | Testing the handler, and seeing how it works. So far, so good.|
# |      With the intent of easy use, and easy to understand.     |
# |                 Also to just look nice. :)                    |
# -----------------------------------------------------------------


# Create database:
MonkeyDB = db_Handler()

# Change and see status:
MonkeyDB.meta.status(newStatus=False)
print('Status',MonkeyDB.data.returnStatus())
# Add column:
print('Creating columns...')
MonkeyDB.edit.addColumn('Names')
MonkeyDB.edit.addColumn('Is Stupid?')
print('Columns:',MonkeyDB.data.columns(),'\n\n')


# Add row:
print('Adding rows...')
MonkeyDB.edit.addRow(['Turtle', 'Yes'])
MonkeyDB.edit.addRow(['Mike', 'No'])
print('Rows:',MonkeyDB.listStorage,'\n\n')

# Remove column:
print('Removing column...')
MonkeyDB.edit.removeColumn('Names')
print('Columns:',MonkeyDB.data.columns())
print('Rows:',MonkeyDB.listStorage,'\n\n')

# Save database:


# Load database:






