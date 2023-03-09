import sqlite3


# Restituisce una lista con tutti gli untenti
def get_users():
    sql = "SELECT * FROM USERS;"
    conn = sqlite3.connect("db/podcast.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql)
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return users


# Restituisce un dizionario con l'utente cercato per id
def get_user(user_id):
    sql = "SELECT * FROM USERS WHERE UserId == ?;"
    conn = sqlite3.connect("db/podcast.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql, (user_id, ))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return user


# Restituisce un utente cercato per email (Email è non ripetibile)
def get_user_by_email(username):
    sql = "SELECT * FROM USERS WHERE Email == ?;"
    conn = sqlite3.connect("db/podcast.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql, (username, ))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    return user


# Restituisce l'elenco dei podcast seguiti da un utente dato il suo id
def get_podcasts_followed(userId):
    sql = "SELECT *     \
        FROM FOLLOWS F, PODCASTS P, USERS U    \
        WHERE F.UserId = ? AND F.PdId = P.PdId AND P.UserId = U.UserId \
        ORDER BY P.Title;"
    conn = sqlite3.connect("db/podcast.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql, (userId, ))
    podcasts = cursor.fetchall()
    cursor.close()
    conn.close()

    return podcasts


# Verifica se un determinato utente segue un determinato podcast
def get_follow(userId, pdId):
    sql = "SELECT UserId     \
        FROM FOLLOWS    \
        WHERE UserId = ? AND PdId = ?;"
    conn = sqlite3.connect("db/podcast.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql, (userId, pdId))
    follow = cursor.fetchone()
    cursor.close()
    conn.close()

    return follow


# Inserisce l'utente nel database
def insert_user(user):
    sql = "INSERT INTO USERS (Email, Name, Surname, Creator, Password) \
        VALUES (?, ?, ?, ?, ?)"
    conn = sqlite3.connect("db/podcast.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False

    try:
        cursor.execute(sql, (user['Email'], user['Name'], user['Surname'], user['Creator'], user['Password']))
        conn.commit()
        success = True
    except:
        conn.rollback()
    
    cursor.close()
    conn.close()
    
    return success


# Dato un utente e un podcast inserisce il follow
def insert_follow(user, pdId):
    sql = "INSERT INTO FOLLOWS (UserId, PdId) \
        VALUES (?, ?)"
    conn = sqlite3.connect("db/podcast.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    success = False

    try:
        cursor.execute(sql, (user, pdId))
        conn.commit()
        success = True
    except:
        conn.rollback()

    cursor.close()
    conn.close()
    
    return success


# Dato un utente e un podcast elimina il follow
def delete_follow(user, pdId):
    sql = "DELETE FROM FOLLOWS WHERE UserId = ? AND PdId = ?;"
    conn = sqlite3.connect("db/podcast.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    
    try:
        cursor.execute(sql, (user, pdId))
        conn.commit()
        success = True
    except:
        conn.rollback()
    
    cursor.close()
    conn.close()

    return success
