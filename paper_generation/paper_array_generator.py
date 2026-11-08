import random
import utilities
import os
import paper_generator


def generate_paper_array(criteria_dict):
    '''

    :param criteria_dict: {"MARKS": int, "DIFFICULTY": int(1->3)}
    :return: array of dicts
    '''

    # 1 - Extract data from criteria_dict
    marks = criteria_dict["MARKS"]
    difficulty = criteria_dict["DIFFICULTY"]

    # 2 - Find optimal question number range
    optimal_question_number = utilities.find_optimal_question_number_range(marks)

    # 3 - create paper array
    generated_paper_array = [{"type": "FRONT"}]
    question_marks_arr = []


    # 4 - Create array for all the question marks
    for i in range(optimal_question_number):
        if marks - sum(question_marks_arr) > utilities.mark_per_question_formula((i+1), 1):
            question_marks_arr.append(utilities.mark_per_question_formula((i+1), 1))
        elif marks - sum(question_marks_arr) > utilities.mark_per_question_formula((i+1), 0.5):
            question_marks_arr.append(utilities.mark_per_question_formula((i+1), 0.5))
        elif marks - sum(question_marks_arr) > utilities.mark_per_question_formula((i+1), 0.25):
            question_marks_arr.append(utilities.mark_per_question_formula((i+1), 0.25))
        elif marks - sum(question_marks_arr) > utilities.mark_per_question_formula((i+1), 0.1):
            question_marks_arr.append(utilities.mark_per_question_formula((i+1), 0.1))
        else:
            break

    # 5 - Create question pdf array
    question_pdf_arr = []
    for question_mark in question_marks_arr:
        files_with_that_mark = os.listdir(f"test2/{question_mark}")
        question_pdf_arr.append(random.choice(files_with_that_mark))

    print(question_pdf_arr)

    # CREATE THE PAPER ARRAY

    for index, question_pdf in enumerate(question_pdf_arr):
        mark = question_marks_arr[index]
        num_extra_pages = mark // 4
        generated_paper_array.append({"type": "QUESTION", "ID": question_pdf.split(".")[0]})

        for i in range(num_extra_pages-1):
            generated_paper_array.append({"type": "EXTRA"})
        generated_paper_array.append({"type": "EXTRA_END", "MARKS": mark})

    print(generated_paper_array)
    paper_bytes = paper_generator.generate_paper(generated_paper_array, f"example_paper")
    return paper_bytes


generate_paper_array({"MARKS": 100, "DIFFICULTY": 1})