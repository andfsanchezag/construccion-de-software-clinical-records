from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from bson import ObjectId
import json
from .models import Pet, ClinicalRecord


def search_clinical_record(request):
    pets = Pet.objects.all()
    data = []

    for pet in pets:
        records = []
        for record in pet.clinical_records:
            records.append({
                "record_id": str(record.id),
                "veterinarian_id": record.veterinarian_id,
                "motive": record.motive,
                "diagnostic": record.diagnostic,
                "medical_procedure": record.medical_procedure,
                "medicine": record.medicine,
                "dose": record.dose,
                "order_id": record.order_id,
                "vaccination_history": record.vaccination_history,
                "allergies": record.allergies,
                "procedure_details": record.procedure_details,
                "cancellation": record.cancellation,
            })

        data.append({
            "pet_id": str(pet.id),
            "clinical_records": records
        })

    return JsonResponse({"status": "success", "data": data}, safe=False)


@csrf_exempt
def create_clinical_record(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)

    try:
        body = json.loads(request.body.decode("utf-8"))
        pet_id = body.get("pet_id")

        if not pet_id:
            return JsonResponse({"status": "error", "message": "Falta el pet_id"}, status=400)

        # Buscar mascota
        try:
            pet_oid = ObjectId(pet_id)
        except InvalidId:
            return JsonResponse({"status": "error", "message": "Formato de pet_id inválido"}, status=400)

        # Buscar mascota
        pet = Pet.objects(id=pet_oid).first()
        if not pet:
            return JsonResponse({
                "status": "error",
                "message": "Mascota no encontrada"
            }, status=404)
        if not pet:
            return JsonResponse({
                "status": "error",
                "message": "Mascota no encontrada",
            }, status=404)

        # Crear historia clínica
        record = ClinicalRecord(
            veterinarian_id=body.get("veterinarian_id"),
            motive=body.get("motive"),
            diagnostic=body.get("diagnostic"),
            medical_procedure=body.get("medical_procedure"),
            medicine=body.get("medicine"),
            dose=body.get("dose"),
            order_id=body.get("order_id"),
            vaccination_history=body.get("vaccination_history"),
            allergies=body.get("allergies"),
            procedure_details=body.get("procedure_details"),
            cancellation=body.get("cancellation"),
        )
        record.save()

        # Asociar historia clínica a la mascota
        pet.clinical_records.append(record)
        pet.save()

        return JsonResponse({
            "status": "success",
            "message": "Historia clínica creada",
            "data": {
                "record_id": str(record.id),
                "pet_id": str(pet.id)
            }
        }, status=201)

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


@csrf_exempt
def create_pet(request):
    if request.method == "POST":
        try:
            # Crear mascota vacía
            pet = Pet()
            pet.save()

            return JsonResponse({
                "status": "success",
                "message": "Mascota creada sin historia clínica",
                "pet_id": str(pet.id)
            }, status=201)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)
