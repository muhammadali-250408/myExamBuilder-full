import pymupdf
import os
import re

'''
This file will have small modules that are used throughout the data preperation phase
'''

# Page Locater - Locates all pages in a pdf where a specific phase is
def page_locater(pdf, look_up_phrase, is_regex):


    page_number = 1
    pages_with_phrase = []


    if is_regex:
        print("REGEX")
        for page in pdf:
            output = page.get_text()
            print(output)

            search_result = re.search(look_up_phrase, output)

            if search_result:
                pages_with_phrase.append(page_number)

            page_number += 1

        return pages_with_phrase


    else:

        for page in pdf:
            output = page.search_for(look_up_phrase)

            if len(output) != 0:
                pages_with_phrase.append(page_number)#

            page_number += 1
        return pages_with_phrase


def txt_file_to_array(txt_path):
    file = open(txt_path, "r")
    text = file.read()
    the_array = text.split("\n")
    file.close()
    return the_array

def directory_num_files_finder(path):
    file_arr = os.listdir(path)
    return len(file_arr)

