import pymupdf
import os
import re
import utilities


def analyse_topic(question_pdf):
    # CONSTANTS
    TOPIC_TXT_PATH = "Assets/TextFiles/TopicWords"

    # Building the common-words dict and the strength dict
    number_of_topics = utilities.directory_num_files_finder(TOPIC_TXT_PATH)
    common_words_dict = {}
    topic_strength_dict = {}

    for i in range(number_of_topics):
        temp_txt_arr = utilities.txt_file_to_array(f"{TOPIC_TXT_PATH}/T{i+1}.txt")
        # lowercase the keyword list once, up front, so comparisons are apples-to-apples
        common_words_dict[f"T{i+1}"] = [w.lower() for w in temp_txt_arr]
        topic_strength_dict[f"T{i+1}"] = 0

    # 1 - Extract the text of the paper and tokenize properly
    raw_text = question_pdf[0].get_text()
    # split on ANY whitespace (space, tab, newline) instead of just " "
    # and strip punctuation so "graph," or "graph.\n" still matches "graph"
    words_in_question = re.findall(r"[a-zA-Z][a-zA-Z\-]*", raw_text.lower())

    # 2 - Loop through every word in the question, check against every topic
    for word in words_in_question:
        for topic, cmn_words in common_words_dict.items():
            if word in cmn_words:
                topic_strength_dict[topic] += 1

    # 3 - Also check for multi-word phrases (e.g. "chain rule", "partial fraction")
    # since a single-token loop above will never catch these
    joined_text = " ".join(words_in_question)
    for topic, cmn_words in common_words_dict.items():
        for phrase in cmn_words:
            if " " in phrase and phrase in joined_text:
                topic_strength_dict[topic] += 1

    print(topic_strength_dict)

    # 4 - Pick the strongest topic
    best_topic = max(topic_strength_dict, key=topic_strength_dict.get)
    return int(best_topic[1:])  # strip the "T" and return as int