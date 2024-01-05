from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose, AdminIndexView
from app import app, db
from app.models import Time, Medicine, Books, Cashier, Patient, MedicalForm, Doctor, Prescription, Receipt, ReceiptDetails, Rules, Administrator
# from wtforms.fields import DateField
# from wtforms.widgets import Input


admin = Admin(app=app, name="QUẢN TRỊ PHÒNG MẠCH TƯ", template_mode="bootstrap4")


class TimeView(ModelView):
    can_export = True

class MedicineView(ModelView):
    column_searchable_list = ['name']
    column_filters = ['price', 'name']
    can_export = True
    can_view_details = True


# class DateWithoutTimeField(DateField):
#     widget = Input()

class BooksView(ModelView):                     #DS khám bệnh
    can_export = True
    column_list = ['id', 'patient', 'booked_date', 'time']
    #column_filters = ['patient_name']

    # form_overrides = {
    #     'booked_date': DateWithoutTimeField
    # }

class PatientView(ModelView):
    can_export = True
    column_list = ['name', 'gioiTinh', 'namSinh', 'diaChi']
    column_filters = ['gioiTinh', 'namSinh']
    column_searchable_list = ['name']

class DoctorView(ModelView):
    column_list = ['name', 'ngayVaoLam']
    column_searchable_list = ['name']
    can_export = True


class MedicalFormView(ModelView):
    column_list = ['patient', 'description', 'disease', 'date', 'doctor']


    # def _format_filter_value(self, value):
    #     patient = Patient.query.get(value)
    #     return patient.name if patient else None



class PrescriptionView(ModelView):
    column_list = ['id', 'medicalForm', 'medicalForm.date', 'medicine', 'quantity', 'guide']


    #column_filters = ['medicalForm.date']
    # can_export = True


class ReceiptView(ModelView):
    column_list = ['patient', 'created_date', 'cashier']

class ReceiptDetailsView(ModelView):
    column_list = ['receipt', 'medicalForm', 'examines_price', 'medicine_price', 'total_price']


class CashierView(ModelView):
    column_list = ['name']

class RulesView(ModelView):
    column_list = ['administrator', 'change_date ', 'quantity_patient', 'examines_price']

class AdminView(ModelView):
    column_list = ['name', 'joined_date']

class MyStatsView(BaseView):
    @expose("/")
    def index(self):
        return self.render('admin/stats.html')




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
