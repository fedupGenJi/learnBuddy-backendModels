from typing import Any, Dict
from . import llm_runtime
from .llm_runtime import load_base_and_adapters, generate_with_adapter, extract_json
from .adapter_router import pick_adapter
from .prompts import prompt_generate_mcq, prompt_solve

def generate_mcq(chapter: str, difficulty: int) -> Dict[str, Any]:
    load_base_and_adapters()
    adapter = pick_adapter(chapter)

    tokenizer = llm_runtime.tokenizer
    assert tokenizer is not None, "Tokenizer not initialized"

    messages = [
        {
            "role": "system",
            "content": (
                "You are an NEB Grade 10 Mathematics question generator.\n"
                "You MUST output STRICT JSON ONLY.\n"
                "No markdown, no role labels, no extra text."
            ),
        },
        {
            "role": "user",
            "content": prompt_generate_mcq(chapter, difficulty),
        },
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    raw = generate_with_adapter(
        adapter_name=adapter,
        prompt=prompt,
        max_new_tokens=300,   # increase for more accurate
        temperature=0.6,
    )

    data, err = extract_json(raw)
    return {"adapter": adapter, "data": data, "error": err, "raw": raw}

def solve(chapter: str, question: str) -> Dict[str, Any]:
    load_base_and_adapters()
    adapter = pick_adapter(chapter)

    tokenizer = llm_runtime.tokenizer
    assert tokenizer is not None, "Tokenizer not initialized"

    messages = [
        {
            "role": "system",
            "content": (
                "You are an NEB Grade 10 Mathematics tutor.\n"
                "You MUST output STRICT JSON ONLY.\n"
                "No markdown, no role labels, no extra text."
            ),
        },
        {
            "role": "user",
            "content": prompt_solve(chapter, question),
        },
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    raw = generate_with_adapter(
        adapter_name=adapter,
        prompt=prompt,
        max_new_tokens=400,   # increase for more accurate
        temperature=0.2,
    )

    data, err = extract_json(raw)
    return {"adapter": adapter, "data": data, "error": err, "raw": raw}
