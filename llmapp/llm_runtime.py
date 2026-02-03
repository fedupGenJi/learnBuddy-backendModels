import os
import json
import threading
from typing import Dict, Tuple, Any, Optional

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

BASE_MODEL = "Qwen/Qwen2.5-7B-Instruct"

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
ADAPTERS_DIR = os.path.join(PROJECT_ROOT, "adapters")

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE = torch.float16

tokenizer = None
model = None
loaded_adapters: Dict[str, str] = {}
loaded = False

adapter_lock = threading.Lock()


def list_adapter_folders(adapters_dir: str):
    if not os.path.isdir(adapters_dir):
        return []
    out = []
    for name in os.listdir(adapters_dir):
        p = os.path.join(adapters_dir, name)
        if os.path.isdir(p) and os.path.isfile(os.path.join(p, "adapter_config.json")):
            out.append(name)
    return sorted(out)


def load_base_and_adapters():
    global tokenizer, model, loaded_adapters, loaded

    if loaded:
        return

    if DEVICE != "cuda":
        raise RuntimeError("CUDA not available. This project is configured to load on GPU only.")

    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, use_fast=True)

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=DTYPE,
    )

    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        quantization_config=bnb_config,
        device_map={"": 0},
        attn_implementation="sdpa",
    )
    base_model.config.use_cache = False
    base_model.eval()

    model = base_model

    adapter_names = list_adapter_folders(ADAPTERS_DIR)
    for name in adapter_names:
        path = os.path.join(ADAPTERS_DIR, name)
        model.load_adapter(path, adapter_name=name)
        loaded_adapters[name] = path

    # move LoRA weights to cuda
    for n, p in model.named_parameters():
        if "lora_" in n and p.device.type != "cuda":
            p.data = p.data.to("cuda")

    if adapter_names:
        model.set_adapter(adapter_names[0])

    loaded = True


def extract_json(text: str) -> Tuple[Optional[Any], Optional[str]]:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None, "Could not find JSON braces in output."

    candidate = text[start:end+1].strip()
    try:
        return json.loads(candidate), None
    except Exception as e:
        return candidate, f"JSON parse error: {e}"


def _generate_text(prompt: str, max_new_tokens: int, temperature: float) -> str:
    global tokenizer, model

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=temperature,
            top_p=0.9,
        )
    return tokenizer.decode(out[0], skip_special_tokens=True)


def generate_with_adapter(adapter_name: str, prompt: str,
                          max_new_tokens: int = 450,
                          temperature: float = 0.3) -> str:
    """
    ✅ This is the safe entrypoint used by views:
    - It locks
    - sets adapter
    - generates
    - unlocks
    """
    global model, loaded_adapters

    if adapter_name not in loaded_adapters:
        raise ValueError(f"Adapter '{adapter_name}' is not loaded. Loaded: {list(loaded_adapters.keys())}")

    with adapter_lock:
        model.set_adapter(adapter_name)
        return _generate_text(prompt, max_new_tokens=max_new_tokens, temperature=temperature)