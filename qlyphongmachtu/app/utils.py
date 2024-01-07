from sqlalchemy import text, func, and_
from app.models import db, Patient, Books, Receipt, Prescription, ReceiptDetails,Medicine, \
    MedicalForm, Time, Cashier

from sqlalchemy.orm import aliased

def get_receipt():
    cashier_alias = aliased(Cashier)
    patient_alias = aliased(Patient)
    query = db.session.query(Receipt.id,Receipt.created_date,patient_alias.name,
        func.sum(Receipt.examines_price + Medicine.price * Prescription.quantity),cashier_alias.name)\
        .join(ReceiptDetails, Receipt.id == ReceiptDetails.receipt_id)\
        .join(Prescription, ReceiptDetails.prescription_id == Prescription.id)\
        .join(Medicine, Prescription.medicine_id == Medicine.id)\
        .join(patient_alias, Receipt.patient_id == patient_alias.id)\
        .join(cashier_alias, Receipt.cashier_id == cashier_alias.id)
    return query.group_by(Receipt.id).all()


def get_receipt_details():

    query = db.session.query(Medicine.id,Medicine.name, Prescription.quantity, func.sum(Prescription.quantity * Medicine.price))\
            .join(Prescription, Prescription.medicine_id == Medicine.id)\
            .join(ReceiptDetails, ReceiptDetails.prescription_id == Prescription.id)\
            .join(Receipt, Receipt.id == ReceiptDetails.receipt_id)
    return query.group_by(Medicine.id, Prescription.quantity).all()

