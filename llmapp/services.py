from typing import Any, Dict
from .llm_runtime import load_base_and_adapters, generate_with_adapter, extract_json
from .adapter_router import pick_adapter
from .prompts import prompt_generate_mcq, prompt_solve


def generate_mcq(chapter: str, difficulty: int) -> Dict[str, Any]:
    load_base_and_adapters()
    adapter = pick_adapter(chapter)

    prompt = prompt_generate_mcq(chapter, difficulty)

    raw = generate_with_adapter(
        adapter_name=adapter,
        prompt=prompt,
        max_new_tokens=450,
        temperature=0.6, 
    )

    data, err = extract_json(raw)
    return {"adapter": adapter, "data": data, "error": err, "raw": raw}


def solve(chapter: str, question: str) -> Dict[str, Any]:
    load_base_and_adapters()
    adapter = pick_adapter(chapter)

    prompt = prompt_solve(chapter, question)

    raw = generate_with_adapter(
        adapter_name=adapter,
        prompt=prompt,
        max_new_tokens=600,
        temperature=0.2, 
    )

    data, err = extract_json(raw)
    return {"adapter": adapter, "data": data, "error": err, "raw": raw}