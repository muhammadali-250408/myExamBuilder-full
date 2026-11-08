import paper_array_generator

marks = int(input("> MARKS >>> "))
difficulty = int(input("> DIFFICULTY >>> "))

pdf = paper_array_generator.generate_paper_array({
    "MARKS": marks,
    "DIFFICULTY": difficulty
})

with open("TEST_PAPER_GENERATED.pdf", "wb") as file:
    file.write(pdf)

print("PDF successfully generated!")
