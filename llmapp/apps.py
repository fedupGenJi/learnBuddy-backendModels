import os
import threading
from django.apps import AppConfig

class LlmappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "llmapp"

    def ready(self):
        if os.environ.get("RUN_MAIN") != "true":
            return

        def _load():
            try:
                from .llm_runtime import load_base_and_adapters
                load_base_and_adapters()
            except Exception as e:
                print("[learnbuddy] Model auto-load failed:", e)

        threading.Thread(target=_load, daemon=True).start()