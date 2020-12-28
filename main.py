import sqlite3
import os


def handleCommandLine():
    print('''
    Welcome to Locker Man! ft.rzla

    Enter 1 for Store a new File

    Enter 2 for Revert a stored File
  ''')

    choice = input("Enter yr option! ")
    if int(choice) == 1:
        encrypt_newFile()

    elif int(choice) == 2:
        retriveData()


def returnBlobData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


def store_dataintoSql(fileToWrite, password, name, extension, path):

    try:
        sqliteConnection = sqlite3.connect('data.db')
        cursor = sqliteConnection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS data
         (photo BLOB,
         password NOT NULL,
         name,
         extension, path);''')

        sqlite_insert_blob_query = """ INSERT INTO data
                                  (photo, password, name, extension, path) VALUES (?, ?, ?, ?, ?)"""

        data_tuple = (fileToWrite, password, name, extension, path)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)


def encrypt_newFile():
    print('''
    Hey Man! Enter the <path of the File> <Password to Store>
    ''')
    fileName = input("Enter the path of the file Bruh! ")

    if os.path.exists(fileName):
        print("Okay")
        passwordToDecrypt = input("Enter the password Bro !")
        while len(passwordToDecrypt) < 8:
            print("Password Must have 8 Characters bro 😂")
            passwordToDecrypt = input("Enter the password Bro !")

        blob_data = returnBlobData(fileName)
        extension = os.path.splitext(fileName)[-1]
        name = fileName.split('/')[-1]

        store_dataintoSql(blob_data, passwordToDecrypt,
                          name, extension, fileName)
        handleCommandLine()
    else:
        print("Enter Right Path bro")
        encrypt_newFile()


def retriveData():
    print("Hey Welocome broi")
    name = input("Enter the file name you want to edukal! ")
    password = input("Enter the password of the file bro XD! ")
    extension = input("Enter the extension of the file!")
    try:
        sqliteConnection = sqlite3.connect('data.db')
        cursor = sqliteConnection.cursor()

        sql_fetch_blob_query = """SELECT * from data where name = ?"""
        cursor.execute(sql_fetch_blob_query, (name,))
        record = cursor.fetchall()
        for row in record:
            #password, name, extension
            blobData = row[0]
            name = row[2]
            extension = row[3]

            if password != row[1]:
                print("Password Wromg Makka")
                handleCommandLine()
            else:
                with open('test'+extension, 'wb') as file:
                    file.write(blobData)

        cursor.close()

    except sqlite3.Error as error:
        print("PAssword Thappu da Mandaya")


handleCommandLine()
