from flask import Flask, render_template, request, redirect, url_for, session
import os
import pathlib
import requests
from app import dao, login
from app import app, db
from flask_login import login_user, logout_user, login_required, current_user

# import requests
# from flask import Flask, session, abort, redirect, request
# from google.oauth2 import id_token
# from google_auth_oauthlib.flow import Flow
# from pip._vendor import cachecontrol
# import google.auth.transport.requests


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/login", methods=['get', 'post'])
def login_user_process():
    if request.method.__eq__('POST'):
        email = request.form.get('email')
        password = request.form.get('password')
        user = dao.auth_user(email=email, password=password)
        if user:
            login_user(user=user)
            if current_user.type == 'patient':
                return redirect("/")
            elif current_user.type == 'doctor':
                return redirect('/doctor')
            elif current_user.type == 'administrator':
                return redirect('/admin')
            elif current_user.type == 'nurse':
                return redirect('/nurse')
            else: # cashier
                return redirect('/cashier')

    return render_template("login.html")




@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)

@app.route('/logout')
def process_logout_user():
    logout_user()
    return redirect("/login")


@app.route('/register', methods=['get', 'post'])
def register_user():
    err_msg = ""
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if password.__eq__(confirm):
            try:
                dao.add_user(name=request.form.get('name'),
                             email=request.form.get('email'),
                             password=password, err_msg=err_msg)
            except:
                err_msg = 'Hệ thống đang bận, vui lòng thử lại sau!'
            else:
                return redirect('/login')
        else:
            err_msg = "Mật khẩu không khớp! Vui lòng nhập lại"
    return render_template('register.html', err_msg=err_msg)



@app.route('/info', methods=['get','post'])
def update():
    err_msg = ""

    if request.method.__eq__('POST'):
        try:
            dao.update_info(namSinh=request.form.get('namSinh'),
                            sdt=request.form.get('sdt'),
                            diaChi=request.form.get('diaChi'),
                            avatar=request.files.get('avatar'),
                            gioiTinh=request.form.get('gioiTinh'),
                            Patient_id=current_user.id)
        except:
            err_msg = 'Hệ thống đang bận, vui lòng thử lại sau!'
        else:
            err_msg = "Cập nhật thành công"
        return redirect('/info')
    return render_template('info.html', err_msg=err_msg)


if __name__ == '__main__':
    from app import admin
    app.run(debug=True)
