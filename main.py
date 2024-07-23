# Ideas for settings:
# max_allowsRows - A db can only have ? rows within it.
# max_allowColumns - a db can only have ? columns within it.
# CaseSensativityAmoungColumnNames=True
bypassPasswordValidation = False # Default False
CaseSensativityAmoungColumnNames = [True] # Default True, if False, then 'Names' and 'names' are the same.
'''Case Sensativity active? 'Names' and 'names' are the same if True. If False, then they are seen as different.'''
userPw_ChangesEachSave = True # Default True
decryptSaveOnLoad = False # Default False
EncryptionKey='userPW'
LoginKey = 'Taco'
EncryptSaveFile = False
loadDBOnEachStartup = 'SERV' # Database tag. If == '', will ignore. Default ''

# Debug Settings:
showArgsOnFunctionCall = False # Default False
# Show Working Working Path
showWorkingPath = False # Default False
'''Create the instance, and you're ready to go! No need to call the load or create functions. They are automatically called. Only works for first instance creation.'''

#Grouped Files
# 1) handler_showcase.py


# -------------------------------------------------------------- #
#                                                                #
#                   Created by Brandon R.                        #
#               Supported and backed by Dakota H.                #
#                                                                #
# -------------------------------------------------------------- #
import os, sys, shutil, random, time, hashlib, builtins, datetime, zipfile, uuid
sys.set_int_max_str_digits(1000000) # Set the max digits for integers to 1,000,000
if showWorkingPath:
    print('Current Path Set:', os.getcwd())
#os.chdir('App')
print('Current Version: 0.1.3')
print(f"Python Version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}.{sys.version_info.releaselevel}")




