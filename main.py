# A rebuilt version of the database handler class.
#         | Only the handler class will be rebuilt here
#         | All other functions that interact with the handler class will be rebuilt af
#         | I've been having issues trying to map out how I want the handler to work with all other functions. So i said, fuck everything else, i'll rebuild those after and work around a good working hanlder
# Use of instances will be used for each database

# Ideas for settings:
# max_allowsRows - A db can only have ? rows within it.

def incrimatationHandler():
    '''The use of instances makes usage of a single variable difficult along with other management issues. This helps with that :)-'''
    # Functions to apply incrimataions to:
    # db_Handler.mkGlobalTempVars()
    pass
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
        def addColumn(self, column, value=None):
            '''Add a new column to the database!
            
            Args:
            - Column(str): The name of the column
            - Value(str/None): The value to fill the empty rows with for the new column. (Default is None)
            
            Notes:
            All rows for this column will be empty. Use mods.EmptyEntryFill() to fill empty values in rows.'''
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
        def removeRow(self, index):
            '''Remove a row from the database! Give me the index of the row to remove. The index starts from 0.
            - To get a index range use: data.row_indexRangeCount()
            - To return the row of an index use: data.row_indexLookup()
            '''
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
        def EmptyEntryFill(self, column, value, NoListValue=['', None], doesIndexForColumnExist=True):
            '''Used after creating a new column to fill all rows with no value to have a value.
            \n
            \nArgs:
            \n- column: The column to fill empty values with
            \n- value: The value to fill the empty values with
            \n- NoListValue: The values to consider as empty. Default is ['', None]
            \n- doesIndexForColumnExist: Does the column have an index created for each row?
            \n    Ex: This example doesn't have an index for each row yet. So it would be False.
            \n    Name | Age | New Column
            \n    Mike | 23  | 
            \n    Mark | 24  |'''
            rows = self.handler.listStorage
            columns = self.handler.columnStorage.index(column) # Gets index of specified column
            for i in range(len(rows)):
                for emptyValue in NoListValue:
                    if rows[i][columns] == emptyValue:
                        rows[i][columns] = value
    class Data:
        def __init__(self, handler):
            self.handler = handler
            
        def returnStatus(self):
            return self.handler.info[0]
        
        def columns(self):
            return self.handler.columnStorage
        
        def row_indexLookup(self, index):
            '''Returns the data of a row based on the index given. The index starts from 0.'''
            return self.handler.listStorage[index]
        
        def row_indexRangeCount(self):
            '''Returns the amount of rows in the database. This function subtracts 1 as the index starts from 0. So 5 items in a list will return 4 since the index starts from 0.'''
            out = len(self.handler.listStorage)
            if out > 0:
                return out-1
            return 0
        
        def findRowWithValues(self, columns, value):
            '''Returns the index of a row with one or multiple values. Specify column for each. If multiple rows have the same value, it will return the first row found.
            Read below for how returns are handled.
            Usage Ex:
            columns = ['Name', 'Age']
            value = ['Mike', 23]
            
            Args:
            - Columns: The columns to search for the value in
            - Value: The value to search for
            
            Returns:
            Example: [[0, 1], [2, 1], [9, 2]]
            - First value: is index of row
            - Second value: is amount of matches with data given for the row found.
            '''
            # Indexs Of Found matches
            found = []
            columnSearch = self.handler.columnStorage
            columnIndexsForSearch = []
            # Get indexs of columns, for faster searching
            for i in range(len(columns)):
                if columns[i] in columnSearch:
                    columnIndexsForSearch.append(columnSearch.index(columns[i]))
                else:
                    raise Exception('\n\nCall Function: --> db_Handler.Data.findRowWithValues()\nColumn does not exist in database.')
            
            # Search for values, and count matches for each row
            print('Indexs:', columnIndexsForSearch)
            for x in range(len(self.handler.listStorage)):
                matchesForThisRow = 0
                for y in range(len(columnIndexsForSearch)):
                    if self.handler.listStorage[x][columnIndexsForSearch[y]] == value[y]:
                        matchesForThisRow += 1
                if matchesForThisRow > 0:
                    found.append([x, matchesForThisRow])

            # Verify found has values
            # --> If not, return None
            if found == []:
                return None
            # <-- If so, return found
            return found
    
        def displayDataOnScreen(self, displayIndex=True):
            '''Prints the table on the screen.'''
            print('< Table for Database: '+str(self.handler.tag[0])+' >')
            columnsNeat='|'
            # Start with the columns
            columns = self.handler.columnStorage
            for i in range(len(self.handler.columnStorage)):
                columnsNeat+=self.handler.space(var = columns[i], max_length=15, hide=True, centerText=True)+'|'
            # Print it!
            print(columnsNeat)
            for x in range(len(columnsNeat)):
                print('-', end='')
            print()

            # Now the rows
            rows=self.handler.listStorage
            for x in range(len(rows)):
                rowsNeat='|'
                for y in range(len(rows[x])):
                    rowsNeat+=self.handler.space(var = rows[x][y], max_length=15, hide=True, centerText=True)+'|'
                if displayIndex:
                    print(rowsNeat, 'Index:', x)
                else:
                    print(rowsNeat)
            

    # Reused from my old handler. Why change something that works? :)- Did make a few changes to it tho.
    def space(self, var=None, max_length=10, hide=False, return_ShortenNotice=False, centerText=False):
        var = str(var)
        if isinstance(var, str):
            if centerText:
                var = var.center(max_length)
                return var
            else:
                length = len(var)
                if hide == False: print('Input length:', length)
                notice = False
                if length < max_length:
                    # Add spaces to fit
                    if hide == False: print('Total spaces to add:', max_length - length)
                    for i in range(max_length - length):
                        var += ' '
                    if hide == False: print('Final Length:', len(var))
                    if return_ShortenNotice == True:
                        return var, notice
                    else:
                        return var
                if length > max_length:
                    # Shorten to fit
                    var = var[0:max_length]
                    if hide == False: print('Final Length:', len(var))
                    notice = True
                    if return_ShortenNotice == True:
                        return var, notice
                    else:
                        return var
                if return_ShortenNotice == True:
                    return var, False
                else:
                    return var
        else:
            if hide == False: print('Error: Input is not string.')
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
MonkeyDB.edit.addColumn('Is Human?')
MonkeyDB.edit.addColumn('Is Smart?')
MonkeyDB.edit.addColumn('Is Alive?')
MonkeyDB.edit.addColumn('Is Dead?')
print('Columns:',MonkeyDB.data.columns(),'\n\n')


