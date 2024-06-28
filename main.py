# A rebuilt version of the database handler class.
#         | Only the handler class will be rebuilt here
#         | All other functions that interact with the handler class will be rebuilt af
#         | I've been having issues trying to map out how I want the handler to work with all other functions. So i said, fuck everything else, i'll rebuild those after and work around a good working hanlder
# Use of instances will be used for each database

# Ideas for settings:
# max_allowsRows - A db can only have ? rows within it.
# CaseSensativityAmoungColumnNames=True

#Grouped Files
# 1) handler_showcase.py
# 2) SaveHeader.txt


# -------------------------------------------------------------- #
#                                                                #
#                   Created by Brandon R.                        #
#               Supported and backed by Dakota H.                #
#                                                                #
# -------------------------------------------------------------- #
import os, sys, shutil
print('Current Path Set:', os.getcwd())
os.chdir('App')
print('Current Version: Testing Only!')




# Temp data (Moving to save file when that has been made/developed)
incrimatationCount='AAAA' 
'''1 letter, then 3 numbers or letters.'''
usedCountList = []

# Temp data (Moving to save file when that has been made/developed)
def generateNextIncrement():
    global incrimatationCount
    # Check to see if current Count has been used yet.
    if incrimatationCount in usedCountList:
        usedCountList.append(incrimatationCount)
        return incrimatationCount
    else:
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        chars_with_numbers = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        tS = len(chars_with_numbers)  # totalSize of letter list(s) each, -1 if index

        # Convert the incrimatationCount to a list for easier manipulation
        incrimatationList = list(incrimatationCount)

        for i in range(len(incrimatationList) - 1, -1, -1):
            # If the current character is not the last one in chars
            if i == 0:
                current_chars = chars
            else:
                current_chars = chars_with_numbers

            if incrimatationList[i] != current_chars[-1]:
                # Find the index of the current character in chars and increment it
                nextIndex = current_chars.index(incrimatationList[i]) + 1
                incrimatationList[i] = current_chars[nextIndex]
                break
            else:
                # If the current character is the last one in chars, reset it to the first character
                incrimatationList[i] = current_chars[0]

        # Convert the list back to a string
        incrimatationCount = ''.join(incrimatationList)
        usedCountList.append(incrimatationCount)
        return incrimatationCount
    

