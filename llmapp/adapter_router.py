from .llm_runtime import loaded_adapters

def pick_adapter(chapter: str) -> str:
    key = " ".join(chapter.strip().lower().split())

    # desired adapter based on chapter keywords
    if "sequence" in key or "series" in key:
        preferred = "sequence_series_v1"
    elif "quadratic" in key:
        preferred = "quadratic_v1"
    elif "growth" in key or "depreciation" in key or "depr" in key:
        preferred = "growth_depr_v1"
    elif "arithmetic" in key or "interest" in key:
        preferred = "arithmetic_v1"
    elif "probability" in key:
        preferred = "probability_v1"
    elif "algebraic" in key or "algebra" in key or "equation" in key:
        preferred = "algebraic_fractions_v1"
    else:
        preferred = "arithmetic_v1"

    if preferred in loaded_adapters:
        return preferred

    if "arithmetic_v1" in loaded_adapters:
        return "arithmetic_v1"

    return next(iter(loaded_adapters.keys()))