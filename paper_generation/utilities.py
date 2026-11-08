import random
import math

def find_optimal_question_number_range(marks):
    return round(0.113*marks + 0.904) + random.randint(-2, 2)

def mark_per_question_formula(question_number, power):
    base = 14.5 - 9.5 * math.exp(-0.15 * question_number**1.3)
    return max(2, min(14, round(base + random.randint(-2, 2) * power)))