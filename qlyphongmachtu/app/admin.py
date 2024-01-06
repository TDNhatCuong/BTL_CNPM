from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose
from app import app, db
from app.models import Time, Medicine, Books, Cashier, Patient, MedicalForm, Doctor, Prescription, Receipt, ReceiptDetails, Rules, Administrator
from flask_login import logout_user, current_user
from flask import redirect


admin = Admin(app=app, name="QUẢN TRỊ PHÒNG MẠCH TƯ", template_mode="bootstrap4")


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

class AuthenticatedDoctor(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.type == 'doctor'

class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.type == 'administrator'

class AuthenticatedAdmin2(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.type == 'administrator'

class AuthenticatedPatient(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.type == 'patient'

class AuthenticatedNurse(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.type == 'nurse'

class AuthenticatedCashier(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.type == 'cashier'




class TimeView(AuthenticatedAdmin):
    can_export = True

class MedicineView(AuthenticatedAdmin, AuthenticatedDoctor):
    column_searchable_list = ['name']
    column_filters = ['price', 'name']
    can_export = True
    can_view_details = True


class BooksView(AuthenticatedNurse):                     #DS khám bệnh
    can_export = True
    column_list = ['id', 'patient', 'booked_date', 'time']
    #column_filters = ['patient_name']



class PatientView(AuthenticatedNurse):
    can_export = True
    column_list = ['name', 'gioiTinh', 'namSinh', 'diaChi']
    column_filters = ['gioiTinh', 'namSinh']
    column_searchable_list = ['name']

class DoctorView(AuthenticatedAdmin):
    column_list = ['name', 'ngayVaoLam']
    column_searchable_list = ['name']
    can_export = True


class MedicalFormView(AuthenticatedDoctor):
    column_list = ['patient', 'description', 'disease', 'date', 'doctor']


    # def _format_filter_value(self, value):
    #     patient = Patient.query.get(value)
    #     return patient.name if patient else None



class PrescriptionView(AuthenticatedDoctor):
    column_list = ['id', 'medicalForm', 'medicalForm.date', 'medicine', 'quantity', 'guide']


class ReceiptView(AuthenticatedCashier):
    column_list = ['patient', 'created_date', 'cashier']

class ReceiptDetailsView(AuthenticatedCashier):
    column_list = ['receipt', 'medicalForm', 'examines_price', 'medicine_price', 'total_price']


class CashierView(AuthenticatedAdmin):
    column_list = ['name']

class RulesView(AuthenticatedAdmin):
    column_list = ['administrator', 'change_date ', 'quantity_patient', 'examines_price']

class AdminView(AuthenticatedAdmin):
    column_list = ['name', 'joined_date']

class MyStatsView(AuthenticatedAdmin2):
    @expose("/")
    def index(self):
        return self.render('admin/stats.html')

class MyLogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


admin.add_view(TimeView(Time, db.session))
admin.add_view(MedicineView(Medicine, db.session))

admin.add_view(BooksView(Books, db.session))
admin.add_view(PatientView(Patient, db.session))
admin.add_view(DoctorView(Doctor, db.session))

admin.add_view(MedicalFormView(MedicalForm, db.session))
admin.add_view(PrescriptionView(Prescription, db.session))

admin.add_view(ReceiptView(Receipt, db.session))
admin.add_view(ReceiptDetailsView(ReceiptDetails, db.session))
admin.add_view(CashierView(Cashier, db.session))

admin.add_view(RulesView(Rules, db.session))
admin.add_view(AdminView(Administrator, db.session))


admin.add_view(MyStatsView(name='Thống kê báo cáo'))
admin.add_view(MyLogoutView(name='Đăng xuất'))