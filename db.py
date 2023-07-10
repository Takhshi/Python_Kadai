import os, psycopg2, string, random, hashlib

def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

def insert_user(user_name, password):
    sql = 'INSERT INTO user_account VALUES (default, %s, %s, %s)'

    salt = get_salt() # ソルトの生成
    hashed_password = get_hash(password, salt) # 生成したソルトでハッシュ

    try : # 例外処理
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (user_name, password, salt))
        count = cursor.rowcount # 更新件数を取得
        connection.commit()
        
    except psycopg2.DatabaseError: # Java でいうcatch 失敗した時の処理をここに書く
        count = 0 # 例外が発生したら0 をreturn する。
    
    finally: # 成功しようが、失敗しようが、close する。
        cursor.close()
        connection.close()
    
    return count

def get_salt():
    # 文字列の候補(英大小文字+ 数字)
    charset = string.ascii_letters + string.digits
    # charset からランダムに30文字取り出して結合
    salt = ''.join(random.choices(charset, k=30))
    return salt

# ソルトとPWからハッシュ値を生成
def get_hash(password, salt):
    b_pw = bytes(password, "utf-8")
    b_salt = bytes(salt, "utf-8")
    hashed_password = hashlib.pbkdf2_hmac("sha256", b_pw, b_salt, 1246).hex()
    return hashed_password

def login(mail, password):
    sql = 'SELECT hashed_password, salt FROM user_account WHERE mail = %s'
    flg = False
    try :
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (mail,))
        user = cursor.fetchone()
        if user != None:
            # SQLの結果からソルトを取得
            salt = user[1]
            
            # DBから取得したソルト+ 入力したパスワードからハッシュ値を取得
            hashed_password = get_hash(password, salt)
            
            # 生成したハッシュ値とDBから取得したハッシュ値を比較する
            if hashed_password == user[0]:
                flg = True
    except psycopg2.DatabaseError :
        flg = False
    finally :
        cursor.close()
        connection.close()
    return flg