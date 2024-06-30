# A rebuilt version of the database handler class.
#         | Only the handler class will be rebuilt here
#         | All other functions that interact with the handler class will be rebuilt af
#         | I've been having issues trying to map out how I want the handler to work with all other functions. So i said, fuck everything else, i'll rebuild those after and work around a good working hanlder
# Use of instances will be used for each database

# Ideas for settings:
# max_allowsRows - A db can only have ? rows within it.
# max_allowColumns - a db can only have ? columns within it.
# CaseSensativityAmoungColumnNames=True
# loadDBOnEachStartup = 'AAAA' or None(Doesn't load anything)

#Grouped Files
# 1) handler_showcase.py


# -------------------------------------------------------------- #
#                                                                #
#                   Created by Brandon R.                        #
#               Supported and backed by Dakota H.                #
#                                                                #
# -------------------------------------------------------------- #
import os, sys, shutil, random, time, hashlib, builtins
sys.set_int_max_str_digits(1000000)
print('Current Path Set:', os.getcwd())
os.chdir('App')
print('Current Version: Testing Only!')




# Temp data (Moving to save file when that has been made/developed)
incrimatationCount='AAAA' 
'''1 letter, then 3 numbers or letters.'''
# Variabled save file additions
usedCountList = []
lastDatabaseSaved = None
mALCount = 0 # Malicios Activity Logger Count

