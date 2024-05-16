from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import LLMChain
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os
import csv


load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=api_key, temperature=0.5, verbose=True)

# pdf = './Chatbot/a.pdf'
def pdf_to_qa_text(pdf):
    # extracting pdf text
    pdf_reader = PdfReader(pdf)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()

    # split into chunks
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=2000,
        chunk_overlap=100,
        length_function=len
    )

    chunks = text_splitter.split_text(text)
    print(len(chunks))
    answer = ""
    count = 0
    for text in chunks:
        print(count)
        count += 1
        text = text
        template = '''
        You'll be provided with a text.

        Your task is to craft five unique medium-sized questions based on the given text. Answers can range from one line to descriptive.
        
        Your response should be structured to be put into a csv file having two headers one for question one for answer(dont give headers). 
        For example:
        
        Who wrote Mahābhārata?_,Sage Vyasa
        Question2_,Answer2
        Question3_,Answer3

        Question and answer should strictly be in same line. Each line for each pair
        % USER INPUT:
        
        {text}
        
        YOUR RESPONSE:
        
        '''
        
        prompt = PromptTemplate(
            input_variables=["text"],
            template=template
        )
        
        chain = LLMChain(llm=llm, prompt=prompt)
        dic = chain.invoke(text)
        # print(dic.get('text'))
        answer += dic.get('text')
        # print(answer)
    return answer


def append_text_to_csv(text, csv_file='./Chatbot/faqs.csv'):
    lines = text.strip().split('\n')
    # print(lines)

    with open(csv_file, 'a', newline='',encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['prompt', 'response'])

        for line in lines:
            
            if line != '' and '_,' in line[1:-2]:  # Check if the line is not blank
                question, answer = line.strip().split('_,', 1)  # Split once on the first occurrence of ","
                # print(question)
                # print(answer)
                writer.writerow({'prompt': question, 'response': answer})
        print('Added to csv')


# text_data = pdf_to_qa_text(pdf=pdf)
# print(text_data)
# print('#########')
# csv_file = './Chatbot/faqs.csv'

# append_text_to_csv(text_data, csv_file)



def list_pdf_files(folder_path=os.getcwd()):
    # Initialize an empty list to store PDF files
    pdf_files = []

    # Loop through all files in the folder
    for file in os.listdir(folder_path):
        # Check if the file has a .pdf extension
        if file.lower().endswith('.pdf'):
            # If yes, append the file name to the list
            pdf_files.append(file)

    # Return the list of PDF files
    return pdf_files
# print(list_pdf_files())


import csv

def read_csv_to_text(csv_file_path="faqs.csv"):
    """
    Reads an existing CSV file and returns all its content in a text variable.

    Args:
    - csv_file_path (str): The path to the CSV file.

    Returns:
    - text_content (str): The content of the CSV file as a text variable.
    """
    text_content = ""
    with open(csv_file_path, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            text_content += ', '.join(row) + '<br>'  # Assuming CSV values are comma-separated
    
    return text_content