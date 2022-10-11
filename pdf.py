import time
import csv
import streamlit as st
import os
from pdfminer.high_level import extract_text
import regex as re
import pandas as pd
import nltk

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
from tika import parser
from selenium import webdriver

def App1page(name, email, number, linkedin, github, summary, education, training, project, skills):
    st.write("**Name:**",name)
    st.write("")
    st.write("**Email:**",email)
    st.write("")
    st.write("**Number:**",number)
    st.write("")
    st.write("**Linkedin:**",linkedin)
    st.write("")
    st.write("**Github:**",github)
    st.write("")
    st.write("**Summary:**",summary)
    st.write("")
    st.write("**Education:**",education)
    st.write("")
    st.write("**Training:**",training)
    st.write("")
    st.write("**Project:**",project)
    st.write("")
    st.write("**Skills:**",skills)


    with st.empty():
        for seconds in range(11):
            st.write(f"After ⏳ {10-seconds} the data will be submitted automatically")
            time.sleep(1)
    return True


@st.cache
def convert_df(df):
   return df.to_csv().encode('utf-8')

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

        texts = extract_text_from_pdf(f'C:/Users/taksa/Desktop/Ez-Fillup/uploads/{pdf_file.name}')
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

        file = f'C:/Users/taksa/Desktop/Ez-Fillup/uploads/{pdf_file.name}'
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

        chromedriver_location = "chromedriver"
        global driver
        driver = webdriver.Chrome()
        driver.get('http://localhost:8501/')
        
        time.sleep(5)


        element = driver.find_element("xpath", "/html/body/div/div[1]/div[1]/div/div/div/section/div/div[1]/div/div[3]/div/div[1]/div/input")
        element.send_keys(dct['Name'])

        element = driver.find_element("xpath","/html/body/div/div[1]/div[1]/div/div/div/section/div/div[1]/div/div[4]/div/div[1]/div/input")
        element.send_keys(dct['Email'])

        element = driver.find_element("xpath",
                                      "/html/body/div/div[1]/div[1]/div/div/div/section/div/div[1]/div/div[5]/div/div[1]/div/input")
        element.send_keys(dct['Phone'])

        element = driver.find_element("xpath",
                                      "/html/body/div/div[1]/div[1]/div/div/div/section/div/div[1]/div/div[6]/div/div[1]/div/input")
        element.send_keys(dct['LinkedIn'])

        element = driver.find_element("xpath",
                                      "/html/body/div/div[1]/div[1]/div/div/div/section/div/div[1]/div/div[7]/div/div[1]/div/input")
        element.send_keys(dct['Github'])

        element = driver.find_element("xpath",
                                      "/html/body/div/div[1]/div[1]/div/div/div/section/div/div[1]/div/div[8]/div/div[1]/div/textarea")
        element.send_keys(dct['summary'])

        element = driver.find_element("xpath",
                                      "/html/body/div/div[1]/div[1]/div/div/div/section/div/div[1]/div/div[9]/div/div[1]/div/textarea")
        element.send_keys(dct['education'])

        element = driver.find_element("xpath",
                                      "/html/body/div/div[1]/div[1]/div/div/div/section/div/div[1]/div/div[10]/div/div[1]/div/textarea")
        element.send_keys(dct['trainings'])

        element = driver.find_element("xpath",
                                      "/html/body/div/div[1]/div[1]/div/div/div/section/div/div[1]/div/div[11]/div/div[1]/div/textarea")
        element.send_keys(dct['projects'])

        element = driver.find_element("xpath",
                                      "/html/body/div/div[1]/div[1]/div/div/div/section/div/div[1]/div/div[12]/div/div[1]/div/textarea")
        element.send_keys(dct['skills'])

        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        while True:
            time.sleep(1)

    st.title("Form")

    name = st.text_input(label="Name")
    email = st.text_input(label="Email ID")
    number = st.text_input(label="Mobile Number")
    linkedin = st.text_input(label="LinkedIn")
    github = st.text_input(label="Github")
    summary = st.text_area(label="Summary")
    education = st.text_area(label="Education")
    training = st.text_area(label="Training")
    project = st.text_area(label="Project")
    skills = st.text_area(label="Skills")

    import csv
    data = {
        "name": name,
        "email": email,
        "number": number,
        "linkedin": linkedin,
        "github": github,
        "summary": summary,
        "education": education,
        "training": training,
        "project": project,
        "skills": skills

    }
    new = pd.DataFrame(data, index=[0])
    csvs = convert_df(new)

    st.download_button(
            "Submit",
            csvs,
            "Resume Data.csv",
            "text/csv",
            key='download-csv'
        )

    submit = st.button("Display")
    try:
        if submit:
            with open('Database.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([name, email, number, linkedin, github, summary, education, training, project, skills])

            done = App1page(name, email, number, linkedin, github, summary, education, training, project, skills)
            if done:
                driver.quit()

    except:
        st.text('Please Enter Correct Details.\n **(Hint : Lookout for special characters and remove them.)**')


    for pdf in os.listdir("uploads"):
        print(pdf)
        os.remove(f'uploads/{pdf}')

    
    # if done:
    #     c = driver.window_handles[1]
    #     driver.close()