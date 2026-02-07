def prompt_generate_mcq(chapter: str, difficulty: int) -> str:
    return f"""
Task: generate_mcq
Chapter: {chapter}
Difficulty: {difficulty}

Rules:
- Create ONE NEB Grade 10 style word problem.
- Provide 4 options (A, B, C, D).
- Exactly ONE option is correct.
- The 3 wrong options must reflect common student mistakes.
- Include short rationales for each wrong option.

Return STRICT JSON ONLY with keys:
question, options, correct_option, answer_explanation, distractor_rationales, meta
""".strip()

def prompt_solve(chapter: str, question: str) -> str:
    return f"""
Task: solve
Chapter: {chapter}

Solve the following question.

Return STRICT JSON ONLY with keys:
given, to_find, steps, final_answer

Question:
{question}
""".strip()