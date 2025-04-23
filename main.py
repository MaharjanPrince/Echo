from fastapi import FastAPI, UploadFile, File, Form # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from fastapi.responses import HTMLResponse # type: ignore
from fastapi.staticfiles import StaticFiles # type: ignore
from pydantic import BaseModel # type: ignore
import uvicorn # type: ignore
import os

from backend.openai_utils import generate_reflection, answer_prompt
from backend.file_parser import extract_text_from_pdf
from backend.journal_writer import save_journal_entry

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #Allows requests from any frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#sets up the API app and allows it to be called from your frontend

# In-memory store for journal reflections (can be moved to DB later)
journal_memory = {}


# Route to serve the index.html
app.mount("/static", StaticFiles(directory="frontend", html = True), name = "frontend")
# #Serve static files(CSS and JS)
# app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("frontend/index.html", "r") as file:
        return HTMLResponse(content=file.read())


class Prompt(BaseModel):
    user_prompt: str
    book_id: str

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("frontend/index.html", "r") as file:
        return HTMLResponse(content=file.read())

@app.post("/upload-book/")
async def upload_book(file: UploadFile = File(...)): # Receives the uploaded PDF file
    """
    Endpoint to upload a PDF and generate a reflection for it.
    - Extracts text from the uploaded PDF.
    - Generates a reflection using OpenAI.
    - Saves the reflection in memory and returns a book ID.
    """
    contents = await file.read() # Reads it into memory with await file.read() 
    book_text = extract_text_from_pdf(contents) #function from file_parser Converts it to text using extract_text_from_pdf
    reflection = generate_reflection(book_text) #function form openai_utils Generates a philosophical reflection with generate_reflection from

    #use the filename as unique ID(without .pdf extension)
    book_id = file.filename.replace(".pdf", "")
    journal_memory[book_id] = reflection
    save_journal_entry(book_id, reflection) # Saves it permanently via save_journal_entry

    return {"message": "Book absorbed", "book_id": book_id}
# Stores that reflection in memory using the book's filename as the ID

#answer a user promp
@app.post("/ask")
async def ask_echo(prompt: Prompt):
    """
    Endpoint to handle user queries based on the absorbed book.
    - Takes a user prompt and generates a response using the book's reflection.
    """
    #Fetch the reflection store for the given book_id
    reflection = journal_memory.get(prompt.book_id, "")

    #Generate a response based on the users promp and the books reflection
    response = answer_prompt(prompt.user_prompt, reflection)

    return {"response": response}

# Fetches the book’s reflection from memory
# Sends both the reflection + user prompt to answer_prompt
# Returns the AI’s philosophical reply


#Runs the server
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
