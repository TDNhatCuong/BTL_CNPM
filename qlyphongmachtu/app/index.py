from datetime import date
from flask import Flask, render_template, request, redirect, jsonify
from flask import request
from app import dao, login
from app import app, db
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Books


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin/login', methods=['post'])
def login_admin_process():
    email = request.form.get('email')
    password = request.form.get('password')

    user = dao.auth_user(email=email, password=password)
    if user:
        login_user(user=user)
        if current_user.type == 'patient':
            return redirect("/")
        else:
            return redirect('/admin')

    return redirect('/admin')


@app.route('/booking-form')
def booking():
    time = dao.load_time()
    return render_template('booking-form.html', time=time)

@app.route('/api/booking-form', methods=['post'])
@login_required
def add_booking():
    data = request.json
    desc = data.get('desc')
    date = data.get('date')
    time = data.get('time_id')
    print(time)
    try:
        b = dao.add_booking(desc=desc, date=date,time=time)
        print(time)
        print('KHONG LOI')
    except  Exception as e:
        print(str(e))
        return {'status': 404, 'err_msg': 'Chương trình đang bị lỗi'}

    return {'status': 201, 'booking': {
        'id' : b.id,
        'desc' : b.desc,
        'date' : b.booked_date,
        'time_id' : b.time_id
        }
    }


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
            else:
                return redirect('/admin')

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

@app.route('/nurse')
@login_required
def nurse():
    books = dao.load_booking()
    patient = dao.load_patient()
    return render_template('nurse.html', books=books,patient=patient, date = date.today())


@app.route('/api/check-patient-count')
def check_patient_count():
    patients_today = Books.query.filter_by(booked_date=date.today()).filter_by(lenLichKham=True).count()
    return jsonify({'patients_today': patients_today})

@app.route('/len-ds', methods=['post'])
def len_ds():
    data = request.json
    id = str(data.get('id'))
    dao.sms(id)
    dao.lenlichkham(id)
    return jsonify({"message": "Đã lên lịch khám cho bệnh nhân"})




if __name__ == '__main__':
    from app import admin
    app.run(debug=True)
