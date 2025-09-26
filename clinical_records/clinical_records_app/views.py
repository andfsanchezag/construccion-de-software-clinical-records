from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Pet, ClinicalRecord
from django.http import JsonResponse
import json


# Create your views here.
def search_clinical_record(request):
    pets = Pet.objects.all()
    data = [
        {"pet_id" : pet.pet_id,
        "clinical_record" : pet.clinical_record}
        for pet in pets
    ]
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

        # Buscar mascota, si no existe se crea
        pet = Pet.objects(pet_id=pet_id).first()
        if not pet:
            
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
           # record.save()

            # Asociar historia clínica a la mascota
            pet.clinical_record = record
            pet = Pet(pet_id=pet_id)
            
            pet.save()

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
        pet.clinical_record = record
        pet.save()

        return JsonResponse({
            "status": "success",
            "message": "Historia clínica creada",
            "data": {
                "record_id": str(record.id),
                "pet_id": pet.pet_id
            }
        }, status=201)

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)