# NEB Grade 10 Math LLM Backend (Django + LoRA Adapters)

This project is a **Django backend** that serves a locally running **LLM fine-tuned with multiple LoRA adapters** for **NEB Grade 10 Mathematics** chapters.

It provides APIs to:

- Generate MCQs from a chapter  
- Solve chapter-specific math questions  
- Automatically route a question to the correct chapter adapter and solve it  

---

## Features

- Django REST-style API endpoints  
- LoRA adapter-based chapter specialization  
- Automatic chapter routing using a classifier adapter (`router_lora`)  
- JSON-only structured outputs for easy frontend integration  
- Built-in Postman-like API testing UI  

---

## Setup Instructions

### 1. Create and Activate Virtual Environment

```powershell
python -m venv venv
venv\Scripts\Activate
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Start the backend server

```powershell
./start.ps1
```
Output must be like:
Backend running at:
http://192.168.1.10:1234/

---

### API Testing Replica
At the homepage there is an webpage which lets you check the apis with desired inputs and let you see the output formats.

---

### APIs
/ -> Loads the base model and the adapters

POST/api/mcq -> Returns an question based on the chapter and the difficulty along with 4 options
Expected json:
{
  "chapter": "chapName",
  "difficulty": (1-5)
}

POST/api/solve -> Solves an question based on the chapter provided
Expected json:
{
  "chapter": "chapName",
  "question": "question for that chapter"
}

POST/api/solve_auto -> Solves an question among a available chapter
Expected json:
{
  "question": "question for a chapter"
}

---