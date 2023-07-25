import os, psycopg2, string, random, hashlib

def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

def get_salt():
    charset = string.ascii_letters + string.digits
    
    salt = ''.join(random.choices(charset, k=30))
    return salt

def get_hash(password, salt):
    b_pw = bytes(password, 'utf-8')
    b_salt = bytes(salt, 'utf-8')
    hashed_passwrd = hashlib.pbkdf2_hmac('sha256', b_pw, b_salt, 1246).hex()
    return hashed_passwrd

def insert_user(user_name, mail, password):
    sql = 'INSERT INTO user_account VALUES (default, %s, %s, %s, %s)'

    salt = get_salt() # ソルトの生成
    hashed_password = get_hash(password, salt) # 生成したソルトでハッシュ

    try : # 例外処理
        connection = get_connection() 
        cursor = connection.cursor()
        cursor.execute(sql, (user_name, mail, hashed_password, salt))
        count = cursor.rowcount # 更新件数を取得
        connection.commit()
        
    except psycopg2.DatabaseError: # Java でいうcatch 失敗した時の処理をここに書く
        count = 0 # 例外が発生したら0 をreturn する。
    
    finally: # 成功しようが、失敗しようが、close する。
        cursor.close()
        connection.close()
    
    return count

def login(mail, password):
    sql = 'SELECT hashed_password, salt FROM user_account WHERE mail = %s'
    flg = False
    
    try :
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (mail, ))
        user = cursor.fetchone()
        
        if user != None:
            salt = user[1]
            
            hashed_password = get_hash(password, salt)
            
            if hashed_password == user[0]:
                flg = True
    except psycopg2.DatabaseError :
        flg = False
    finally :
        cursor.close()
        connection.close()
        
    return flg

def insert_absence(date, department, name, reason):
    sql = 'INSERT INTO user_absence VALUES (default, %s, %s, %s, %s)'
          
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (date, department, name, reason))
        count = cursor.rowcount # 更新件数を取得
        connection.commit()
        
    except psycopg2.DatabaseError:
        count = 0
    
    finally:
        cursor.close()
        connection.close()
    
    return count

def get_absence_list():
    connection = get_connection()
    cursor = connection.cursor()

    sql = 'SELECT date, department, name, reason FROM user_absence ORDER BY date, department, name'

    cursor.execute(sql)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()
    return rows

def search_absence_by_criteria(criteria, keyword):
    connection = get_connection()
    cursor = connection.cursor()

    sql = 'SELECT date, department, name, reason FROM user_absence WHERE {} = %s ORDER BY date, department, name'.format(criteria)

    cursor.execute(sql, (keyword,))
    rows = cursor.fetchall()

    cursor.close()
    connection.close()
    return rows

def update_absence(id, reason):
    sql = 'UPDATE user_absence SET reason=%s WHERE date=%s'
    try:
        connection = get_connection() 
        cursor = connection.cursor()
        cursor.execute(sql, (reason, id))
        count = cursor.rowcount
        connection.commit()
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()
    
    return count

def delete_absence(id):
    sql = 'DELETE FROM user_absence WHERE date = %s'
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (id,))
        count = cursor.rowcount
        connection.commit()
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()

    return count