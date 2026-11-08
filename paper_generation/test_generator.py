import paper_array_generator

marks = int(input("> MARKS >>> "))
difficulty = int(input("> DIFFICULTY >>> "))

pdf = paper_array_generator.generate_paper_array({
            "MARKS": marks,
            "DIFFICULTY": difficulty
        })