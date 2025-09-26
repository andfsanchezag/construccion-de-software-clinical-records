from mongoengine import (
    Document, StringField, IntField, ReferenceField,
    CASCADE, ValidationError
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
 # este será el _id de Mongo
    pet_id = IntField(primary_key=True, required=True)
    clinical_record = ReferenceField(
        ClinicalRecord, reverse_delete_rule=CASCADE
    )

    meta = {
        "collection": "pets",
        "indexes": ["pet_id"]
    }
