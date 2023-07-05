from flask import Flask, render_template, request, redirect, url_for, session
import db, string, random

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))

@app.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg')
    
    if msg == None:
        return render_template('index.html')
    else:
        return render_template('index.html', msg=msg)

@app.route('/', methods=['POST'])
def login():
    mail = request.form.get('mail')
    password = request.form.get('password')

    if db.login(mail, password):
        session['user'] = True # session にキー：'user', バリュー:True を追加
        return redirect(url_for('mypage'))
    else :
        error = 'ログインに失敗しました。'
        return render_template('index.html', error=error)

@app.route('/mypage', methods=['GET'])
def mypage():
# session にキー：'user' があるか判定
    if 'user' in session:
        return render_template('mypage.html') # session があればmypage.html を表示
    else :
        return redirect(url_for('index')) # session がなければログイン画面にリダイレクト
    
@app.route('/logout')
def logout():
    session.pop('user', None) # session の破棄
    return redirect(url_for('index')) # ログイン画面にリダイレクト

@app.route('/register')
def register_form():
    return render_template('register.html')

@app.route('/register_exe', methods=['POST'])
def register_exe():
    user_name = request.form.get('username')
    mail = request.form.get('mail')
    password = request.form.get('password')
    
    count = db.insert_user(user_name, mail, password)
    
    if count == 1:
        msg = '登録が完了しました。'
        return redirect(url_for('index', msg=msg))
    else:
        error = '登録に失敗しました。'
        return render_template('register.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
    
