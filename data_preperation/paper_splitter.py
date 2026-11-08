import pymupdf
import utilities
import re
import os

def find_question_pages(pdf_path, exam_board, year):
    '''

    :param pdf_path: path to the pdf
    :param exam_board: used to check which phrase is used to identify the question page I.E edexcel
    it is ALWAYS page 2 and the page after the page with the phrase "Total for Question"
    :return:
    '''

    # EDEXCEL
    if exam_board == "edexcel":

        """
        Split a past-paper PDF into individual per-question PDF files.
        """

        # CONSTANTS
        MIN_X_PERCENT_FROM_LEFT = 0.09371
        MAX_X_PERCENT_FROM_LEFT = 0.89722
        MIN_Y_PERCENT_FROM_TOP = 0.053442
        FALLBACK_MAX_Y_PERCENT_FROM_TOP = 0.92

        LOOK_UP_PHRASE_NEW = "Total for Question"
        LOOK_UP_PHRASE_OLD = r"Total\s+for\s+Question\s+\d+\s+is\s+\d+\s+marks|Total.*marks"

        question_pages = [2]

        # Opening the pdf
        paper_doc = pymupdf.open(pdf_path)

        try:
            # Finds the pages with the LOOK_UP_PHRASE
            pages_with_phrase = utilities.page_locater(paper_doc, LOOK_UP_PHRASE_NEW, False)
            if len(pages_with_phrase) == 0:
                print("OLD PAPER OLD PAPER OLD PAPER")
                pages_with_phrase = utilities.page_locater(paper_doc, LOOK_UP_PHRASE_OLD, True)

            if len(pages_with_phrase) == 0:
                raise ValueError(f"No question-ending markers found in PDF: {pdf_path}")

            # Finds the question pages by adding 1 onto all the pages with the phrase as
            # after the end of a question there is usually a new question on the next page
            # apart from the last hence the - 1 in range
            for i in range(len(pages_with_phrase) - 1):
                next_question_page = pages_with_phrase[i] + 1

                if next_question_page <= len(paper_doc):
                    question_pages.append(next_question_page)

            # Remove duplicate pages while preserving order
            question_pages = list(dict.fromkeys(question_pages))

            # Get width and height of the paper
            temp = paper_doc[0]
            paper_doc_width = temp.rect.width
            paper_doc_height = temp.rect.height

            # Setting the constant bounds
            min_x_bound = paper_doc_width * MIN_X_PERCENT_FROM_LEFT
            max_x_bound = paper_doc_width * MAX_X_PERCENT_FROM_LEFT
            min_y_bound = paper_doc_height * MIN_Y_PERCENT_FROM_TOP
            fallback_max_y_bound = paper_doc_height * FALLBACK_MAX_Y_PERCENT_FROM_TOP

            os.makedirs("test", exist_ok=True)

            print(f"{pdf_path}: found question start pages {question_pages}")

            # 3 - Creating pdf files of the certain regions
            for i, question_page_number in enumerate(question_pages):
                source_page_index = question_page_number - 1
                source_page = paper_doc[source_page_index]

                # Search for writing lines on this page.
                # If none are found, use a safe lower crop bound instead of crashing.
                line_output = source_page.search_for("_")

                if line_output:
                    temp_max_y_bound = line_output[0].y0
                else:
                    temp_max_y_bound = fallback_max_y_bound
                    print(
                        f"Warning: no writing line found on page {question_page_number} "
                        f"in {pdf_path}; using fallback crop bound."
                    )

                if temp_max_y_bound <= min_y_bound:
                    temp_max_y_bound = fallback_max_y_bound

                # Create the rect
                question_area_rect = pymupdf.Rect(
                    min_x_bound,
                    min_y_bound,
                    max_x_bound,
                    temp_max_y_bound
                )

                # Create the new pdf
                temp_new_question_pdf = pymupdf.open()

                try:
                    # create new page
                    temp_new_page = temp_new_question_pdf.new_page(
                        width=question_area_rect.width,
                        height=question_area_rect.height
                    )

                    # Copy the question to the new page
                    temp_new_page.show_pdf_page(
                        temp_new_page.rect,
                        paper_doc,
                        source_page_index,
                        clip=question_area_rect
                    )

                    # Find Number of Marks
                    text_of_page = source_page.get_text()

                    marks = re.findall(r"\((\d{1,2})\)", text_of_page)
                    total_marks = sum(int(mark) for mark in marks)

                    temp_new_question_pdf.save(f"test/{total_marks}_{year}_Q{i + 1}.pdf")
                finally:
                    temp_new_question_pdf.close()

            print(f"20{year} HAS {len(question_pages)} QUESTIONS")

        finally:
            paper_doc.close()
