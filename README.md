# Overview #
- Information on the engineering behind MyExamBuilder can be found here https://github.com/muhammadali-250408/myexambuilder-engineering
- MyExamBuilder is a website which allows A Level students to create unlimited, specfication aligned papers that are not purely random, it uses an equation of a curve to select the number of mark each question should be, the curve equation was derived after analysing the marks vs question number graphs of 53 International A Level Math past papers.
- Website: myexambuilder.co.uk
- Note: The API runs on a test server, after a few hours of no requests the server goes to sleep, and so paper generations could take up to several minutes to occur, however once activated typically takes a few seconds only.

## 2 Main Systems ##
It consists of 2 main systems, data preparation and paper generation. 
- **Data preparation**: The data pipeline used to turn regular past paper pdf's into individual question templates to be used in the paper generation.
- **Paper generation**: The system which involves generating the mark distribution of the paper, selecting questions to use based on number of marks, creating the dictionary of the paper which includes front cover and answer pages, generating the paper itself.

### How they interact ###
The data preparation outputs a directory called question_templates which contains all question pdf's in the final template form and can then be directly used by paper generation

# Data Preparation #
## Files ##
- main_hub.py
- paper_splitter.py
- question_template_maker.py
- question_topic_analyser.py
- utilities.py

## How to operate ##
Run main_hub.py it will show an interface like this:
```
WHAT TO DO
    >[A] EXTRACT QUESTIONS
    >[B] ASSIGN TOPICS
    >[C] CREATE PDF TEMPLATES
    >[D] ORGANISE QUESTIONS ON MARKS
>>> 
```

### Extract Questions ###
This will then show the interface: 
```
[A] EXTRACT FROM 1 PDF
[B] EXTRACT FROM A DIRECTORY
>>> 
```
Selecting either will prompt you to enter a path, relative to main_hub.py for where the past paper(s) you want to split are stored.
A will only do it to 1 paper
B will do it to all papers in the directory
  Note: The name of the pdf will be used to indicate the year, month and sitting of the paper i.e 24j2.pdf = 2024 june paper 2

This will run paper_splitter.find_question_pages either once or for every pdf in the directory depending on your selection and create a pdf for each question, selecting only the question area.
It will be stored in the directory /test once the python script is terminated.

To test this on a large scale try:
  1 - [A] Extract questions
  2 - [B] Extract from a directory
  3 - PATH >>> Assets/PDFs/papers
This will then analyse and extract all papers in that directory and save it in test/

### Assign Topics ###
This will show the interface:
```
ENTER PATH >>> 
```
- Enter the path of where the extracted questions are stored (if you did the test showed above put "test")
- Once this runs it will show:

```
ENTER STORE PATH >>> 
```
- This will be the directory where all the topic directories are stored (T1, T2... T12)
- It can be named anything
- You need to terminate the python process for the directories to be available
- You will see directories being outputted these are directories for each paper on the number of questions in that paper in those topics

### Create PDF templates ###
This will show the interface:
```
> ENTER QUESTION PATH >>> 
```
- The question path is the directory where the extracted questions are stored (if you followed the test inputs in Extract questions use test

- This will then show the interface:
```
> ENTER OUTPUT PATH>>> 
```
- This is the path where the question templates will be stored.
- A template is where the cropped question pdf extracted earlier is put onto my own answer line pdf to create a full A4 question page.
- Python process needs to be terminated for the template directory to be created.

### Organise questions on marks ###
- This is used to organise teh question into files based of the number of total marks it is worth.
- This was needed to make looking up questions with specific number of marks easier during the paper generation phase.
- Outputs a directory called test2 which contains other directories named after the corresponding number of marks (2,3,4...)

# Paper generation #
## Files ##
- main.py
- paper_array_generator.py
- paper_generator.py
- utilities.py
- test_generator.py

## How to operate ##
- Run the test_generator.py.
- It will ask for marks and difficulty:
    - Marks: Integer
    - Difficulty: Integer (1 - 3)
 It will output a pdf called TEST_GENERATION_PAPER.py