class db_Handler:
    '''An extremely simple, but yet thought out hanlder. :)-'''
    def __init__(self) -> None:
        # Active Status, 
        self.info = [True]
        # Global Temp Var Identifier
        self.tag = [generateNextIncrement()] # Makes self tag unique for each database, temp vars don't colide this way.
        # Data
        self.columnStorage = []
        # List Storage
        self.listStorage = []
        # Owner of the database
        self.owner = None

        # Initialize self amoung classes, and classify user functions
        self.edit = self.Edit(self)
        self.data = self.Data(self)
        self.meta = self.Meta(self)
        self.save = self.Save(self)
        self.mods = self.Mods(self)
        self.randomMath = self.RandonMath(self)
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
        
        def addColumn(self, column, value=None, AutoFillEmptyRows=True):
            '''Add a new column to the database!
            
            Args:
            - Column(str): The name of the column
            - Value(str/None): The value to fill the empty rows with for the new column. (Default is None)

            Settings:
            - AutoFillEmptyRows: True/False
            
            Notes:
            All rows for this column will be empty. Use mods.EmptyEntryFill() to fill empty values in rows.'''
            if type(column) == str:
                self.handler.columnStorage.append(column)
                if AutoFillEmptyRows:
                    self.handler.mods.EmptyEntryFill(column=column, value=value, doesIndexForColumnExist=True)
            else:
                raise Exception('\n\nCall Function: --> db_Handler.Edit.addColumn()\n - Column must be a string.')
        
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
            if type(index) == int:
                if index < len(self.handler.listStorage):
                    self.handler.listStorage.pop(index)
                    return
                else:
                    raise Exception('\n\nCall Function: --> db_Handler.Edit.removeRow()\nIndex is out of range.')
            else:
                raise Exception('\n\nCall Function: --> db_Handler.Edit.removeRow()\nIndex must be an integer.')
        
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
        
        def EmptyEntryFill(self, column, value, NoListValue=['', None], doesIndexForColumnExist=False):
            '''Used after creating a new column to fill all rows with no value to have a value.
            \n
            \nArgs:
            \n- column: The column to fill empty values with
            \n- value: The value to fill the empty values with
            \n- NoListValue: The values to consider as empty. Default is ['', None]
            \n\n- doesIndexForColumnExist: Does the column have an index created for each row? Default is False.
            \n    Ex: This example doesn't have an index for each row yet. So it would be False.
            \n    Name | Age | New Column
            \n    Mike | 23  | 
            \n    Mark | 24  |'''
            # Make local variables, for faster sequantial access
            rows = self.handler.listStorage
            columns = self.handler.columnStorage.index(column) # Gets index of specified column
            # Loop through rows
            for i in range(len(rows)):
                # Loop through columns
                for emptyValue in NoListValue: 
                    try:
                        if rows[i][columns] == emptyValue:
                            rows[i][columns] = value
                    except:
                        if doesIndexForColumnExist:
                            # If no actual index exists for the column, create it with the value of (value)-var
                            rows[i].append(value) # Add value to row
                        else:
                            raise Exception('\n\nCall Function: --> db_Handler.mods.EmptyEntryFill()\n - Index for column does not exist. Retry with doesIndexForColumnExist=True.')
            # Update listStorage
            self.handler.listStorage = rows
                    
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
            
    # Reused from my old handler. Why change something that works? :)- Did make a few changes to it tho. :laugh:
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
    class RandonMath:
        def __init__(self, handler):
            self.handler = handler
        def tireRotationsMpH(speed_mph = 400,
            tire_diameter_inches = 25.5,
            feet_per_mile = 5280,
            minutes_per_hour = 60):
            '''Calculate tire rotations per minute based on tire diameter and speed in miles per hour. Used to calculate RPM required from an electric motor to achieve a certain speed.'''
            import math

            # Calculations
            circumference_inches = math.pi * tire_diameter_inches
            circumference_feet = circumference_inches / 12  # Convert inches to feet
            speed_feet_per_minute = speed_mph * feet_per_mile / minutes_per_hour
            rpm = speed_feet_per_minute / circumference_feet

            print(f'A tire with a diameter of {tire_diameter_inches} inches will rotate {rpm:.2f} times per minute; or be the rpm motor requirements for an illegal moped, to travel at a speed of {speed_mph} mph.')

    class Backup:
        '''Saving the database, creates a backup each time. The backup is saved in a folder called "Backups". This class is used to manage the backups.'''
        def __init__(self, handler):
            self.handler = handler
        
        def createBackupFolder(self):
            '''Creates a folder to store backups.'''
            os.mkdir('db_'+str(self.handler.tag[0])+'_Backups')
        
        def clearBackups(self):
            '''Clears all backups for the database.'''
            pass
        
        def compressBackups(self):
            '''Compresses all backups for the database into a zip file.'''
            pass

    class Save:
        def __init__(self, handler):
            self.handler = handler

        def all(self):
            '''Saves the entire db instance. This includes all data, columns, and meta data.'''
            # You can save a database even if it's empty. Allows for an easy setup of hundreds of databases.
            # Vars saved: tag, columnStorage, listStorage, incrementCount, usedCountList

            # Make the name for our save file
            saveNm='db_'+str(self.handler.tag[0])+'.txt'

            # Check if file exists
            if os.path.exists('db_'+str(self.handler.tag[0])+'.txt'):
                # Check if folder exists
                if not os.path.exists('Backups'):
                    os.mkdir('db_'+str(self.handler.tag[0])+'_Backups')

                # If so, copy file to backups folder

                backup_folder = 'db_' + str(self.handler.tag[0]) + '_Backups'
                if not os.path.exists(backup_folder):
                    os.mkdir(backup_folder)
                backup_files = os.listdir(backup_folder)
                num_files = len(backup_files)
                # Make the name for our backup file
                saveNmBk = 'db_'+str(num_files)+'_'+str(self.handler.tag[0])+'.txt'
                os.rename(saveNm, saveNmBk)
                backup_file = os.path.join(backup_folder, saveNmBk)
                shutil.copyfile(saveNmBk, backup_file)

                # Then, Delete the save file
                os.remove(saveNmBk)


            # Now, we save the database.
            with open(saveNm, 'w') as f:
                f.write('tag = '+str(self.handler.tag[0])+'\n')
                f.write('columnStorage = '+str(self.handler.columnStorage)+'\n')
                f.write('listStorage = '+str(self.handler.listStorage)+'\n')
                f.write('incrementCount = '+str(incrimatationCount)+'\n')
                f.write('usedCountList = '+str(usedCountList)+'\n')
                f.close()

            # All done!
            print('Database saved as:', saveNm)

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

        '''Add or Modify meta data of a database.'''
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
MonkeyDB.edit.addRow(['Tacos', 'Turtles', 'Tacos', 'Turtles', 'Tacos', 'Turtles'])
print('Rows:',MonkeyDB.listStorage,'\n\n')

# Remove column:
print('Removing column...')
MonkeyDB.edit.removeColumn('Names')
print('Columns:',MonkeyDB.data.columns())
print('Rows:',MonkeyDB.listStorage,'\n\n')

# Add column with no value:
print('Adding column with no value...')
MonkeyDB.edit.addColumn('Trash')

# Remove row:
print('Removing Row:')
output = MonkeyDB.data.row_indexRangeCount()
print('row_indexRangeCount return:',output)
output1 = MonkeyDB.data.findRowWithValues(columns=['Is Human?', 'Is Stupid?'], value=['Tacos', 'Turtles'])
print('findRowWithValues return:',output1)
MonkeyDB.edit.removeRow(0)

MonkeyDB.edit.removeRow(0)
print('Rows:',MonkeyDB.listStorage,'\n\n')
MonkeyDB.data.displayDataOnScreen()


# Fill empty values
print('Filling empty values...')
MonkeyDB.edit.addColumn('Is Dead?')
MonkeyDB.mods.EmptyEntryFill('Is Dead?', 'No')

print(MonkeyDB.columnStorage)
# Save database:
MonkeyDB.save.all()

# Load database:


# Random Math:
MonkeyDB.RandonMath.tireRotationsMpH()





# data.addColumn() - Needs to create empty values for all rows in the new column
# edit.removeRow() - Hasn't been done at all yet.
# edit.addRow() - Needs to verify the input list is less than or equal to the column count. If less than, fill empty values with None. If more than, raise an error.
# incrimatationHandler() - Needs to be designed. Will be used for creating temp vars for each database.



# Updates June/24/2024:
# 1)
# - mods.EmptyEntryFill()
    # Implemented doesIndexForColumnExist option. 
    # Usage: mods.EmptyEntryFill(column='Am I A Turtle?', value='No', doesIndexForColumnExist=True)
# 2)
# - generateNextIncrement()
    # Implemented a function to generate the next increment for the database usage.
    # For creating temp vars, that do not colide with other databases temp vars.
    # Usage: db_Handler.mkGlobalTempVars()
