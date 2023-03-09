import sqlite3


# Restituisce una lista con tutti i podcast (dizionari)
def get_podcasts():
    sql = "SELECT * FROM PODCASTS   \
        ORDER BY PdId DESC;"
    conn = sqlite3.connect("db/podcast.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql)
    posts = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return posts


# Restituisce una lista di tutti i post e l'utente di ciascun post
def get_podcasts_users():
    sql = "SELECT * \
        FROM PODCASTS P, USERS U \
        WHERE P.UserId = U.UserId \
        ORDER BY PdId DESC;"
    conn = sqlite3.connect("db/podcast.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql)
    posts_users = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return posts_users


# Dato l'id di un podcast restituisce le sue informazioni, con l'utente che l'ha creato
def get_podcast_user(pdId):
    sql = "SELECT * \
        FROM PODCASTS P, USERS U \
        WHERE P.PdId = ? AND P.UserId = U.UserId;"
    conn = sqlite3.connect("db/podcast.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql, (pdId, ))
    podcast = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return podcast 
    

# Restituisce il massimo PdId nel db
def get_max_id():
    sql = "SELECT MAX(PdId) AS Max FROM PODCASTS;"
    conn = sqlite3.connect("db/podcast.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql)     
    max_id = cursor.fetchone()
    cursor.close()
    conn.close()

    return max_id


# Dato l'id del podcast restituisce il nome dell'immagine
def get_podcast_img(pdId):
    sql = "SELECT Img \
        FROM PODCASTS   \
        WHERE PdId = ?;"
    conn = sqlite3.connect("db/podcast.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql, (pdId, ))     
    img = cursor.fetchone()
    cursor.close()
    conn.close()

    return img


# Iserisce un nuovo podcast nel database
def insert_podcast(podcast):
    sql = "INSERT INTO PODCASTS (PdId, Title, Img, Description, Category, UserId) \
        VALUES (?, ?, ?, ?, ?, ?);"
    conn = sqlite3.connect("db/podcast.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False

    try:
        cursor.execute(sql, (podcast['PdId'], podcast['Title'], podcast['Img'], podcast['Description'], podcast['Category'], podcast['UserId']))
        conn.commit()
        success = True
    except:
        conn.rollback()

    cursor.close()
    conn.close()

    return  success


# Dato l'id del podcast lo elimino dal database
def delete_podcast(pdId):
    sql = "DELETE FROM PODCASTS WHERE PdId = ?;"
    conn = sqlite3.connect("db/podcast.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()
    
    success = False
    
    try:
        cursor.execute(sql, (pdId,))
        conn.commit()
        success = True
    except:
        conn.rollback()

    cursor.close()
    conn.close()

    return success


# Aggiorno il podcast
def modify_podcast(podcast):
    sql = "UPDATE PODCASTS      \
        SET Title = ?, Img = ?, Description = ?, Category = ?\
        WHERE PdId = ?;"
    conn = sqlite3.connect("db/podcast.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    success = False
    
    try:
        cursor.execute(sql, (podcast['Title'], podcast['Img'], podcast['Description'], podcast['Category'], podcast['PdId']))
        conn.commit()
        success = True
    except:
        conn.rollback()

    cursor.close()
    conn.close()

    return success