# Temp data (Moving to save file when that has been made/developed)
incrimatationCount='AAAA' 
'''1 letter, then 3 numbers or letters.'''
# Variabled save file additions
usedCountList = []
lastDatabaseSaved = None
mALCount = 0 # Malicios Activity Logger Count
databasesLoaded = []

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
    '''An extremely simple, but yet thought out handler. :)-'''
    def __init__(self) -> None:
        # Active Status, 
        self.info = [True]
        # Global Temp Var Identifier
        self.tag = [str(generateNextIncrement())] # Makes self tag unique for each database, temp vars don't colide this way.
        '''Ensure tag is being pulled with tag[0]. You forget to do this alot.'''

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
        self.authentication = self.Authentication(self)
        self.backup = self.Backup(self)

        if loadDBOnEachStartup != '':
            self.tag = [loadDBOnEachStartup]
            self.load(loadDBOnEachStartup)
            self.mkGlobalTempVars()
    
    def assignTemp(self, value):
        var = ('TempVar'+str(self.tag[0]))
        globals()[var] = value
    def returnTemp(self):
        var = ('TempVar'+str(self.tag[0]))
        return globals()[var]
    def mkGlobalTempVars(self):
        newVar = ('TempVar'+str(self.tag[0]))
        globals()[newVar] = None
    def create(self, tag=None):
        '''Used to setup a database. Required if user accounts will be used.
        \nArgs:
        \n - tag(str): The tag of the database. If not set, a random tag will be generated.'''
        self.mkGlobalTempVars()
        if tag != None:
            self.tag = tag
        self.userPW = self.encryption.uniqueIDGen(maxKeyLength=50, password='EncryptionKey', consistantOutput=False)
    def makeRowTmpFile(self):
        '''Creates a temporary file for rows.'''
        globals()['TempRowFile'+str(self.tag[0])] = open('TempRowFile'+str(self.tag[0])+'.txt', 'w')
    
    class MaliciosActivityLogger:
        '''This class is only used/called when data between variables doesn't match and may be a sign of malicios activity.
        This class logs all calls to itself and will take precautions if malicios data is found depending from where it occured.'''
        def __init__(self, handler):
            self.handler = handler

        def report(self, type, data):
            '''Report malicios activity. This function may be called by mistake if code is improperly maintainted or if a bug occurs.
            
            Malicous Types: Set type as one of the following in string format. Case sensative. Next is the level of danger.
            - (Data Mismatch): Data between variables doesn't match or is invalid. (2/10)
            - (LoggedInUserDoesNotExist): User logged in does not exist within known users. (10/10)
            - (Failed Authentication): Failed to authenticate user. (5/10)
            - 
            '''
            knownType = ['Data Mismatch', 
                         'LoggedInUserDoesNotExist', 
                         'Failed Authentication']
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
            file.write(str(('Type:',type,'Time:',time.time(),'Date:',time.strftime('%Y-%m-%d %H:%M:%S'),'\nData:',data,'\n\n')))
            file.close()
    
    class Authentication:
        '''User authentication class. Credential Check, Signin, Signout'''
        def __init__(self, handler):
            self.handler = handler
        
        def signin(self, user, passw):
            '''Login to an existing account!'''
            if self.handler.userLogged == []:
                if self.checkCreds(user, passw):
                    out1 = self.handler.users.returnUserPerm(user)
                    if out1 == False:
                        raise Exception('Unable to retrieve permissions for user.')
                    out2 = self.handler.users.returnUserId(user)
                    if out2 == False:
                        raise Exception('Unable to retrieve id for user.')
                    self.handler.userLogged = [user, out1, out2]
                    print('Authentication Success...')
                    return
                else:
                    self.handler.maliciosActivityLogger.report(type='Failed Authentication', data=[user, passw])
                    return
            else:
                raise Exception('A user is already logged in. Cannot login more than 1 user at a time.')
            
        def signout(self):
            '''Sign out of your logged in account!'''
            # Reset var
            self.handler.userLogged = []
            
        def checkCreds(self, user, passw):
            '''Verifys creds are correct.'''
            for userS in self.handler.knownUsers:
                if userS[0] == user:
                    if userS[1] == passw:
                        return True
            # Return False if creds are not found.
            return False

    class Users:
        '''User management class. This class is used to manage users within the database.
        \n - Allows you to do the following:
        \n - disable/enable users
        \n - Create/Remove users
        \n - Enable/Disable writing and/or reading of particular columns in the database
        \n - Enable/Disable writing and/or reading of particular rows in the database
        \n\nlist of functions:
        \n - returnUserPerm(name) # Permission of user
        \n - returnUserId(name) # ID of user
        \n - permissionsAllowed(perm) # Check if permission is allowed, checks against allowedPermissions
        \n - verifyUserLoggedExists() # Check if user logged in exists within known users
        \n - checkNameInUse(name) # Check if name is in use
        \n - checkIDInUse(id) # Check if id is in use
        \n - create(name, passw, permission, id) # Create a user
        \n - remove(name) # Remove a user
        \n\nFunctions to be implemented:
        \n - disableUser(name) # Disable a user
        \n - enableUser(name) # Enable a user
        \n - disableColumn(column, name) # Disable writing to a column
        \n - enableColumn(column, name) # Enable writing to a column


        '''
        def __init__(self, handler):
            self.handler = handler
        
        def returnUserPerm(self, name):
            '''Returns the permission of a given user. Returns False if nothing found.'''
            for x in range(len(self.handler.knownUsers)):
                if self.handler.knownUsers[x][0] == name:
                    return self.handler.permissions[x][0]
            return False

        def returnUserId(self, name):
            '''Returns the id of a given user. Returns Fase if nothing found.'''
            for x in range(len(self.handler.knownUsers)):
                if self.handler.knownUsers[x][0] == name:
                    return self.handler.permissions[x][1]
            return False
        
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
            nameF = False
            for user in self.handler.knownUsers:
                for perm in self.handler.permissions:
                    if user[0] == self.handler.userLogged[0]:
                        nameF = True
                        if perm[0] == self.handler.userLogged[1]:
                            print(perm[1], self.handler.userLogged[2])
                            if perm[1] == self.handler.userLogged[2]:
                                return True
                            
                        
            if nameF == False:
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
            # Verify new permission is allowed
            if not self.permissionsAllowed(permission):
                raise PermissionError('Argument: (Permission) Invalid Permission')
            # Verify new Password Is allowed
            if not self.handler.encryption.VerifyPassword(input = passw):
                raise ValueError("Argument: (Password) contains invalid characters.")
            # Verify new ID selected is not in use
            if not self.checkIDInUse(id):
                raise Exception("Argument: (id) Already in use by another user")
            # Verify new Name selected is not in use
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
                        else:
                            raise Exception('The user logged in, if logged in, does not have admin rights to run this action.')
            if checkPass == True:
                self.handler.knownUsers.append([name, passw])
                self.handler.permissions.append([permission, id])

        def remove(self, name):
            '''Remove a user. Requires admin permissions.
            Returns:
            - True: Removed User Successfuly
            - False: The user was not removed, and/or found.'''
            if self.handler.userLogged != []:
                if self.verifyUserLoggedExists() == True:
                    if self.handler.userLogged[1] == 'admin':
                        for x in range(len(self.handler.knownUsers)):
                            if self.handler.knownUsers[x][0] == name:
                                self.handler.knownUsers[x].pop()
                                self.handler.permissions[x].pop()
                                # If userLogged in remvoed themselves. Remove them from being logged in.
                                if self.handler.userLogged[0] == name:
                                    self.handler.userLogged = []
                    else:
                        raise Exception('The user logged in, if logged in, does not have admin rights to run this action.')
                else:
                    raise Exception('Invalid Data within userLogged')
            else:
                raise Exception('No user is currently signed in. Admin permissions are required for this action.')

        def disableUser(self, name):
            '''Disable a user. Requires admin permissions.'''   
            pass
            
        def enableUser(self, name):
            '''Enable a user. Requires admin permissions.'''
            pass
        
        def disableColumn(self, column, name):
            '''Disable writing to a column. Requires admin permissions.'''
            pass
        
        def enableColumn(self, column, name):
            '''Enable writing to a column if disabled. Requires admin permissions.'''
            pass
    
    class Encryption:
        '''Encryption class. Used for encrypting and decrypting data.
        
        Settings Implemented:
        - showArgsOnFunctionCall'''
        def __init__(self, handler):
            self.handler = handler

        def VerifyPassword(self, input):
            '''Verify a password is valid and doesn\'t contain anyn characters that are not allowed.
            
            Args:
            - input(str): The password to verify

            Retuns:
            - True: Password Meets Requirments
            - False: Password is invalid'''
            global bypassPasswordValidation
            if not bypassPasswordValidation:
                allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"  # Excluded confusing characters
                if any(char not in allowed_chars for char in str(input)):
                    return False
                return True
            return True
        
        def uniqueIDGen(self, inputLength=5, maxKeyLength=200, luckyNumber=None, password=None, consistantOutput=False):
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
            \n   -  If using EncryptionKey Variable, set password 'EncryptionKey' to use the key, or set password as globals()['EncryptionKey']
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
            global showArgsOnFunctionCall
            # Check settings:
            if showArgsOnFunctionCall:
                print('\n\nCall Function: --> Encryption.uniqueIDGen()\n - inputLength:', inputLength, '\n - maxKeyLength:', maxKeyLength, '\n - luckyNumber:', luckyNumber)
            # Check arguments:
            if password == 'EncryptionKey':
                password = globals()['EncryptionKey']
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
                # Verify password is valid
                if not self.VerifyPassword(password):
                    raise ValueError("password contains invalid characters.")
                # Use hashing to generate a unique number from password
                hash_object = hashlib.sha256(password.encode()) 
                # Convert the hash to an integer
                experimental_number = int(hash_object.hexdigest(), 16)
                # Random the seed
                random.seed(experimental_number)
                luckyNumber = experimental_number
            else:
                random.seed(luckyNumber)
            # Randomize how long the key will be
            mxSize = random.randint(maxKeyLength // 2, maxKeyLength)
            # Add inconsistency to the key
            if not consistantOutput:
                random.seed(time.time())
            else:
                random.seed(0)
            keyOut = ' ' # Space is removed before returning the key
            # Generate the key
            for gen in range(mxSize):
                while True:
                    # Select next number for the key
                    if not consistantOutput:
                        # Generate 15 random numbers into a list:
                        rList = []
                        for i in range(15):
                            rList.append(random.randint(0, 9))
                        # Add all the numbers together
                        new_key = 0
                        for num in rList:
                            new_key += num
                        # Divide the sum by the length of the list
                        new_key = new_key // len(rList)
                        # Multiple by maxKeyLength
                        new_key = str(new_key * maxKeyLength)
                        # Select the a random digit
                        new_key = int(new_key[random.randint(0, len(new_key)-1)])
                        random.seed(new_key)
                        new_key = random.randint(0, luckyNumber)
                    else:
                        new_key = random.randint(0, luckyNumber)
                    # Ensure no 2 chars next to eachother are the same
                    if keyOut[-1] == new_key:
                        continue
                    else:
                        break
                # Add the new char to the key
                keyOut += str(new_key)
                # Seed the random number generator with a random number
                random.seed(random.randint(0, gen))
                if not consistantOutput:
                    # Get the uuid of the current time string
                    uuid_str = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(time.time())))
                    # Give each char in uuid a unique number and save each number to a list.
                    uuid_list = []
                    for char in uuid_str:
                        uuid_list.append(str(ord(char)))
                    # Randomize the list
                    random.shuffle(uuid_list)
                    # Create a random value. Then run through the list and alternate between adding, subtracting, and multiplying the value by the list value.
                    random_value = random.randint(0, 100)
                    for value in uuid_list:
                        random_value += int(value)
                        random_value -= int(value)
                        random_value *= int(value)
                    # Seed the random value
                    random.seed(random_value)
                    # Generate a new random value
                    random_value = random.randint(0, 100)

                # Add more inconsistency to the key
                if not consistantOutput:
                    b1 = int(random.randint(1, int(time.time())))
                else:
                    b1 = int(random.randint(0, luckyNumber))
                # More math
                b2 = int(random.randint(0, luckyNumber))
                # Even more math
                random.seed((int(b1) + int(b2)))
                b3 = random.randint(0, 100)
                b4 = random.randint(0, 3)
                # Add even more inconsistency
                try:
                    with open('/dev/hwrng', 'rb') as f:
                        # Read 4 bytes from hardware RNG
                        hw_seed = f.read(4)
                        # Convert bytes to an integer
                        seed = int.from_bytes(hw_seed, 'big')
                        random.seed(seed)
                except:
                    if not consistantOutput:
                        if b4 == 0:
                            random.seed(time.time() * b3)
                        elif b4 == 1:
                            random.seed(time.time() + b3)
                        else:
                            random.seed(time.time() - b3)
            # Return the key
            return keyOut[1:maxKeyLength-1] # Verify the length of the key is correct
        
        def getNewLineIndicators(self, input):
            '''Gets the indexs of new line indicators within a string. Used for encryption and decryption.
            
            Returns:
            - modified_input: The input with new line indicators removed
            - newline_indexes: The indexes of the new line indicators within the input string'''
            global showArgsOnFunctionCall
            # Check settings
            if showArgsOnFunctionCall:
                print('\n\nCall Function: --> Encryption.getNewLineIndicators()\n - input:', input)
            # Get indexs of new lines indicators
            newline_indexes = [i for i, char in enumerate(input) if char == '\n']
            # Remove indicators
            input = str(input)
            modified_input = input.replace('\n', '')
            return modified_input, newline_indexes

        def reInsertNewLineIndicators(self, input, newline_indexes):
            '''Reinserts new line indicators into a string.'''
            for index in reversed(newline_indexes):
                input = input[:index] + '\n' + input[index:]
            return input

        def bullshitEncrypt(self, input, uniqueID, strength=168):
            '''Does really confusing stuff. This is called bullshit encryption. Once bullshitted, it's hard to un-bullshit without the 'bullshitDecrypt' function. Requires the encryption and decryption to occur on the same device. As device specific data is used to encrypt the data.'''
            # Check settings
            global bypassPasswordValidation, showArgsOnFunctionCall
            if showArgsOnFunctionCall:
                print('\n\nCall Function: --> Encryption.bullshitEncrypt()\n - input:', input, '\n - uniqueID:', uniqueID, '\n - strength:', strength)
            import platform
            networkName = platform.node()
            wasEnabled=False
            if bypassPasswordValidation:
                wasEnabled = True
            bypassPasswordValidation = True # Bypass password validation, since networkName may contain invalid characters.
            # Create id with networkName
            networkName = db_Handler.Encryption.uniqueIDGen(self, maxKeyLength=strength, password=str(uniqueID)+networkName, consistantOutput=True)
            # Encrypt
            input = db_Handler.Encryption.en(self, input=input, uniqueID=networkName, decrypt=False)
            # Generate ConsistantKey with uniqueID
            uniqueIDNew = db_Handler.Encryption.uniqueIDGen(self, maxKeyLength=strength, password=str(uniqueID), consistantOutput=True)
            # Encrypt
            input = db_Handler.Encryption.en(self, input=input, uniqueID=uniqueIDNew, decrypt=False)
            # Encrypt Again, but with original uniqueID
            input = db_Handler.Encryption.en(self, input=input, uniqueID=uniqueID, decrypt=False)
            if not wasEnabled:
                bypassPasswordValidation = False # Reset back to False
            return input
        
        def bullshitDecrypt(self, input, uniqueID, strength=168):
            '''Use me to un-bullshit the bullshit. I'm the un-bullshitter.'''
            global bypassPasswordValidation, showArgsOnFunctionCall
            # Check settings
            if showArgsOnFunctionCall:
                print('\n\nCall Function: --> Encryption.bullshitDecrypt()\n - input:', input, '\n - uniqueID:', uniqueID, '\n - strength:', strength)
            wasEnabled=False
            if bypassPasswordValidation:
                wasEnabled = True
            bypassPasswordValidation = True # Bypass password validation, since networkName may contain invalid characters.
            import platform
            networkName = platform.node()

            # Generate ConsistantKey with uniqueID
            uniqueIDNew = db_Handler.Encryption.uniqueIDGen(self, maxKeyLength=strength, password=str(uniqueID), consistantOutput=True)
            # Decrypt, but with original uniqueID
            input = db_Handler.Encryption.en(self, input=input, uniqueID=uniqueID, decrypt=True)
            # Decrypt again, but with new uniqueID
            input = db_Handler.Encryption.en(self, input=input, uniqueID = uniqueIDNew, decrypt=True)
            # Create id with networkName
            networkName = db_Handler.Encryption.uniqueIDGen(self, maxKeyLength=strength, password=str(uniqueID)+networkName, consistantOutput=True)
            # Decrypt
            input = db_Handler.Encryption.en(self, input=input, uniqueID=networkName, decrypt=True)
            if not wasEnabled:
                bypassPasswordValidation = False # Reset back to False
            return input
        
        def en(self, input, uniqueID, r=False, acc4decrywithIOverflow=False, debug=False, InvertedCount=False, maxLength=100, decrypt=False, shuffletmpList=False):
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
            - shuffletmpList: Randomize the list using the uniqueID. DO NOT USE AT ALL. IT'S NO WORK.
                    
            Use Example:
            - encrypting: en('Hello', 1234)
            - decrypting: en('Hello', 1234, decrypt=True)
            All other settings are optional and are designed for more advanced usage.

            Returns:
            - Encrypted output
            '''
            global showArgsOnFunctionCall
            # Check settings
            if showArgsOnFunctionCall:
                print('\n\nCall Function: --> Encryption.en()\n - input:', input, '\n - uniqueID:', uniqueID, '\n - r:', r, '\n - acc4decrywithIOverflow:', acc4decrywithIOverflow, '\n - debug:', debug, '\n - InvertedCount:', InvertedCount, '\n - maxLength:', maxLength, '\n - decrypt:', decrypt, '\n - shuffletmpList:', shuffletmpList)
            try:
                uniqueID = int(uniqueID)
            except:
                raise Exception('\n\nCall Function: --> Encryption.en()\n - uniqueID must be an integer.')
            modified_input, newline_indexes = self.getNewLineIndicators(input)
            splitInput = [modified_input[i:i+maxLength] for i in range(0, len(modified_input), maxLength)]
            output = ''
            for chunk in splitInput:
                
                # Remove \n in chunk, but remember where it was located, so we can add it back in after chunk is encrypted/decrypted
                newLineIndex = None
                if '\n' in chunk:
                    chunk = chunk.replace('\n', '')
                    newLineIndex = chunk.index('\n')
                # Convert chunk to list
                tmpList = list(chunk)
                uniqueIDStr = str(uniqueID)
                # Reverse uniqueIDStr
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
                
                if shuffletmpList:
                    # randomize the list using the uniqueID.
                    # Shuffle List
                    if not decrypt:
                        random.seed(uniqueID)
                        random.shuffle(tmpList)
                    # Unshuffle List
                    if decrypt:
                        random.seed(uniqueID)
                        # Generate the same sequence of shuffle operations
                        shuffle_operations = list(range(len(tmpList)))
                        random.shuffle(shuffle_operations)
                        
                        # Reverse the shuffle operations
                        unshuffled_list = [None] * len(tmpList)
                        for original_index, shuffled_index in enumerate(shuffle_operations):
                            unshuffled_list[shuffled_index] = tmpList[original_index]
                        tmpList = unshuffled_list
                
                # Add \n back in
                if newLineIndex is not None:
                    tmpList.insert(newLineIndex, '\n')
                output += ''.join(tmpList)
            new_output = self.reInsertNewLineIndicators(output, newline_indexes)
            return new_output

    class Edit:
        '''Edit class. Used for editing the database. Adding, removing, and modifying data.'''
        def __init__(self, handler):
            self.handler = handler
        
        def addColumn(self, column, value=None, AutoFillEmptyRows=True):
            '''Add a new column to the database!
            
            Args:
            - Column(str): The name of the column, or a list of columns!
                # Will check if any column name in list exists before adding. Will not add any if any match is found.
            - Value(str/None): The value to fill the empty rows with for the new column. (Default is None)

            Settings:
            - AutoFillEmptyRows: True/False
            
            Notes:
            All rows for this column will be empty. Use mods.EmptyEntryFill() to fill empty values in rows.'''
            global CaseSensativityAmoungColumnNames
            if type(column) == list:
                for c in column:
                    if CaseSensativityAmoungColumnNames:
                        if c.lower() in [x.lower() for x in self.handler.columnStorage]:
                            raise Exception('\n\nCall Function: --> db_Handler.Edit.addColumn()\nColumn already exists.')
                    else:
                        if c in self.handler.columnStorage:
                            raise Exception('\n\nCall Function: --> db_Handler.Edit.addColumn()\nColumn already exists.')
                    self.handler.columnStorage.append(c)
                    if AutoFillEmptyRows:
                        self.handler.mods.EmptyEntryFill(column=c, value=value, doesIndexForColumnExist=True)
            if type(column) == str:
                # Check if column exists:
                for c in self.handler.columnStorage:
                    if CaseSensativityAmoungColumnNames:
                        if c.lower() == column.lower():
                            raise Exception('\n\nCall Function: --> db_Handler.Edit.addColumn()\nColumn already exists.')
                    else:
                        if c == column:
                            raise Exception('\n\nCall Function: --> db_Handler.Edit.addColumn()\nColumn already exists.')
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
        
        def addRow(self, row, quickSave=True):
            '''Add a new row to the database! Give me a list of data to add. The list cannot be longer or shorter than the column count.
            
            Args:
            - Row(list): The data to add to the row. Must be a list.
            - quickSave(bool): Add rows to tempFile. (Only Use If Speed Is A Requirment)'''
            if len(row) == len(self.handler.columnStorage):
                if type(row) == list:
                    if quickSave:
                        try:
                            globals()['TempRowFile'+str(self.handler.tag[0])].write(str(row)+'\n')
                        except:
                            # Make file then write
                            globals()['TempRowFile'+str(self.handler.tag[0])] = open('TempRowFile'+str(self.handler.tag[0]), 'w')
                            globals()['TempRowFile'+str(self.handler.tag[0])].write(str(row)+'\n')
                    self.handler.listStorage.append(row)
                    return
                else:
                    raise Exception('\n\nCall Function: --> db_Handler.Edit.addRow()\nRow must be a list. Please and thank you.')
            else:
                raise Exception('\n\nCall Function: --> db_Handler.Edit.addRow()\nRow length must be the same as the column length.')
    
    class Mods:
        '''Things I personally would love to have built into a handler. But done simply! None of that complicated shit. Functions in here are soley ideas.'''
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
                    
        def setPermForColumn(self):
            '''Set permissions for a column. Allows you to set permissions for a column, and who can read/write to it.'''
            pass

        def encryptRow(self, row, uniqueID):
            '''Encrypt a row. Password for encryption is stored within the saveFile for the database.
            
            Args:
            - row: The row to encrypt
            - uniqueID: The uniqueID to encrypt the row with
            
            Returns:
            - Encrypted Row'''
            pass
    
    class Data:
        '''Data class. Used for managing data within the database. Displaying, finding, and returning data.'''
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
            
    def space(self, var=None, max_length=10, hide=False, return_ShortenNotice=False, centerText=False):
        '''Reused from my old handler. Why change something that works? :)- Did make a few changes to it tho. :laugh:discord:id:9620981493924'''
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
        
        def tireRotationsMpH(speed_mph = 400, tire_diameter_inches = 25.5, feet_per_mile = 5280, minutes_per_hour = 60):
            '''Calculate tire rotations per minute based on tire diameter and speed in miles per hour. Used to calculate RPM required from an electric motor to achieve a certain speed.'''
            import math

            # Calculations
            circumference_inches = math.pi * tire_diameter_inches
            circumference_feet = circumference_inches / 12  # Convert inches to feet
            speed_feet_per_minute = speed_mph * feet_per_mile / minutes_per_hour
            rpm = speed_feet_per_minute / circumference_feet

            print(f'A tire with a diameter of {tire_diameter_inches} inches will rotate {rpm:.2f} times per minute; or be the rpm motor requirements for an illegal moped, to travel at a speed of {speed_mph} mph.')
            return rpm
        class SpeedPerHourConversion:
            '''Convert all types of speeds to miles per hour. Ex: 100 km/h to mph
            list Of All Speeds:
            - km/h
            - m/s
            - ft/s
            - mph
            - knots
            - mach
            - speed of light
            - speed of sound
            - speed of a snail
            - speed of a cheetah
            Note: I did not include converting a speed to the same speed. That would be pointless. So don't think I forgot, duhhhh.
            '''
            class kilometerPerHour:
                def metersPerSecond(speed):
                    '''Converts km/h to m/s.'''
                    return speed / 3.6
                def feetPerSecond(speed):
                    '''Converts km/h to ft/s.'''
                    return speed / 1.09728
                def milesPerHour(speed):
                    '''Converts km/h to mph.'''
                    return speed / 1.60934
                def knots(speed):
                    '''Converts km/h to knots.'''
                    return speed / 1.852
                def mach(speed):
                    '''Converts km/h to mach.'''
                    return speed / 1234.8
                def speedOfLight(speed):
                    '''Converts km/h to the speed of light.'''
                    return speed / 1079252848.8
                def speedOfSound(speed):
                    '''Converts km/h to the speed of sound.'''
                    return speed / 1234.8
                def speedOfSnail(speed):
                    '''Converts km/h to the speed of a snail.'''
                    return speed / 0.000166667
                def speedOfCheetah(speed):
                    '''Converts km/h to the speed of a cheetah.'''
                    return speed / 109.728
            class metersPerSecond:
                def feetPerSecond(speed):
                    '''Converts m/s to ft/s.'''
                    return speed * 3.28084
                def metersPerSecond(speed):
                    # Already in meters per second
                    return speed
                def milesPerHour(speed):
                    '''Converts m/s to mph.'''
                    return speed * 2.23694
                def knots(speed):
                    '''Converts m/s to knots.'''
                    return speed * 1.94384
                def mach(speed):
                    '''Converts m/s to mach.'''
                    return speed / 343.592
                def speedOfLight(speed):
                    '''Converts m/s to the speed of light.'''
                    return speed / 299792458
                def speedOfSound(speed):
                    '''Converts m/s to the speed of sound.'''
                    return speed / 343.592
                def speedOfSnail(speed):
                    '''Converts m/s to the speed of a snail.'''
                    return speed * 0.000277778
                def speedOfCheetah(speed):
                    '''Converts m/s to the speed of a cheetah.'''
                    return speed * 2.23694
            class FeetPerSecond:
                def feet_to_kmh(value):
                    return value * 1.09728
                def feet_to_ms(value):
                    return value * 0.3048
                def feet_to_fts(value):
                    return value
                def feet_to_mph(value):
                    return value * 0.681818
                def feet_to_knots(value):
                    return value * 0.592484
                def feet_to_mach(value):
                    return value / 1125
                def feet_to_speed_of_light(value):
                    return value / 983571056
                def feet_to_speed_of_sound(value):
                    return value / 1125
                def feet_to_speed_of_snail(value):
                    return value / 0.013
                def feet_to_speed_of_cheetah(value):
                    return value / 88
            class MilesPerHour:
                def mph_to_kmh(value):
                    return value * 1.60934
                def mph_to_ms(value):
                    return value * 0.44704
                def mph_to_fts(value):
                    return value * 1.46667
                def mph_to_mph(value):
                    return value
                def mph_to_knots(value):
                    return value * 0.868976
                def mph_to_mach(value):
                    return value / 761.207
                def mph_to_speed_of_light(value):
                    return value / 670616629
                def mph_to_speed_of_sound(value):
                    return value / 761.207
                def mph_to_speed_of_snail(value):
                    return value / 0.001
                def mph_to_speed_of_cheetah(value):
                    return value / 70
            class Knots:
                def knots_to_kmh(value):
                    return value * 1.852
                def knots_to_ms(value):
                    return value * 0.514444
                def knots_to_fts(value):
                    return value * 1.68781
                def knots_to_mph(value):
                    return value * 1.15078
                def knots_to_knots(value):
                    return value
                def knots_to_mach(value):
                    return value / 661.470
                def knots_to_speed_of_light(value):
                    return value / 582749912
                def knots_to_speed_of_sound(value):
                    return value / 661.470
                def knots_to_speed_of_snail(value):
                    return value / 0.000911344
                def knots_to_speed_of_cheetah(value):
                    return value / 59.675
            class Mach:
                def mach_to_kmh(value):
                    return value * 1234.8
                def mach_to_ms(value):
                    return value * 343.592
                def mach_to_fts(value):
                    return value * 1125
                def mach_to_mph(value):
                    return value * 761.207
                def mach_to_knots(value):
                    return value * 661.470
                def mach_to_mach(value):
                    return value
                def mach_to_speed_of_light(value):
                    return value / 874030
                def mach_to_speed_of_sound(value):
                    return value
                def mach_to_speed_of_snail(value):
                    return value / 0.001364
                def mach_to_speed_of_cheetah(value):
                    return value / 114.5
            class SpeedOfLight:
                def speed_of_light_to_kmh(value):
                    return value * 1079252848.8
                def speed_of_light_to_ms(value):
                    return value * 299792458
                def speed_of_light_to_fts(value):
                    return value * 983571056
                def speed_of_light_to_mph(value):
                    return value * 670616629
                def speed_of_light_to_knots(value):
                    return value * 582749912
                def speed_of_light_to_mach(value):
                    return value * 874030
                def speed_of_light_to_speed_of_light(value):
                    return value
                def speed_of_light_to_speed_of_sound(value):
                    return value * 0.34029
                def speed_of_light_to_speed_of_snail(value):
                    return value / 299792458
                def speed_of_light_to_speed_of_cheetah(value):
                    return value / 249448.5
            class SpeedOfSound:
                def speed_of_sound_to_kmh(value):
                    return value * 1234.8
                def speed_of_sound_to_ms(value):
                    return value * 343.592
                def speed_of_sound_to_fts(value):
                    return value * 1125
                def speed_of_sound_to_mph(value):
                    return value * 761.207
                def speed_of_sound_to_knots(value):
                    return value * 661.470
                def speed_of_sound_to_mach(value):
                    return value
                def speed_of_sound_to_speed_of_light(value):
                    return value * 0.34029
                def speed_of_sound_to_speed_of_sound(value):
                    return value
                def speed_of_sound_to_speed_of_snail(value):
                    return value / 343.592
                def speed_of_sound_to_speed_of_cheetah(value):
                    return value / 28.8
            class SpeedOfSnail:
                def speed_of_snail_to_kmh(value):
                    return value * 0.000166667
                def speed_of_snail_to_ms(value):
                    return value * 0.0000462963
                def speed_of_snail_to_fts(value):
                    return value * 0.000152587
                def speed_of_snail_to_mph(value):
                    return value * 0.000104167
                def speed_of_snail_to_knots(value):
                    return value * 0.0000907895
                def speed_of_snail_to_mach(value):
                    return value * 0.001364
                def speed_of_snail_to_speed_of_light(value):
                    return value * 299792458
                def speed_of_snail_to_speed_of_sound(value):
                    return value * 343.592
                def speed_of_snail_to_speed_of_snail(value):
                    return value
                def speed_of_snail_to_speed_of_cheetah(value):
                    return value / 8400
            class SpeedOfCheetah:
                def speed_of_cheetah_to_kmh(value):
                    return value * 109.728
                def speed_of_cheetah_to_ms(value):
                    return value * 30.48
                def speed_of_cheetah_to_fts(value):
                    return value * 100
                def speed_of_cheetah_to_mph(value):
                    return value * 68.1818
                def speed_of_cheetah_to_knots(value):
                    return value * 59.2484
                def speed_of_cheetah_to_mach(value):
                    return value * 114.5
                def speed_of_cheetah_to_speed_of_light(value):
                    return value * 249448.5
                def speed_of_cheetah_to_speed_of_sound(value):
                    return value * 28.8
                def speed_of_cheetah_to_speed_of_snail(value):
                    return value * 8400
                def speed_of_cheetah_to_speed_of_cheetah(value):
                    return value

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
            - afterCreateBackup(bool): After removals, create a brand new backup. Only works if the dB specified, is this one.
            
            Exceptions:
            - dB backups with tag does not exist.
            - Cannot backup unloaded database.'''
            # Check if folder exists
            if not os.path.exists('db_'+str(tag[0])+'_Backups'):
                raise Exception('\n\nCall Function: --> db_Handler.Backup.clearBackups()\nDatabase backups with tag does not exist.')
            # Get all files in folder
            files = os.listdir('db_'+str(tag[0])+'_Backups')
            # Change directory to folder
            os.chdir('db_'+str(tag[0])+'_Backups')
            # Remove all files, except the latest one if exemptOne is True
            if exemptOne:
                for file in files:
                    if file != files[-1]:
                        os.remove(file)
            else:
                for file in files:
                    os.remove(file)
            # Create a new backup if afterCreateBackup is True
            if afterCreateBackup:
                if self.handler.tag[0] == tag:
                    self.handler.save.all()
                else:
                    raise Exception('\n\nCall Function: --> db_Handler.Backup.clearBackups()\nCannot backup unloaded database. Please ensure the database is loaded, and the database being cleared is the one currently running this instance. Current tag: '+str(self.handler.tag[0]))
        
        def compressBackups(self, tag):
            '''Compresses all backups for the database into a zip file. Zips will be located in a folder called (zippedBackups)
            Ex of filename: db_AAAA-1-11-24.zip'''
            # Check if folder exists
            if not os.path.exists('db_'+str(self.handler.tag[0])+'_Backups'):
                raise Exception('\n\nCall Function: --> db_Handler.Backup.compressBackups()\nDatabase backups with tag does not exist.')
            # Get all files in folder
            files = os.listdir('db_'+str(self.handler.tag[0])+'_Backups')
            # Change directory to folder
            os.chdir('db_'+str(self.handler.tag[0])+'_Backups')
            # Zip all files with zipfile.CompleteDirs
            with zipfile.ZipFile('db_'+str(self.handler.tag[0])+'-'+str(datetime.datetime.now().month)+'-'+str(datetime.datetime.now().day)+'.zip', 'w') as zipf:
                for file in files:
                    zipf.write(file)
            # Check if zippedBackups folder exists
            if not os.path.exists('../zippedBackups'):
                os.mkdir('../zippedBackups')
            # Move zip to folder
            os.rename('db_'+str(self.handler.tag[0])+'-'+str(datetime.datetime.now().month)+'-'+str(datetime.datetime.now().day)+'.zip', '../zippedBackups/db_'+str(self.handler.tag[0])+'-'+str(datetime.datetime.now().month)+'-'+str(datetime.datetime.now().day)+'.zip')
            # Remove all files
            for file in files:
                os.remove(file)
            
    class Save:
        '''Database saving class.
        \n - all(): Saves the entire database. This includes all data, rows/columns, and meta data.
        \n - VariabledSave(): Used periodically to save important variables for stable runtime of handler.'''
        def __init__(self, handler):
            self.handler = handler

        def mergeTempRowFile(self):
            '''Merges the tempRowFile with the main database file.'''
            # Close TempFile
            try:
                globals()['TempRowFile'+str(self.handler.tag[0])].close()
            except:
                # Already Closed/Doesn't exist
                pass
            # Check if file exists
            if os.path.exists('TempRowFile'+str(self.handler.tag[0])+'.txt'):
                # Open tempFile
                with open('TempRowFile'+str(self.handler.tag[0])+'.txt', 'r') as f:
                    tempFile = f.readlines()
                    f.close()
                # Add lines to self.handler.listStorage
                for line in tempFile:
                    self.handler.listStorage.append(eval(line))
                # Remove tempFile
                os.remove('TempRowFile'+str(self.handler.tag[0])+'.txt')

        def all(self):
            '''Saves the entire db instance. This includes all data, rows/columns, and meta data.'''
            global lastDatabaseSaved, userPw_ChangesEachSave, EncryptSaveFile, LoginKey
            # You can save a database even if it's empty. Allows for an easy setup of hundreds of databases.
            # Vars saved: tag, columnStorage, listStorage, owner, knownUsers, permissions, allowedPermissions, userPW

            # Make the name for our save file
            # Prevents the tag getting bracketed. Ex: db_[AAAA].txt
            saveNm='db_'+str(self.handler.tag[0])+'.txt'

            # Check if file exists
            if os.path.exists('db_'+str(self.handler.tag[0])+'.txt'):
                # Check if folder exists
                if not os.path.exists('db_'+str(self.handler.tag[0])+'_Backups'):
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
            svList = ['columnStorage', 'listStorage', 'owner', 'knownUsers', 'permissions', 'allowedPermissions']
            if EncryptSaveFile:
                # Encryption of save file.
                # Key for encryption, can be recreated by using the same password. Will be required for decryption.
                print('Login key:', LoginKey)
                out = str(self.handler.encryption.uniqueIDGen(maxKeyLength=50, password=str(LoginKey), consistantOutput=True))
                print('ID:', out)
            
                with open(saveNm, 'w') as f:
                    f.write('tag = '+str(self.handler.tag[0])+'\n')
                    for item in svList:
                        actual_value = getattr(self.handler, item)
                        line = (item + ' = ' + str(actual_value) +'\n')
                        f.write(self.handler.encryption.en(input=line, uniqueID=out))
                    if userPw_ChangesEachSave:
                        line = ('userPW = "'+str(self.handler.encryption.uniqueIDGen(maxKeyLength=50, password='EncryptionKey', consistantOutput=False))+'"\n')
                        f.write(self.handler.encryption.en(input=line, uniqueID=out))
                    else:
                        line = ('userPW = "'+str(self.handler.userPW)+'"\n')
                        f.write(self.handler.encryption.en(input=line, uniqueID=out))

                    f.write('')
                    f.close()
            if not EncryptSaveFile:
                with open(saveNm, 'w') as f:
                    f.write('tag = '+str(self.handler.tag[0])+'\n')
                    for item in svList:
                        actual_value = getattr(self.handler, item)
                        f.write(item + ' = ' + str(actual_value) +'\n')
                    if userPw_ChangesEachSave:
                        line = ('userPW = "'+str(self.handler.encryption.uniqueIDGen(maxKeyLength=50, password='EncryptionKey', consistantOutput=False))+'"\n')
                        f.write(line)
                    else:
                        line = ('userPW = "'+str(self.handler.userPW)+'"\n')
                        f.write(line)
                    f.write('')
                    f.close()

            # Verify TempRowFile is removed:
            try:
                os.remove('TempRowFile'+str(self.handler.tag[0])+'.txt')
            except:
                pass
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
        - tag (Only excuse if you know what your doing) must be reassigned after.
        - owner
        - known users
        - permissions
        - allowedPermissions
        - userPW
        
        Returns:
        False: If the database savefile requested does not exist'''
        global LoginKey, decryptSaveOnLoad, databasesLoaded
        # if db save file exists, then check if it's encrypted
        if os.path.exists('db_'+str(tag[0])+'.txt') == False:
            print('Ignoring load, as save file does not exist.')
            return False
        else:
            SaveEnc = self.CheckIfSaveIsEncrypted(tag=tag)
            # If password is specified, decrypt the save file first
            if SaveEnc == True:
                if self.CheckIfSaveIsEncrypted(tag=tag) == False:
                    raise Exception('\n\nCall Function: --> db_Handler.load()\nSave file is not encrypted. Cannot decrypt save file.')
                # Encryption of save file.
                # Key for encryption, can be recreated by using the same password. Will be required for decryption.
                out = str(self.encryption.uniqueIDGen(maxKeyLength=50, password=str(LoginKey), consistantOutput=True))
            
                # Check excusable variables
                allowedExcuses = ['columnStorage', 'listStorage', 'tag', 'owner', 'knownUsers', 'permissions', 'userLogged', 'allowedPermissions', 'userPW']
                for i in range(len(excuse)):
                    if excuse[i] not in allowedExcuses:
                        raise Exception('\n\nCall Function: --> db_Handler.load()\nInvalid excuse given. Excuse must be in the list of allowed excuses.')
                
                if tag != None:
                    # Set the tag to the one given
                    self.tag = [tag]
                elif tag == None and lastDatabaseSaved != None:
                    # Set the tag to the last saved database
                    self.tag = [lastDatabaseSaved]
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
                            if decryptSaveOnLoad and SaveEnc == True:
                                # Rewrite the save file with the decrypted data from variable (out)
                                tmpData = ''
                            with open(saveNm, 'r') as f:
                                for line in f:
                                    if SaveEnc == True:
                                        if 'tag =' not in line:
                                            line = self.encryption.en(input=line, uniqueID=out, decrypt=True)
                                        if decryptSaveOnLoad:
                                            tmpData += str(line)
                                    if ' = ' in line:
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
                                        if 'tag' not in excuse:
                                            if name == 'tag':
                                                self.tag[0] = eval(value)
                                        if 'columnStorage' not in excuse:
                                            if name == 'columnStorage':
                                                self.columnStorage = eval(value)
                                        if 'listStorage' not in excuse:
                                            if name == 'listStorage':
                                                self.listStorage = eval(value)
                                        if 'owner' not in excuse:
                                            if name == 'owner':
                                                self.owner = eval(value)
                                        if 'knownUsers' not in excuse:
                                            if name == 'knownUsers':
                                                self.knownUsers = eval(value)
                                        if 'permissions' not in excuse:
                                            if name == 'permissions':
                                                self.permissions = eval(value)
                                        if 'allowedPermissions' not in excuse:
                                            if name == 'allowedPermissions':
                                                self.allowedPermissions = eval(value)
                                        if 'userPW' not in excuse:
                                            if name == 'userPW':
                                                self.userPW = int(eval(value))
                                    else:
                                        raise Exception('\n\nCall Function: --> db_Handler.load()\nInvalid data in save file. Unable to load database. Please check the save file for corruption.')
                            try:
                                # if the tag within the list (tag) is a list in a list, remove the within list.
                                # Fixes the issue of the tag being a list within a list.
                                if type(self.tag[0]) == list:
                                    self.tag = self.tag[0]
                            except:
                                pass
                            if decryptSaveOnLoad and SaveEnc == True:
                                f = open(saveNm, 'w')
                                f.write(tmpData)
                                f.close()
                            databasesLoaded.append(self.tag[0])
                            print('Database loaded:', saveNm)
                            True
                        else:
                            raise Exception('\n\nCall Function: --> db_Handler.load()\nDatabase save file does not exist.')
    
    def dataLoadingIssueDetection():
        '''Scans a selected save file for errors or possible corruption. Called automatically before a database loads, and/or if a save file fails to load.
        \n Other functions will be created to attempt repairs on common issues, if possible. If not, the user will be notified of the issue and possible ways to repair the save file.
        \n Remember, this handler comes with a backup manager. So if all else fails, you can always restore a backup. Granted if your doing them on a regular basis.'''
        pass

    def CheckIfSaveIsEncrypted(self, tag=None):
        '''This function checks wether a save file is encrypted or not. This is used to determine if the save file should requires a key for decrypting before loading.
        Returns:
        - True: Save file is encrypted
        - False: Save file is not encrypted'''
        # Check if tag is specified
        if tag == None:
            # If not, set the tag to the current database
            tag = self.tag[0]
        # Grab a line from the save file, The first line should be the tag, and not encrypted, the second line if not encrypted, should be a variable assinged to a value called columnStorage.
        # Calculate the total number of lines in the file
        with open('db_'+str(tag[0])+'.txt', 'r') as file:
            total_lines = sum(1 for line in file)

        # Calculate x (half of the total lines, rounded up)
        x = -(-total_lines // 2)  # Using integer division rounding up

        # Iterate through the file up to x lines
        with open('db_'+str(tag[0])+'.txt', 'r') as file:
            for i, line in enumerate(file):
                if i >= x:
                    break  # Stop after x lines
                if 'columnStorage =' in line:
                    return False
                if 'listStorage =' in line:
                    return False
        return True
            
    class Meta:
        '''Add or Modify meta data of a database.'''
        def __init__(self, handler):
            self.handler = handler

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
# Patch Notes for this version of the handler: 0.1.3
# 1) Added new setting: loadDBOnEachStartup
    # - Simplifies the process of loading a database on each startup.
# 2) Added quickSave argument to AddRow function.
    # - Used for apps that will be adding constant rows, but cannot afford the power needed to save after each if redundency is needed.
    # - .makeRowTmpFile() Should be called before use. Not required.
