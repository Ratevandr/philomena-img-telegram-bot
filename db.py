import sqlite3
import os.path
import logging


def createDB():
        if (not os.path.isfile('botDB.db')):
            conn = sqlite3.connect("botDB.db")  # или :memory: чтобы сохранить в RAM
            cursor = conn.cursor()
            # Создание таблицы
            cursor.execute("""CREATE TABLE msgWithImg (id INTEGER PRIMARY KEY AUTOINCREMENT, imgUrl text, msgId INT8, groupID INT8) """)
            cursor.execute("""CREATE TABLE answers (id INTEGER, answer text UNIQUE,FOREIGN KEY (id) REFERENCES msgWithImg(id)) """)
            conn.commit()
        else:
            logging.debug("DB already exist")



def addQuiz(imgUrl, msgId, groupId):
    conn = sqlite3.connect("botDB.db")
    cursor = conn.cursor()
    data = (imgUrl, msgId, groupId)
    cursor.execute(
        """INSERT INTO msgWithImg  VALUES (null, ?, ?, ?);""",  data)
    conn.commit()


def searchMsgWithImgID(msgID, grouID):
    data = (msgID, grouID)

    conn = sqlite3.connect("botDB.db")  # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    cursor.execute(
        """SELECT id FROM msgWithImg WHERE msgId LIKE ? AND groupID LIKE ?""", data)
    keyID = cursor.fetchall()
    if (len(keyID) > 0):
        return int(keyID[0][0])
    return -1


def getAnswers(keyID):
    conn = sqlite3.connect("botDB.db")  # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    cursor.execute("SELECT answer FROM answers WHERE id LIKE ?", (keyID,))
    answers = cursor.fetchall()
    answList = []
    for answ in answers:
        if (len(answ) > 0):
            answList.append(answ[0])
    return answList


def insertAnswer(keyID, answer):
    conn = sqlite3.connect("botDB.db")
    cursor = conn.cursor()
    data = (keyID, answer)
    try:
        cursor.execute(
            """INSERT INTO answers  VALUES (?,?);""",  data)
        conn.commit()
    except Exception as err:
        logging.warn(f"Most likely the field {answer} already exists. Error {err}")


def deleteOnKind(msgID, grouID):
    conn = sqlite3.connect("botDB.db")
    cursor = conn.cursor()

    data = (msgID, grouID)
    cursor.execute(
        """DELETE FROM msgWithImg WHERE msgId=? AND groupID=?""",  data)
    searchedMsgId = searchMsgWithImgID(msgID, grouID)
    cursor.execute(
        """DELETE FROM answers WHERE id=?""", (searchedMsgId,))
    conn.commit()

 
   # if (not os.path.isfile('botDB.db')):
   #     createDB()
   # else:
   #     print("DB already exist")

#addQuiz("http:/kek", 218, -451410879)
#id = searchMsgWithImgID(218, -451410879)
#if (id > -1):
#    print(id)
#    insertAnswer(id, "tag")
#    getAnswers(id)
#    deleteOnKind(218, -451410879)
