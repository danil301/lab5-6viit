import requests
from flask import Flask, render_template, request, redirect
import  psycopg2

app = Flask(__name__)
conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="3012",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):

            # получаем логин и пароль из формы html
            username = request.form.get('username')
            password = request.form.get('password')

            # проверка полей логина и пароля на заполненность
            if not username or not password:
                return render_template('new.html', Error="Пустой логин или пароль")




            # выбираем из бд строку, где поля логина и пароля в базе совпадают с полями из html
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            # заносим данные в список
            records = list(cursor.fetchall())

            # рендерим страницу account.html, передавая в неё нужные данные
            if len(records) > 0:
                return render_template('account.html', full_name=records[0][1], login=records[0][2], password=records[0][3])
            else:
                return render_template('new.html', Error="Пользователя нет в базе данных либо неверный логин или пароль")
        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')

@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        if not name or not login or not password:
            return render_template('new.html', Error="Не все поля заполнены")

        cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                       (str(name), str(login), str(password)))
        conn.commit()

        return redirect('/login/')

    return render_template('registration.html')




