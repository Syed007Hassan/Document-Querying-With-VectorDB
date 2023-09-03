from config import baseUrl
import os
from flask import Flask, jsonify
import google.generativeai as palm
import requests
import json
import base64
import PyPDF2
import io
import pandas as pd
import chromadb
from chromadb.api.types import Documents, Embeddings
palm.configure(api_key='AIzaSyCiEx4VJELwnAjCmGfgZ4ovTKz50pIRJWQ')

promptPrefix = """
You are a chatbot integrated with an ERP system. You are here to help the user to reorder items.
Further you can help the user to get the vendor details for a particular item.
Also the user can create invoices by selecting either the company or individual. Then selecting the item and quantity.
Afterwards the user can create and download/print the invoice. 

"""

models = [m for m in palm.list_models(
) if 'embedText' in m.supported_generation_methods]
model = models[0]


text_models = [m for m in palm.list_models(
) if 'generateText' in m.supported_generation_methods]
text_model = text_models[0]


def embed_function(texts: Documents) -> Embeddings:
    # Embed the documents using any supported method
    return [palm.generate_embeddings(model=model, text=text)['embedding']
            for text in texts]


def create_chroma_db(documents, name):
    chroma_client = chromadb.Client()
    db = chroma_client.create_collection(
        name=name, embedding_function=embed_function)
    for i, d in enumerate(documents):
        db.add(
            documents=d,
            ids=str(i)
        )
    return db


def get_relevant_passage(query, db):
    passage = db.query(query_texts=[query], n_results=1)['documents'][0][0]
    return passage


# Perform embedding search
def make_prompt(query, relevant_passage):
    escaped = relevant_passage.replace(
        "'", "").replace('"', "").replace("\n", " ")
    prompt = ("""You are a helpful and informative bot that answers questions using text from the reference passage included below. \
  Be sure to respond in a complete sentence, being comprehensive, including all relevant background information. \
  However, you are talking to a non-technical audience, so be sure to break down complicated concepts and \
  strike a friendly and converstional tone. \
  If the passage is irrelevant to the answer, you may ignore it.
  QUESTION: '{query}'
  PASSAGE: '{relevant_passage}'

    ANSWER:
  """).format(query=query, relevant_passage=escaped)

    return prompt


def answer(model, query, db, temperature):
    passage = get_relevant_passage(query, db)
    prompt = make_prompt(query, passage)
    answer = palm.generate_text(prompt=prompt, model=model, candidate_count=3,
                                temperature=temperature, max_output_tokens=1024,)
    return answer.candidates[0]['output']


@staticmethod
def get_solutions(pdf_content, query):
    try:
        # Decode the base64-encoded PDF content
        pdf_content_dict = json.loads(pdf_content)
        pdf_content_encoded = pdf_content_dict['pdfContentEncoded']
        pdf_content_decoded = base64.b64decode(pdf_content_encoded)

        # Read the content of each page of the PDF and concatenate them into a single string
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content_decoded))
        pdf_content = ""
        for page in range(len(pdf_reader.pages)):
            pdf_content += pdf_reader.pages[page].extract_text()

        # pdf_content = pdf_reader.pages[0].extract_text()
        pdf_content = pdf_content[:6200]

        # Set up the DB
        db = create_chroma_db([pdf_content], "googlecardb")

        temperature = 0.65

        response = answer(text_model, query, db, temperature)

        print(response)

        # Return the concatenated text
        return response
    except Exception as e:
        print("Error generating response: " + str(e))
        return str(e)


def palm_create_response(prompt1: str):

    try:
        response = palm.generate_text(
            prompt=prompt1, max_output_tokens=800, temperature=0.7)
        print(response.result)
        return response.result
    except Exception as e:
        print("Error generating response: " + str(e))
        return "I am have issue with that. Is there any thing i can do..."


def palm_chat_response(prompt1: str):

    try:
        response = palm.generate_text(
            prompt=promptPrefix + prompt1, max_output_tokens=800, temperature=0.7)
        print(response.result)
        return response.result
    except Exception as e:
        print("Error generating response: " + str(e))
        return "I am have issue with that. Is there any thing i can do..."