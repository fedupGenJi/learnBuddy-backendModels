import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .llm_runtime import load_base_and_adapters, loaded_adapters
from .services import generate_mcq as generate_mcq_service
from .services import solve as solve_service


def index(request):
    load_base_and_adapters()

    from . import llm_runtime
    device = str(llm_runtime.model.device) if llm_runtime.model else "not_loaded"

    return render(request, "index.html", {
        "device": device,
        "adapters": sorted(list(loaded_adapters.keys())),
    })


@csrf_exempt
def api_generate_mcq(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    chapter = payload.get("chapter")
    difficulty = payload.get("difficulty", 2)

    if not chapter:
        return JsonResponse({"error": "chapter is required"}, status=400)

    result = generate_mcq_service(chapter, int(difficulty))
    status = 200 if result["error"] is None else 502
    return JsonResponse(result, status=status)


@csrf_exempt
def api_solve(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    chapter = payload.get("chapter")
    question = payload.get("question")

    if not chapter or not question:
        return JsonResponse({"error": "chapter and question are required"}, status=400)

    result = solve_service(chapter, question)
    status = 200 if result["error"] is None else 502
    return JsonResponse(result, status=status)