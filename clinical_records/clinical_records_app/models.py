from mongoengine import (
    Document, StringField, IntField, ReferenceField,
    CASCADE, ValidationError, ListField
)

class ClinicalRecord(Document):
    veterinarian_id = IntField(required=True)
    motive = StringField(required=True)
    diagnostic = StringField(required=True)
    medical_procedure = StringField()
    medicine = StringField()
    dose = StringField()
    order_id = IntField()
    vaccination_history = StringField()
    allergies = StringField()
    procedure_details = StringField()
    cancellation = StringField()

    meta = {
        "collection": "clinical_records",
        "indexes": ["veterinarian_id", "order_id"]
    }

    def clean(self):
        if not self.motive and not self.diagnostic:
            raise ValidationError("Debe existir al menos motivo o diagnóstico")


class Pet(Document):
    clinical_records = ListField( 
        ReferenceField(ClinicalRecord, reverse_delete_rule=CASCADE)
    )

    meta = {
        "collection": "pets",
    }