# Add row:
print('Adding rows...')
MonkeyDB.edit.addRow(['Turtle', 'Yes', 'Perhaps', 'No', 'Yes', 'No'])
MonkeyDB.edit.addRow(['Mike', 'No', 'Most Likely', 'Yes', 'Yes', 'No'])
MonkeyDB.edit.addRow(['Mark', 'Yes', 'Perhaps', 'No', 'Yes', 'No'])
MonkeyDB.edit.addRow(['Turtle', 'Yes', 'Perhaps', 'No', 'Yes', 'No'])
MonkeyDB.edit.addRow(['Mike', 'No', 'Most Likely', 'Yes', 'Yes', 'No'])
MonkeyDB.edit.addRow(['Mark', 'Yes', 'Perhaps', 'No', 'Yes', 'No'])
MonkeyDB.edit.addRow(['Turtle', 'Yes', 'Perhaps', 'No', 'Yes', 'No'])
MonkeyDB.edit.addRow(['Mike', 'No', 'Most Likely', 'Yes', 'Yes', 'No'])
MonkeyDB.edit.addRow(['Mark', 'Yes', 'Perhaps', 'No', 'Yes', 'No'])
MonkeyDB.edit.addRow(['Turtle', 'Yes', 'Perhaps', 'No', 'Yes', 'No'])
MonkeyDB.edit.addRow(['Mike', 'No', 'Most Likely', 'Yes', 'Yes', 'No'])
print('Rows:',MonkeyDB.listStorage,'\n\n')

# Remove column:
print('Removing column...')
MonkeyDB.edit.removeColumn('Names')
print('Columns:',MonkeyDB.data.columns())
print('Rows:',MonkeyDB.listStorage,'\n\n')

# Remove row:
print('Removing Row:')
output = MonkeyDB.data.row_indexRangeCount()
print('row_indexRangeCount return:',output)
output1 = MonkeyDB.data.findRowWithValues(columns=['Is Human?', 'Is Stupid?'], value=['Perhaps', 'Yes'])
print('findRowWithValues return:',output1)

MonkeyDB.edit.removeRow(0)
print('Rows:',MonkeyDB.listStorage,'\n\n')
MonkeyDB.data.displayDataOnScreen()


# Fill empty values
print('Filling empty values...')
MonkeyDB.edit.addColumn('Is Dead?')
MonkeyDB.mods.EmptyEntryFill('Is Dead?', 'No')


# Save database:


# Load database:






# data.addColumn() - Needs to create empty values for all rows in the new column
# mods.EmptyEntryFill() - Needs doesIndexForColumnExist option to be implemented
# edit.removeRow() - Hasn't been done at all yet.
