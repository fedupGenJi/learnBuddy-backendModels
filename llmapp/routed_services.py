import re
from typing import Dict, Any

from . import llm_runtime
from .llm_runtime import load_base_and_adapters, generate_with_adapter, extract_json
from .adapter_router import pick_adapter
from .prompts import prompt_solve 

VALID_LABELS = [
    "algebraic_fractions",
    "arithmetic",
    "growth_depreciation",
    "probability",
    "quadratic_equations",
    "sequence_series",
    "none",
]

def extract_label(raw: str) -> str:
    t = raw.strip().lower()
    t = re.sub(r"\s+", " ", t)

    for lab in VALID_LABELS:
        if t == lab:
            return lab
        
    for lab in VALID_LABELS:
        if lab in t:
            return lab

    return "none"

def route_question(question: str) -> str:
    load_base_and_adapters()

    tokenizer = llm_runtime.tokenizer
    assert tokenizer is not None, "Tokenizer not initialized"

    messages = [
        {
            "role": "system",
            "content": (
                "You are a routing classifier.\n"
                "Output ONLY one label from:\n\n"
                "algebraic_fractions,\n"
                "arithmetic,\n"
                "growth_depreciation,\n"
                "probability,\n"
                "quadratic_equations,\n"
                "sequence_series,\n"
                "none\n\n"
                "Rules:\n"
                "- Output exactly one label\n"
                "- No explanation\n"
                "- No punctuation"
            ),
        },
        {
            "role": "user",
            "content": question.strip(),
        },
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    raw = generate_with_adapter(
        adapter_name="router_lora",
        prompt=prompt,
        max_new_tokens=6,
        temperature=0.0,
    )

    return extract_label(raw)


def solve_routed(question: str) -> Dict[str, Any]:
    load_base_and_adapters()

    chapter = route_question(question)

    if chapter == "none":
        return {
            "routed_chapter": "none",
            "adapter": None,
            "data": None,
            "error": "Router could not classify this question into a valid chapter.",
            "raw": None,
        }

    adapter = pick_adapter(chapter)

    prompt = prompt_solve(chapter, question)

    raw = generate_with_adapter(
        adapter_name=adapter,
        prompt=prompt,
        max_new_tokens=400,
        temperature=0.2,
    )

    data, err = extract_json(raw)

    return {
        "routed_chapter": chapter,
        "adapter": adapter,
        "data": data,
        "error": err,
        "raw": raw,
    }
