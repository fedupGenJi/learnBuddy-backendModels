def prompt_generate_mcq(chapter: str, difficulty: int) -> str:
    return f"""SYSTEM:
You are an NEB Grade 10 Mathematics question generator for the chapter {chapter}.
Output MUST be STRICT JSON only. No markdown, no explanation outside JSON.

USER:
Task: generate_mcq
Chapter: {chapter}
Difficulty: {difficulty}
Rules:
- Create ONE NEB-style word problem from this chapter.
- Provide 4 options (A,B,C,D).
- Exactly ONE option is correct.
- The 3 wrong options must be based on common student mistakes.
- Include distractor mistake tags and short reasons.
Return JSON ONLY with keys:
question, options, correct_option, answer_explanation, distractor_rationales, meta
""".strip()


def prompt_solve(chapter: str, question: str) -> str:
    return f"""SYSTEM:
You are an NEB Grade 10 Mathematics tutor for the chapter {chapter}.
Output MUST be STRICT JSON only. No markdown, no extra text.

USER:
Task: solve
Show full steps and final answer in JSON.
Chapter: {chapter}
Question: {question}

Return JSON ONLY with keys:
given, to_find, steps, final_answer
""".strip()