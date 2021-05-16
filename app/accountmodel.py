from app import app, mysql
import random

class account():
    def __init__(self, username=None, password=None, accountType=None):
        self.username = username
        self.password = password
        self.accountType = accountType

  
    def addAccount(self):
        
        cur = mysql.connection.cursor()
        # generate unique userID
        uniqueIndicator = False
        while uniqueIndicator == False:
            userID = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
            cur.execute("SELECT * FROM accounts WHERE userID=%s", (userID,))
            data = cur.fetchall()
            if len(data) == 0 or data == None:
                uniqueIndicator = True

        cur.execute("INSERT INTO accounts(userID,username,password,accountType) VALUES (%s,%s,AES_ENCRYPT(%s,UNHEX(SHA2('kumsainibai',512))),%s)",
                    (userID,self.username,self.password,self.accountType))
        mysql.connection.commit()
        return userID
    
    @classmethod 
    def login(cls,usernameOrEmail,password):
        cur = mysql.connection.cursor()
        cur.execute('''SELECT * FROM (SELECT accounts.userID,accounts.username,AES_DECRYPT(accounts.password,UNHEX(SHA2('kumsainibai',512))),accounts.accountType,profiles.firstName,profiles.lastName,profiles.birthdate,profiles.gender,contacts.email,contacts.phoneNumber
                        FROM accounts, profiles, contacts
                        WHERE accounts.userID = profiles.profileID AND profiles.profileID = contacts.contactID) AS accountInfo
                        ''')
        data = cur.fetchall()
        #validate login credentials
        for i in data:
            x = i[2]
            x = x.decode('utf8')
            if (i[1]==usernameOrEmail and x==password) or (i[-1]==usernameOrEmail and x==password):
                n = len(i)
                m = 0
                accountInfo = []
                while m<n:
                    if m!=2 and m!=6:
                        accountInfo.append(i[m])
                        m+=1
                    elif m==6:
                        splitDate = str(i[6])
                        accountInfo.append(splitDate)
                        m+=1
                    else:
                        print(x)
                        accountInfo.append(x)
                        m+=1
                return accountInfo
            else:
                msg = "Invalid login credentials"
                return msg
            
    @classmethod
    def changePassword(cls,oldPassword,newPassword):
        cur = mysql.connection.cursor()
        cur.execute("UPDATE accounts SET password=AES_ENCRYPT(%s,UNHEX(SHA2('kumsainibai',512))) WHERE password=AES_ENCRYPT(%s,UNHEX(SHA2('kumsainibai',512))) ",(newPassword,oldPassword))
        mysql.connection.commit()
        
    @classmethod
    def searchAllAccounts(cls):
        cur = mysql.connection.cursor()
        cur.execute("SELECT userID,username FROM accounts")
        data = cur.fetchall()
        if data!=None:
            return data
        else:
            data = []
            return data