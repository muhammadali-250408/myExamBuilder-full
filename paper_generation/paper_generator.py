import pymupdf
import io
import random

# TEXT STYLE
FONTs = "hebo"        # Helvetica-Bold (built-in, closest to Arial Bold)
FONT_SIZE = 12
TEXT_COLOR = (0, 0, 0)

# FILE LOCATIONS
FRONT_PAGE_LOC = "Assets/ExamPaper/Templates/coverpage.pdf"
EXTRA_PAGE_LOC = "Assets/ExamPaper/Templates/answerpage.pdf"
QUESTION_DIR_LOC = "question_templates/"


def generate_paper(paper_dict, file_name):
    new_doc = pymupdf.open()
    question_number = 1


    # Looping through the dictionary

    for page in paper_dict:

        if page["type"] == "FRONT":
            add_front_page(new_doc)
            add_watermark(new_doc)

        elif page["type"] == "QUESTION":
            add_question_page(question_number, page["ID"], new_doc)
            question_number += 1
            add_watermark(new_doc)
        elif page["type"] == "EXTRA":
            add_extra_page(new_doc)
            add_watermark(new_doc)
        elif page["type"] == "EXTRA_END":
            add_extra_end_page(new_doc, page["MARKS"])

            add_watermark(new_doc)



    #new_doc.save(f"{file_name}.pdf")
    #new_doc.close()

    pdf_bytes = new_doc.tobytes()
    return pdf_bytes




def add_front_page(doc):
    src_front = pymupdf.open(FRONT_PAGE_LOC)
    doc.insert_pdf(src_front)
    src_front.close()
    print("== FRONT PAGE ADDED ==")


def add_question_page(question_number, question_id, doc):
    # Cover rect
    cover_rect = pymupdf.Rect(37, 27, 57, 127)

    # Adding queston page
    src_question = pymupdf.open(f"{QUESTION_DIR_LOC}{question_id}.pdf")
    doc.insert_pdf(src_question)

    # Getting page count
    page_count = doc.page_count

    # Adding cover rect
    doc[page_count-1].draw_rect(cover_rect, color=(252/255, 251/255, 249/255), fill=(252/255, 251/255, 249/255))

    # Adding text that says Question ...
    doc[page_count-1].insert_text((37, 67), f"{question_number}.", fontname=FONTs, fontsize=FONT_SIZE, color=TEXT_COLOR)

    # Clsoe the question
    src_question.close()

    print("== QUESTION PAGE ADDED ==")

def add_extra_page(doc):
    src_extra = pymupdf.open(EXTRA_PAGE_LOC)
    doc.insert_pdf(src_extra)
    src_extra.close()
    print("== EXTRA PAGE ADDED ==")

def add_extra_end_page(doc, marks):
    # Get the width and height of the page
    page_width = doc[0].rect.width
    page_height = doc[0].rect.height
    src_extra_end = pymupdf.open(EXTRA_PAGE_LOC)
    doc.insert_pdf(src_extra_end)
    src_extra_end.close()
    doc[doc.page_count-1].insert_text((page_width*0.73, page_height*0.91), f"Total Marks: {marks}", fontname=FONTs, fontsize=FONT_SIZE+4, color=TEXT_COLOR)

    print("== EXTRA END PAGE ADDED ==")

def add_watermark(doc):
    page_width = doc[0].rect.width
    page_height = doc[0].rect.height
    doc[-1].insert_text((page_width*0.23, page_height*0.91), f"Made with myexambuilder.co.uk", fontname=FONTs, fontsize=FONT_SIZE-2, color=TEXT_COLOR)