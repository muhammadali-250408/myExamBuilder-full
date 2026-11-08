from os.path import exists

import question_topic_analyser
import os
import pymupdf
import paper_splitter
import time
import question_template_maker
import shutil

while True:
    user_input = input("WHAT TO DO\n    >[A] EXTRACT QUESTIONS\n    >[B] ASSIGN TOPICS\n    >[C] CREATE PDF TEMPLATES\n    >[D] ORGANISE QUESTIONS ON MARKS\n>>> ")

    if user_input == "A":

        user_input = input("[A] EXTRACT FROM 1 PDF\n[B] EXTRACT FROM A DIRECTORY\n>>> ")

        if user_input == "A":
            pdf_path = input("> PATH >>> ")
            paper_splitter.find_question_pages(pdf_path, "edexcel", 24)
        elif user_input == "B":
            pdf_path = input("> PATH >>> ")
            pdf_list = os.listdir(pdf_path)

            start_time = time.perf_counter()
            for i in range(len(pdf_list)):
                print(f"Processing {pdf_list}")
                split_pdf_list = []
                for paper in pdf_list:
                    split_pdf_list.append(paper.split(".")) # Outputs in the form [['year', 'pdf'], ...] i,e [['19', 'pdf']]

                temp_year = split_pdf_list[i][0]
                paper_splitter.find_question_pages(pdf_path + "/" + pdf_list[i], "edexcel", temp_year)
                print(f"CREATED 20{temp_year} PAPER"
                      f"")

            end_time = time.perf_counter()
            print(f"QUESTION GENERATION TIME: {end_time - start_time:.4f} seconds")



    elif user_input == "B":
        #CONSTS
        direcotry_path = input("> ENTER PATH >>> ")
        store_path = input("> ENTER STORE PATH >>> ")

        # Get File List
        pdf_list = os.listdir(direcotry_path)


        # Open each pdf file and put into the question topic analyser

        for file in pdf_list:

            temp_file = pymupdf.open(f"{direcotry_path}/{file}")
            temp_quest_topic = question_topic_analyser.analyse_topic(temp_file)


            print(store_path)
            for i in range(12):
                os.makedirs(f"{store_path}/T{i+1}", exist_ok=True)
            temp_file.save(f"{store_path}/T{temp_quest_topic}/{file}")

            temp_file.close()

    elif user_input == "C":
        question_path = input("> ENTER QUESTION PATH >>> ")
        question_full_output_path = input("> ENTER OUTPUT PATH>>> ")

        # Get all files in the directory as a list
        pdf_list = os.listdir(question_path)
        TEMPLATE_PATH = "Assets/PDFs/ExamPaper/Templates/questionpage.pdf"

        for file in pdf_list:
            # Params
            final_question_path = f"{question_path}/{file}"
            output_pdf_name = file.split(".")[0]


            question_template_maker.create_question_template(final_question_path, question_full_output_path, TEMPLATE_PATH, output_pdf_name)

    elif user_input == "D":
        paper_files = os.listdir("test")
        for file in paper_files:
            temp_mark = file.split("_")[0]

            os.makedirs(f"test2/{temp_mark}", exist_ok=True)
            shutil.move(f"test/{file}", f"test2//{temp_mark}/")