# Temp data (Moving to save file when that has been made/developed)
def generateNextIncrement():
    global incrimatationCount, usedCountList
    # Check to see if current Count has been used yet.

    if incrimatationCount not in usedCountList:
        usedCountList.append(incrimatationCount)
        return incrimatationCount
    else:
        print('Gen new tag')
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
        # UserName / Passwords
        self.knownUsers = []
        # Permission / ID's
        self.permissions = []
        # User Logged In
        self.userLogged = [] # Name, Perm, ID
        # Permissions allowed
        self.allowedPermissions = ['admin', 'normal', 'basic']
        # Unique ID for userPW:
        self.userPW = None

        # Initialize self amoung classes, and classify user functions
        self.edit = self.Edit(self)
        self.data = self.Data(self)
        self.meta = self.Meta(self)
        self.save = self.Save(self)
        self.mods = self.Mods(self)
        self.users = self.Users(self)
        self.encryption = self.Encryption(self)
        self.randomMath = self.RandonMath(self)
        self.maliciosActivityLogger = self.MaliciosActivityLogger(self)
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
        '''Used to setup a database. Required if user accounts will be used.'''
        self.mkGlobalTempVars()
        self.userPW = self.encryption.uniqueIDGen(maxKeyLength=50, password='UserPW', consistantOutput=False)
    class MaliciosActivityLogger:
        '''This class is only used/called when data between variables doesn't match and may be a sign of malicios activity.
        This class logs all calls to itself and will take precautions if malicios data is found depending from where it occured.'''
        def __init__(self, handler):
            self.handler = handler

        def report(self, type, data):
            '''Report malicios activity. This function may be called by mistake if code is improperly maintainted or if a bug occurs.
            
            Malicous Types: Set type as one of the following in string format. Case sensative.
            - (Data Mismatch): Data between variables doesn't match or is invalid.
            - 
            '''
            knownType = ['Data Mismatch', 'LoggedInUserDoesNotExist']
            if type not in knownType:
                raise Exception('Invalid Malicios Type. Please use one of the following: {}'.format(knownType))
            # Log the data
            self.log(type=type, data=data)
            
        def log(self, type, data):
            '''Logs data into a logger file.'''
            # if exists, add to file
            if os.path.exists('activityLogger.txt') == True:
                file = open('activityLogger.txt', 'a')
            # if not, create file
            else:
                file = open('activityLogger.txt', 'w')
            # Write data. type, time and date, then data, then add 2 lines for spacing
            file.write('Type:',type,'Time:',time.time(),'Date:',time.strftime('%Y-%m-%d %H:%M:%S'),'\nData:',data,'\n\n')
            file.close()
            
    class Users:
        '''User management class. This class is used to manage users within the database.
        \n - Allows you to do the following:
        \n - disable/enable users
        \n - Create/Remove users
        \n - Enable/Disable writing of particular columns in the database
        '''
        # 
        def __init__(self, handler):
            self.handler = handler
        
        def permissionsAllowed(self, perm):
            '''Checks wether a permission is allowed to be used.
            Retuns:
            - True: Allowed
            - False: Not allowed'''
            if perm in self.handler.allowedPermissions:
                return True
            return False

        def verifyUserLoggedExists(self):
            '''Checks whether the user logged actually exists within known users. If not, assume malicous activity occured. Reports are automaically done.
            
            Returns:
            - True: User Found/Verified
            - False: User Not Found/Invalid Data
            '''
            nameF, permF = False, False
            for user in self.handler.knownUsers:
                for perm in self.handler.permissions:
                    if user[0] == self.handler.userLogged[0]:
                        nameF = True
                        if perm[0] == self.handler.userLogged[1]:
                            permF = True
                            if perm[1] == self.handler.userLogged[2]:
                                return True
            if nameF == False or permF == False:
                self.handler.MaliciosActivityLogger.report(type='LoggedInUserDoesNotExist', data=[self.handler.userLogged[0], self.handler.userLogged[1], self.handler.userLogged[2]])
            # Else return False
            return False

        def checkNameInUse(self, name):
            '''Check argument (name) against know users.
            Args:
            - name(str): (name) to check
            Returns: 
            - Name In use: False
            - Name Not in use: True'''
            cList = self.handler.knownUsers # Check List
            for user in cList:
                if user[0] == name:
                    return False
            return True

        def checkIDInUse(self, id):
            '''Check argument (id) against know users.
            Args:
            - id(str): (id) to check
            Returns: 
            - ID In use: False
            - ID Not in use: True'''
            cList = self.handler.permissions # Check List
            for user in cList:
                if user[1] == id:
                    return False
            return True
        
        def create(self, name, passw, permission, id):
            '''Create a user. Requires admin permissions to create a user, unless no users exist. After the first user is created, only the admins can modify users.
            
            Args:
            - name(str): Username
            - passw(str): Password
            - permission(str): Permission
            - id(str): Refference ID, Must be unique to the account, cannot be used more than once. Checks are done.'''
            # Will use db_Handler to store user data
            # Encryption will be managed by db_Handler.Encryption.en()
            # Check Arguments
            exCall = '\n\nCall Function: --> Users.create()\n'  # Exception Call
            strList = ['name', 'passw', 'id', 'permission']
            for item in strList:
                if not type(locals()[item]) == str:
                    raise Exception(exCall + 'Invalid Argument Type({}), must be string.'.format(str(item)))
            # Verify permission is allowed
            if not self.permissionsAllowed(permission):
                raise PermissionError('Argument: (Permission) Invalid Permission')
            # Verify Password Is allowed
            if not self.handler.encryption.VerifyPassword(input = passw):
                raise ValueError("Argument: (Password) contains invalid characters.")
            # Verify ID selected is not in use
            if not self.checkIDInUse(id):
                raise Exception("Argument: (id) Already in use by another user")
            # Verify Name selected is not in use
            if not self.checkNameInUse(name):
                raise Exception('Argument: (Name): Already in use')
            # Check if permissions are required for user creation.
            # Start with checking current user logged:
            checkPass = False
            # If no users are created yet, and no user is logged in, bypass verifacation.
            if self.handler.knownUsers == [] and self.handler.permissions == []:
                if self.handler.userLogged == []:
                    checkPass = True
            else:
                if self.handler.userLogged == []:
                    # A user logged in, and with admin permissions is required for creation, so throw Exception.
                    raise Exception('A user needs to be signed in with a admin role to create a user.')
                
                if self.handler.userLogged != []:
                    # If User is logged in, verify name, permission, and check to see if that account actually exists, or has it been malicisouly modified.
                    if self.verifyUserLoggedExists() == True:
                        if self.handler.userLogged[1] == 'admin':
                            checkPass = True # Allow Modifacations.
            if checkPass == True:
                self.handler.knownUsers.append([name, passw])
                self.handler.permissions.append([permission, id])

        def remove(self, name):
            '''Remove a user'''
            pass

    class Encryption:
        def __init__(self, handler):
            self.hanlder = handler

        def VerifyPassword(self, input):
            '''Verify a password is valid and doesn\'t contain anyn characters that are not allowed.
            
            Args:
            - input(str): The password to verify

            Retuns:
            - True: Password Meets Requirments
            - False: Password is invalid'''
            allowed_chars = "abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # Excluded confusing characters
            if any(char not in allowed_chars for char in input):
                return False
            return True
        
        def uniqueIDGen(self, inputLength=5, maxKeyLength=50, luckyNumber=None, password=None, consistantOutput=False):
            '''Creates a random Key for encryption. The longer the key, the stronger the encryption. 
            \n The design behind this generator is to create a key that is random, but also a nuicance to decrypt.
            \n
            \nArgs:
            \n- inputLength(int): The length of the input, used in deciding the key (Not Necessary at this point in time.)
            \n-  -  Ensure count starts from 0, as it's indexes are needed for indices.
            \n-  -  Ex: If Input is 'Password', then the Length is 7. Not 8. If we start from 0.
            \n- maxKeyLength(int): How long the random key is allowed to be. 
            \n-  -  The key generated will be a random length from maxKeyLength/2 to max_Key_length
            \n-  -  Max for this var is: 10,000.
            \n- luckyNumber(int): A number you think is lucky. Some random number. Similar to password, but only numbers.
            \n- password(str): In progress.. Using a character password, a unique number is created and used in place of luckyNumber. The number is unique to character location whithin a string, what character is where, etc...
            \n- consistantOutput(bool): Disables the uniqueness used by time.time(), creating a consisting output

            \n
            \n Use Example:
            \n - .uniqueIDGen(inputLength=5, maxKeyLength=100)
            \nReturn(s):
            \n- uniqueID(int)
            \n
            \nNotes:
            \n1) No 2 chars next to eachother will be the same.
            '''
            # Check arguments:
            if luckyNumber == None and password == None:
                luckyNumber = random.randint(1, 50)
            if maxKeyLength > 10000:
                raise Exception('\n\nCall Function: --> Encryption.uniqueIDGen()\nMax Key Length is too large. Max is 10000')
            exCall = '\n\nCall Function: --> Encryption.uniqueIDGen()\n'  # Exception Call
            intList = ['inputLength', 'maxKeyLength']  # Removed luckyNumber from intList
            for item in intList:
                if not isinstance(locals()[item], int):
                    raise Exception(exCall + 'Invalid Argument Type({}), must be int.'.format(str(item)))

            # Validate and process password
            if password:
                if not self.VerifyPassword(password):
                    raise ValueError("password contains invalid characters.")
                # Use hashing to generate a unique number from password
                hash_object = hashlib.sha256(password.encode()) 
                experimental_number = int(hash_object.hexdigest(), 16)
                random.seed(experimental_number)
                luckyNumber = experimental_number
            else:
                random.seed(luckyNumber)

            mxSize = random.randint(maxKeyLength // 2, maxKeyLength)
            if not consistantOutput:
                random.seed(time.time())
            else:
                random.seed(0)
            keyOut = ' '
            for gen in range(mxSize):
                while True:
                    new_key = str(random.randint(0, inputLength))
                    if keyOut[-1] == new_key:
                        continue
                    else:
                        break
                keyOut += new_key
                random.seed(random.randint(0, gen))
                if not consistantOutput:
                    b1 = int(random.randint(1, int(time.time())))
                else:
                    b1 = int(random.randint(0, luckyNumber))
                b2 = int(random.randint(0, luckyNumber))
                random.seed((int(b1) + int(b2)))
                b3 = random.randint(0, 100)
                b4 = random.randint(0, 3)
                if not consistantOutput:
                    if b4 == 0:
                        random.seed(time.time() * b3)
                    elif b4 == 1:
                        random.seed(time.time() + b3)
                    else:
                        random.seed(time.time() - b3)
            
            return keyOut[0:maxKeyLength-1] # Verify the length of the key is correct
        
        def en(self, input, uniqueID, r=False, acc4decrywithIOverflow=False, debug=False, InvertedCount=False, maxLength=9, decrypt=False):
            '''Using an inputed string and unique number, we can scatter the actual input
            
            Args:
            - input(str): Input to be encrypted
            - uniqueID: Random Numbers, but any indiviual number cannot be greater than the length of input -1
            -     - Ex: input = 'Password', thus making it 8 chars longs. So we can not use any number greater than 7.
                  - The length of uniqueID can be any length, but the numbers within it cannot be greater than the length of input -1
                        This is due to a limitation of the method used to encrypt the data.
            - r: Reverse the position of placed chars: True/False
            - acc4decrywithIOverflow or Account for decrypt with (I) overflow, if input is gone through more than once.
                    Or if len(input) is less than < len(str(uniqueID)). Used for decryption only.
            - InvertedCount: Normal I Usage: 0.1.2.3.0... Inverted 3.2.1.0.3...
            - maxLength: How long each bit can be. Max 10, Min 2.
            - decrypt: If the Input, has already been encrypted, and you want to decrypt it. Set to True.
                    
            Use Example:
            - encrypting: en('Hello', 1234)
            - decrypting: en('Hello', 1234, decrypt=True)
            All other settings are optional and are designed for more advanced usage.

            Returns:
            - Encrypted output
            '''
            try:
                uniqueID = int(uniqueID)
            except:
                raise Exception('\n\nCall Function: --> Encryption.en()\n - uniqueID must be an integer.')
            splitInput = [input[i:i+maxLength] for i in range(0, len(input), maxLength)]
            output = ''
            for chunk in splitInput:
                tmpList = list(chunk)
                uniqueIDStr = str(uniqueID)
                if InvertedCount:
                    uniqueIDStr = uniqueIDStr[::-1]
                swapOperations = []
                for i, char in enumerate(tmpList):
                    if acc4decrywithIOverflow:
                        i = i % len(uniqueIDStr)
                    if i < len(uniqueIDStr):
                        swapIndex = int(uniqueIDStr[i]) % len(tmpList)
                        swapOperations.append((i, swapIndex))
                
                # If decrypt is True, reverse the swap operations
                if decrypt:
                    swapOperations.reverse()
                
                # Index Swapping
                for i, swapIndex in swapOperations:
                    if r:
                        tmpList[i], tmpList[swapIndex] = tmpList[i], tmpList[swapIndex]
                    else:
                        tmpList[i], tmpList[swapIndex] = tmpList[swapIndex], tmpList[i]
                    if debug:
                        print(f'Swapping {tmpList[i]} with {tmpList[swapIndex]} at indices {i} and {swapIndex}')
                output += ''.join(tmpList)
            return output

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
        '''This class is relativily pointless. This contains the random equations my stoned a$$ comes up with after I smoked a doobie.'''
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
        
        def clearBackups(self, tag, exemptOne=False, afterCreateBackup=False):
            '''Clears all backups for the database.
            
            Args:
            - tag(str): The tag of the database to remove all backups for.
            - exemptyOne(Bool): Remove all but the latest backup.
            - afterCreateBackup(bool): After removals, create a brand new backup.'''
            pass
        
        def compressBackups(self):
            '''Compresses all backups for the database into a zip file. Zips will be located in a folder called (zippedBackups)
            Ex of filename: db_AAAA-1-11-24.zip'''
            pass
            
    class Save:
        def __init__(self, handler):
            self.handler = handler

        def all(self):
            '''Saves the entire db instance. This includes all data, columns, and meta data.'''
            global lastDatabaseSaved
            # You can save a database even if it's empty. Allows for an easy setup of hundreds of databases.
            # Vars saved: tag, columnStorage, listStorage, owner, knownUsers, permissions, userLogged, allowedPermissions, userPW

            # Make the name for our save file
            saveNm='db_'+str(self.handler.tag[0])+'.txt'

            # Check if file exists
            if os.path.exists('db_'+str(self.handler.tag[0])+'.txt'):
                # Check if folder exists
                if not os.path.exists('Backups'):
                    os.mkdir('db_'+str(self.handler.tag[0])+'_Backups')
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
                f.write()
                f.close()

            # All done!
            lastDatabaseSaved = saveNm
            print('Database saved as:', saveNm)

        def VariabledSave(self):
            '''Used periodically to save important variables for stable runtime of handler.'''
            global usedCountList, lastDatabaseSaved
            # Check if file exists, set as backup
            if os.path.exists('variableSave.py'):
                os.rename('variableSave.py', 'variableSaveBackup.py')

            # Overwrite file, or open new one and write data
            file = open('variableSave.py', 'w+')
            file.write('usedCountList = {}'.format(usedCountList))
            file.write('\nlastDatabaseSaved = {}'.format(lastDatabaseSaved))
            file.write('\nmALCount = {}'.format(mALCount))
            file.close()

    def load(self, tag=None, excuse=[]):
        '''Loads data from a saved database. Requires this database instance to be empty.
        
        Args:
        tag: The tag of the database to load. If None, it will load last saved database.
        excuse: A list of variables to excuse from being loaded. Empty = Load all.
        
        Excusable Variables:
        - columnStorage
        - listStorage
        - tag (Only call if you know what your doing)'''

        # Check excusable variables
        allowedExcuses = ['columnStorage', 'listStorage', 'tag']
        for i in range(len(excuse)):
            if excuse[i] not in allowedExcuses:
                raise Exception('\n\nCall Function: --> db_Handler.load()\nInvalid excuse given. Excuse must be in the list of allowed excuses.')
        
        if tag != None:
            # Set the tag to the one given
            self.tag[0] = tag
        elif tag == None and lastDatabaseSaved != None:
            # Set the tag to the last saved database
            self.tag[0] = lastDatabaseSaved
        else:
            raise Exception('\n\nCall Function: --> db_Handler.load()\nNo tag given, and no database has been saved yet. Unable to automatically determine what to load.')
        
        if self.columnStorage != [] or self.listStorage != []:
            raise Exception('\n\nCall Function: --> db_Handler.load()\nData already exists in this database. Cannot load data into an existing database.')
        else:
            # Check if columnStorage and listStorage are empty
            if self.columnStorage == [] and self.listStorage == []:
                # Make the name for our save file
                saveNm='db_'+str(self.tag[0])+'.txt'
                # Check if file exists
                if os.path.exists(saveNm):
                    # Load the database
                    with open(saveNm, 'r') as f:
                        for line in f:
                            # Get the value of the line
                            value = line.split(' = ')[1]
                            # Remove the '\n' at the end
                            value = value.replace('\n', '')
                            # Get the name of the line
                            name = line.split(' = ')[0]
                            # Remove the spaces at the end
                            name = name.replace(' ', '')
                            # Set the value to the database

                            # Verify excuses before setting values
                            if 'tag' not in allowedExcuses:
                                if name == 'tag':
                                    self.tag[0] = value
                            if 'columnStorage' not in allowedExcuses:
                                if name == 'columnStorage':
                                    self.columnStorage = eval(value)
                            if 'listStorage' not in allowedExcuses:
                                if name == 'listStorage':
                                    self.listStorage = eval(value)

                    print('Database loaded:', saveNm)
                else:
                    raise Exception('\n\nCall Function: --> db_Handler.load()\nDatabase save file does not exist.')
            
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
# |            Also designed to just look nice. :)                |
# -----------------------------------------------------------------
