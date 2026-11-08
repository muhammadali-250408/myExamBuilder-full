import pymupdf
import os

def create_question_template(question_path, question_output_path, template_path, output_pdf_name):
    template = pymupdf.open(template_path)
    question_overlay = pymupdf.open(question_path)

    # Creating file jic
    os.makedirs(question_output_path, exist_ok=True)

    # Opening the specific page rather than just document
    template_page = template[0]
    question_overlay_page = question_overlay[0]

    # Question height and width
    height = question_overlay_page.rect.height
    width = question_overlay_page.rect.width

    # Position of it on screen
    target_rect = pymupdf.Rect(50, 20, 50+width, 20+height)

    # Putting the overlay on top of the template
    template_page.show_pdf_page(target_rect, question_overlay, 0)

    # Saving it
    template.save(f"{question_output_path}/{output_pdf_name}.pdf")