import subprocess
import sys
import time
import streamlit as st
import os
from pdfminer.high_level import extract_text
import regex as re
import PyPDF2
import requests
import json
import numpy as np
import pandas as pd
import nltk
from streamlit import web

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
from tika import parser
from selenium import webdriver

def upload_pdf():
    pdf_file = st.file_uploader("Upload PDF", type=["pdf"])

    if pdf_file is not None:
        file_details = {"filename": pdf_file.name, "filetype": pdf_file.type,
                        "filesize": pdf_file.size}

        with open(os.path.join("uploads", pdf_file.name), "wb") as f:
            f.write((pdf_file).getbuffer())

        st.success("File Uploaded")

    if pdf_file:
        def extract_text_from_pdf(pdf_path):
            return extract_text(pdf_path)

        texts = extract_text_from_pdf(f'C:/Users/Pranav/Desktop/Python Practs/ezfillup/uploads/{pdf_file.name}')
        texts = texts.lower().split('\n')
        for i in range(len(texts)):
            texts[i] = texts[i].strip()
        dct = {}
        dct['Name'] = " "
        dct['Role'] = " "
        dct['Email'] = " "
        dct['Phone'] = " "
        dct['LinkedIn'] = " "
        dct['Github'] = " "
        dct['Name'] = texts[0]
        dct['Role'] = texts[2]
        email_re = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_re = r'^(?:(?:\+|0{0,2})91?(\s)?(\s*[\-]\s*)?|[0]?)?([789]\d{4})?(\s*[\-]\s*)?(\d{5})'
        linkedin_re = r'([\w]+\.)?linkedin.com'
        git_re = r'([\w]+\.)?github.com'
        res_skills = []

        for text in texts:
            for split_text in text.split(' '):
                if (re.fullmatch(email_re, split_text)):
                    dct['Email'] = split_text
                if (re.fullmatch(phone_re, split_text)):
                    dct['Phone'] = split_text
                if (re.match(linkedin_re, split_text)):
                    dct['LinkedIn'] = split_text
                if (re.match(git_re, split_text)):
                    dct['Github'] = split_text

        file = f'C:/Users/Pranav/Desktop/Python Practs/ezfillup/uploads/{pdf_file.name}'
        file_data = parser.from_file(file)

        text = file_data['content']

        parsed_content = {}

        Keywords = ["education",
                    "summary",
                    "accomplishments",
                    "executive profile",
                    "professional profile",
                    "personal profile",
                    "work background",
                    "academic profile",
                    "other activities",
                    "qualifications",
                    "experience",
                    "interests",
                    "skills",
                    "achievements",
                    "publications",
                    "publication",
                    "certifications",
                    "workshops",
                    "projects",
                    "internships",
                    "trainings",
                    "hobbies",
                    "overview",
                    "objective",
                    "position of responsibility",
                    "jobs",
                    "e d u c a t i o n",
                    "s u m m a r y",
                    "a c c o m p l i s h m e n t s",
                    "e x e c u t i v e  p r o f i l e",
                    "p r o f e s s i o n a l  p r o f i l e",
                    "p e r s o n a l  p r o f i l e",
                    "w o r k  b a c k g r o u n d",
                    "a c a d e m i c  p r o f i l e",
                    "o t h e r  a c t i v i t i e s",
                    "q u a l i f i c a t i o n s",
                    "e x p e r i e n c e",
                    "i n t e r e s t s",
                    "s k i l l s",
                    "a c h i e v e m e n t s",
                    "p u b l i c a t i o n s",
                    "p u b l i c a t i o n",
                    "c e r t i f i c a t i o n s",
                    "w o r k s h o p s",
                    "p r o j e c t s",
                    "i n t e r n s h i p s",
                    "t r a i n i n g s",
                    "h o b b i e s",
                    "o v e r v i e w",
                    "objective",
                    "p o s i t i o n  o f  r e s p o n s i b i l i t y",
                    "j o b s"
                    ]

        for i in Keywords:
            dct[f'{i}'] = " "
        text = text.replace("\n", " ")
        text = text.replace("[^a-zA-Z0-9]", " ");
        # re.sub('\W+','', text)
        text = text.lower()

        content = {}
        indices = []
        keys = []
        for key in Keywords:
            try:
                content[key] = text[text.index(key) + len(key):]
                indices.append(text.index(key))
                keys.append(key)
            except:
                pass

        zipped_lists = zip(indices, keys)
        sorted_pairs = sorted(zipped_lists)
        sorted_pairs

        tuples = zip(*sorted_pairs)
        indices, keys = [list(tuple) for tuple in tuples]

        content = []
        for idx in range(len(indices)):
            if idx != len(indices) - 1:
                content.append(text[indices[idx]: indices[idx + 1]])
            else:
                content.append(text[indices[idx]:])

        for i in range(len(indices)):
            parsed_content[keys[i]] = content[i]

        new_dct = {}
        for i in parsed_content:
            s = (parsed_content[i]).split(" ", 1)
            dct[i] = (s[1:])[0]

        st.text(dct)

        chromedriver_location = "chromedriver"
        driver = webdriver.Chrome()
        driver.get('http://localhost:8501/')
        time.sleep(2)


        element = driver.find_element("xpath", "/html/body/div/div[1]/div[1]/div/div/div/section/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div[1]/div/input")
        element.send_keys(dct['Name'])

        element = driver.find_element("xpath","/html/body/div/div[1]/div[1]/div/div/div/section/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div[1]/div/input")
        element.send_keys(dct['Email'])

        element = driver.find_element("xpath",
                                      "/html/body/div/div[1]/div[1]/div/div/div/section/div/div[1]/div/div[3]/div[1]/div/div[3]/div/div[1]/div/input")
        element.send_keys(dct['Phone'])

        element = driver.find_element("xpath",
                                      "/html/body/div/div[1]/div[1]/div/div/div/section/div/div[1]/div/div[3]/div[1]/div/div[4]/div/div[1]/div/input")
        element.send_keys(dct['LinkedIn'])

        element = driver.find_element("xpath",
                                      "/html/body/div/div[1]/div[1]/div/div/div/section/div/div[1]/div/div[3]/div[1]/div/div[5]/div/div[1]/div/input")
        element.send_keys(dct['Github'])

        element = driver.find_element("xpath",
                                      "/html/body/div/div[1]/div[1]/div/div/div/section/div/div[1]/div/div[3]/div[1]/div/div[6]/div/div[1]/div/div/textarea")
        element.send_keys(dct['summary'])

        element = driver.find_element("xpath",
                                      "/html/body/div[1]/div[1]/div[1]/div/div/div/section/div/div[1]/div/div[3]/div[1]/div/div[7]/div/div[1]/div/div/textarea")
        element.send_keys(dct['education'])

        element = driver.find_element("xpath",
                                      "/html/body/div[1]/div[1]/div[1]/div/div/div/section/div/div[1]/div/div[3]/div[1]/div/div[8]/div/div[1]/div/div/textarea")
        element.send_keys(dct['trainings'])

        element = driver.find_element("xpath",
                                      "/html/body/div[1]/div[1]/div[1]/div/div/div/section/div/div[1]/div/div[3]/div[1]/div/div[9]/div/div[1]/div/div/textarea")
        element.send_keys(dct['projects'])

        element = driver.find_element("xpath",
                                      "/html/body/div[1]/div[1]/div[1]/div/div/div/section/div/div[1]/div/div[3]/div[1]/div/div[10]/div/div[1]/div/div/textarea")
        element.send_keys(dct['skills'])

        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        while True:
            time.sleep(1)

    st.title("Form")

    my_form = st.form(key="form1")
    name = my_form.text_input(label="Name")
    email = my_form.text_input(label="Email ID")
    number = my_form.text_input(label="Mobile Number")
    linkedin = my_form.text_input(label="LinkedIn")
    github = my_form.text_input(label="Github")
    summary = my_form.text_area(label="Summary")
    education = my_form.text_area(label="Education")
    training = my_form.text_area(label="Training")
    project = my_form.text_area(label="Project")
    skills = my_form.text_area(label="Skills")

    submit = my_form.form_submit_button('Submit')

    def run_cap():
        if submit:  # Make button a condition.
            on_click()
            st.text("Submitted Successfully")

    def on_click():
        subprocess.run([f"{sys.executable}", "pdf.py"])
    run_cap()
