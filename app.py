from flask import Flask, render_template, request, redirect, url_for, session
import db, string, random
from datetime import timedelta

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))

@app.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg')
    
    if msg == None:
        return render_template('index.html')
    else :
        return render_template('index.html', msg=msg)

@app.route('/', methods=['POST'])
def login():
    mail = request.form.get('mail')
    password = request.form.get('password')

    if db.login(mail, password):
        session['user'] = True
        session.permanent = True
        app.permanent_session_lifetime = timedelta(hours=1)
        return redirect(url_for('mypage'))
    else :
        error = 'ログインに失敗しました。'
        return render_template('index.html', error=error)
    
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/mypage', methods=['GET'])
def mypage():
    if 'user' in session:
        return render_template('mypage.html')
    else :
        return redirect(url_for('index'))
 
@app.route('/register')
def register_form():
    return render_template('register.html')

@app.route('/register_exe', methods=['POST'])
def register_exe():
    user_name = request.form.get('username')
    mail = request.form.get('mail')
    password = request.form.get('password')
    
    if user_name == '':
        error = 'ユーザ名が未入力です。'
        return render_template('register.html', error=error, user_name=user_name, mail=mail, password=password)
    if mail == '':
        error = 'メールアドレスが未入力です。'
        return render_template('register.html', error=error, user_name=user_name, mail=mail, password=password)
    if password == '':
        error = 'パスワードが未入力です。'
        return render_template('register.html', error=error, user_name=user_name, mail=mail, password=password)
    
    count = db.insert_user(user_name, mail, password)
    
    if count == 1:
        msg = '登録が完了しました。'
        return redirect(url_for('index', msg=msg))
    else:
        error = '登録に失敗しました。'
        return render_template('register.html', error=error)

@app.route('/register_absence')
def register_absence_form():
    return render_template('register_absence.html')

@app.route('/register_absence_exe', methods=['POST'])
def register_absence_exe():
    date = request.form.get('date')
    department = request.form.get('department')
    name = request.form.get('name')
    reason = request.form.get('reason')
    
    if date == '':
        error = '日付が未入力です。'
        return render_template('register_absence.html', error=error, date=date, department=department, name=name, reason=reason)
    if department == '':
        error = '学科が未入力です。'
        return render_template('register_absence.html', error=error, date=date, department=department, name=name, reason=reason)
    if name == '':
        error = '学生の名前が未入力です。'
        return render_template('register_absence.html', error=error, date=date, department=department, name=name, reason=reason)
    if reason == '':
        error = '欠席理由が未入力です。'
        return render_template('register_absence.html', error=error, date=date, department=department, name=name, reason=reason)
    
    count = db.insert_absence(date, department, name, reason)
    
    if count == 1:
        msg = '登録が完了しました。'
        return redirect(url_for('show_absence_list', msg=msg))
    else:
        error = '登録に失敗しました。'
        return render_template('register_absence.html', error=error)
    
@app.route('/absence_list')
def show_absence_list():
    absence_list = db.get_absence_list()
    return render_template('absence_list.html', absence_list=absence_list)
 
@app.route('/search_absence', methods=['POST'])
def search_absence():
    criteria = request.form.get('criteria')
    keyword = request.form.get('keyword')
    absence_list = db.search_absence_by_criteria(criteria, keyword)
    return render_template('absence_list.html', absence_list=absence_list)
 
@app.route('/edit_absence')
def edit_absence():
    return render_template('edit_absence.html')
 
@app.route('/edit_absence_exe/<string:id>', methods=['POST'])
def edit_absence_exe(id):
    absence_info = db.get_absence_by_id(id)
    if request.method == 'POST':
        reason = request.form.get('reason')

        count = db.update_absence(id, reason)

        if count == 1:
            msg = '更新が完了しました。'
            return redirect(url_for('show_absence_list', msg=msg))
        else:
            error = '更新に失敗しました。'
            return render_template('edit_absence.html', id=id, error=error, reason=reason)
    else:
        return render_template('edit_absence.html', id=id, reason=absence_info[3])
 
@app.route('/delete_absence/<string:id>')
def delete_absence(id):
    count = db.delete_absence(id)
    if count == 1:
        msg = '削除が完了しました。'
    else:
        msg = '削除に失敗しました。'
    return redirect(url_for('show_absence_list', msg=msg))
 
if __name__ == '__main__':
    app.run(debug=True)
