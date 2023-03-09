import sqlite3


# Dato l'id di un podcast mi restituisce tutti i suoi episodi ordinati dal più recente al meno
def get_episodes_podcast(pdId):
    sql = "SELECT EpId, Title, Description, Date, Audio \
        FROM EPISODES   \
        WHERE PdId = ?  \
        ORDER BY Date DESC, EpId DESC;"
    conn = sqlite3.connect("db/podcast.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql, (pdId, ))
    episodes = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return episodes


# Dato l'id di un podcast mi restituisce tutti i nomi dei file audio dei suoi episodi
def get_episodes_audio(pdId):
    sql = "SELECT Audio \
        FROM EPISODES   \
        WHERE PdId = ?;"
    conn = sqlite3.connect("db/podcast.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql, (pdId, ))
    episodes = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return episodes


# Dato l'id di un episodio ne restituisce tutte le informazioni
def get_episode(epId):
    sql = "SELECT * \
        FROM EPISODES \
        WHERE EpId = ?;"
    conn = sqlite3.connect("db/podcast.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql, (epId, ))
    episode = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return episode


# Dato l'id dell'episodio restituisce il nome dell'audio
def get_podcast_img(epId):
    sql = "SELECT Audio \
        FROM EPISODES   \
        WHERE EpId = ?;"
    conn = sqlite3.connect("db/podcast.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql, (epId, ))     
    audio = cursor.fetchone()
    cursor.close()
    conn.close()

    return audio


# Dato l'id di un commento ritorno tutte le sue informazioni
def get_comment(comId):
    sql = "SELECT * \
        FROM COMMENTS \
        WHERE ComId = ?;"
    conn = sqlite3.connect("db/podcast.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql, (comId, ))
    comment = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return comment


# Dato l'id di un episodio restituisce tutti i commenti con i relativi utenti
def get_comments_users(epId):
    sql = "SELECT * \
        FROM COMMENTS C, USERS U \
        WHERE C.EpId = ? AND C.UserId = U.UserId    \
        ORDER BY C.Date DESC, C.ComId DESC;"
    conn = sqlite3.connect("db/podcast.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql, (epId, ))
    episode = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return episode


# Restituisce il massimo EpId nel db
def get_max_id():
    sql = "SELECT MAX(EpId) AS Max FROM EPISODES;"
    conn = sqlite3.connect("db/podcast.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql)
    max_id = cursor.fetchone()
    cursor.close()
    conn.close()

    return max_id


# Dato l'id dell'episodio restituisce il nome del file audio
def get_episode_audio(epId):
    sql = "SELECT Audio \
        FROM EPISODES   \
        WHERE EpId = ?;"
    conn = sqlite3.connect("db/podcast.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql, (epId, ))
    img = cursor.fetchone()
    cursor.close()
    conn.close()

    return img


# Iserisce un nuovo episodio nel database
def insert_episode(episode):
    sql = "INSERT INTO EPISODES (EpId, Title, PdId, Description, Date, Audio) \
        VALUES (?, ?, ?, ?, ?, ?);"
    conn = sqlite3.connect("db/podcast.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    success = False

    try:
        cursor.execute(sql, (episode['EpId'], episode['Title'], episode['PdId'], episode['Description'], episode['Date'], episode['Audio']))
        conn.commit()
        success = True
    except:
        conn.rollback()

    cursor.close()
    conn.close()

    return success


# Inserisce un nuovo commento
def insert_comment(comment):
    sql = "INSERT INTO COMMENTS (EpId, UserId, Text, Date) \
        VALUES (?, ?, ?, ?);"
    conn = sqlite3.connect("db/podcast.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    success = False
    
    try:
        cursor.execute(sql, (comment['EpId'], comment['UserId'], comment['Text'], comment['Date']))
        conn.commit()
        success = True
    except:
        conn.rollback()

    cursor.close()
    conn.close()

    return success


# Dato l'id dell'episodio lo elimino dal database
def delete_episode(epId):
    sql = "DELETE FROM EPISODES WHERE EpId = ?;"
    conn = sqlite3.connect("db/podcast.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()
    
    success = False
    
    try:
        cursor.execute(sql, (epId, ))
        conn.commit()
        success = True
    except:
        conn.rollback()
    
    cursor.close()
    conn.close()

    return success


# Dato l'id del commento lo elimino dal database
def delete_comment(comId):
    sql = "DELETE FROM COMMENTS WHERE ComId = ?;"
    conn = sqlite3.connect("db/podcast.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    success = False
    
    try:
        cursor.execute(sql, (comId, ))
        conn.commit()
        success = True
    except:
        conn.rollback()
    
    cursor.close()
    conn.close()

    return success


# Aggiorna l'episodio
def modify_episode(episode):
    sql = "UPDATE EPISODES      \
        SET Title = ?, Description = ?, Date = ?, Audio = ?\
        WHERE EpId = ?;"
    conn = sqlite3.connect("db/podcast.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    success = False
    
    try:
        cursor.execute(sql, (episode['Title'], episode['Description'], episode['Date'], episode['Audio'], episode['EpId']))
        conn.commit()
        success = True
    except:
        conn.rollback()
    
    cursor.close()
    conn.close()

    return success


# Modicica un commento
def modify_comment(comment):
    sql = "UPDATE COMMENTS      \
        SET Text = ?    \
        WHERE ComId = ?;"
    conn = sqlite3.connect("db/podcast.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    
    try:
        cursor.execute(sql, (comment['Text'], comment['ComId']))
        conn.commit()
        success = True
    except:
        conn.rollback()
    
    cursor.close()
    conn.close()

    return success
