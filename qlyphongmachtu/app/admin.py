from datetime import date
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose
from app import app, db, dao
from app.models import Time, Medicine, Books, Cashier, Patient, MedicalForm, Doctor, Prescription, Receipt, ReceiptDetails, Rules, Administrator, Nurse
from flask_login import logout_user, current_user
from flask import redirect, request, jsonify
from app import utils


admin = Admin(app=app, name="QUẢN TRỊ PHÒNG MẠCH TƯ", template_mode="bootstrap4")


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

class AuthenticatedDoctor(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.type == 'doctor'

class AuthenticatedDoctor2(BaseView):
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

class AuthenticatedNurse2(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.type == 'nurse'

class AuthenticatedCashier(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.type == 'cashier'

class AuthenticatedCashierBV(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.type == 'cashier'




class PaymentView(AuthenticatedCashierBV):
    @expose("/")
    def index(self):
        kw = request.args.get('kw')
        patients = dao.load_patient(kw=kw)
        return self.render("admin/payment-cash.html", patients=patients)

class MedicineView(AuthenticatedAdmin, AuthenticatedDoctor):
    column_searchable_list = ['name']
    column_filters = ['price', 'name']
    can_export = True
    can_view_details = True


class BooksView(AuthenticatedNurse):                     #DS khám bệnh
    can_export = True
    column_list = ['id', 'patient', 'booked_date', 'time']


class PatientView(AuthenticatedNurse):
    can_export = True
    column_list = ['name', 'gioiTinh', 'namSinh', 'diaChi']
    column_filters = ['gioiTinh', 'namSinh']
    column_searchable_list = ['name']

# class AllBooksModelView(AuthenticatedNurse2):
#     @expose("/")
#     def index(self):
#         books = dao.load_book()
#         return self.render("admin/nurse.html", books=books)


class MedicalFormView(AuthenticatedDoctor):
    column_list = ['patient', 'description', 'disease', 'date', 'doctor']

# class AllMedicineModelView(AuthenticatedDoctor2):
#     @expose("/")
#     def index(self):
#         kw = request.args.get('kw')
#         medicine = dao.load_medicine(kw=kw)
#         return self.render("admin/medicine-list.html", medicine=medicine)

# class AllPatientModelView(AuthenticatedDoctor2):
#     @expose("/")
#     def index(self):
#         kw = request.args.get('kw')
#         patient = dao.load_patient(kw=kw)
#         book = dao.load_book()
#         return self.render("admin/patient-list.html", patient=patient, book=book, date=date.today())


class PrescriptionView(AuthenticatedDoctor):
    column_list = ['id', 'medicalForm', 'medicalForm.date', 'medicine', 'quantity', 'guide']


# class AllPhieuKhamView(AuthenticatedDoctor2):
#     @expose("/")
#     def index(self):
#         medicine = dao.load_medicine()
#         book = dao.load_book()
#         medicalForm = dao.load_medicalForm()
#         prescription = dao.load_prescription()
#         return self.render("admin/phieukham.html", medicine=medicine,book=book ,medicalForm=medicalForm, prescription=prescription)


# class AllDetailsModelView(AuthenticatedCashier):
#     @expose("/")
#     def index(self):
#         receipt = utils.get_receipt()
#         return self.render("admin/receipt-list.html", receipt=receipt)


class ReceiptDetailsView(AuthenticatedCashier):
    @expose("/")
    def index(self):
        receipt_details = utils.get_receipt_details()
        return self.render("admin/receipt-details.html", receipt_details=receipt_details)




class TimeView(AuthenticatedAdmin):
    can_export = True

class DoctorView(AuthenticatedAdmin):
    column_list = ['name', 'ngayVaoLam']
    column_searchable_list = ['name']
    can_export = True

class NurseView(AuthenticatedAdmin):
    column_list = ['name']
    can_export = True

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



# @app.route('/len-pk', methods=['post'])
# def len_pk(self):
#     data = request.json
#     id = str(data.get('id'))
#     b_id = dao.load_patient2(id)
#     return self.render("admin/patient-list.html", b_id=b_id)




admin.add_view(TimeView(Time, db.session))
admin.add_view(MedicineView(Medicine, db.session))

# admin.add_view(AllBooksModelView(name='Patient List Nurse'))
admin.add_view(BooksView(Books, db.session))
admin.add_view(PatientView(Patient, db.session))


# admin.add_view(AllPatientModelView(name='Patient List'))
# admin.add_view(AllMedicineModelView(name='Medicine List'))
# admin.add_view(AllPhieuKhamView(name='Lập Phiếu Khám'))

admin.add_view(MedicalFormView(MedicalForm, db.session))
admin.add_view(PrescriptionView(Prescription, db.session))


# admin.add_view(AllDetailsModelView(Receipt, db.session,name="Receipt", category="Receipt" ))
admin.add_view(ReceiptDetailsView(ReceiptDetails,  db.session,name="Receipt Details", category="Receipt"))
admin.add_view(PaymentView(name='Lập hóa đơn'))



admin.add_view(DoctorView(Doctor, db.session))
admin.add_view(NurseView(Nurse, db.session))
admin.add_view(CashierView(Cashier, db.session))
admin.add_view(RulesView(Rules, db.session))
admin.add_view(AdminView(Administrator, db.session))



admin.add_view(MyStatsView(name='Thống kê báo cáo'))
admin.add_view(MyLogoutView(name='Đăng xuất'))