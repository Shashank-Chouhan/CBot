from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile
import os
import application as backend
import functions as fn

app = FastAPI()

class UserInput(BaseModel):
    message: str
class Login(BaseModel):
    username: str
    password: str


# Allow requests from specific origins
origins = [
    "http://127.0.0.1:5500",  # Update this with your frontend URL
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
)

@app.post("/message")
async def send_message(user_input: UserInput):
    message = user_input.message
    response = backend.generate_response(message)
    
    return {"message": response}

@app.post("/login")
async def login(login: Login):
    username = login.username
    password = login.password
    # if user in db then msg = logged in successfully else try again
    msg = "fail"
    if username == 'admin' and password == 'admin123' :
        msg =  "success"
    return {"message": msg}


@app.post("/fileupload")
async def upload_file(file: UploadFile = File(...)):
    # Check if file is uploaded
    if not file:
        return {"message": "No file provided"}
    
    # Save the uploaded file to disk
    with open(file.filename, "wb") as f:
        f.write(await file.read())

    return {"message": "File uploaded successfully ", "filename": file.filename}


@app.get("/createdb")
async def create_database():
    list_of_pdfs_in_cwd = fn.list_pdf_files() #[a.pdf, b.pdf]

    for pdf in list_of_pdfs_in_cwd:
        text = fn.pdf_to_qa_text(pdf)
        print('text created')

        fn.append_text_to_csv(text, csv_file='faqs.csv')
        print('appended to csv')

        # delete that file here
        os.remove(pdf)

    return {"message": "Database created successfully"}

database = "This is database"#from csv file
@app.get("/showdb")
def show_database():
    database = fn.read_csv_to_text()
    return database