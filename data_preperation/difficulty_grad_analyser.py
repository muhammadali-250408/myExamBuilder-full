import os
import re
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# SETTINGS
# ============================================================

FOLDER = "test"

# Expected:
# MARKS_YEAR_QNUMBER.pdf
#
# Examples:
# 4_2024_Q1.pdf
# 6_2024_Q2.pdf
# 8_2024_Q3.pdf


# ============================================================
# READ DATA FROM FILENAMES
# ============================================================

pattern = re.compile(
    r"^(\d+)_([^_]+)_Q(\d+)\.pdf$",
    re.IGNORECASE
)

data = []

for filename in os.listdir(FOLDER):

    match = pattern.match(filename)

    if not match:
        print(
            f"Skipping filename with unexpected format: {filename}"
        )
        continue

    marks = int(match.group(1))
    year = match.group(2)
    question_number = int(match.group(3))

    data.append({
        "marks": marks,
        "year": year,
        "question": question_number,
        "filename": filename
    })


# ============================================================
# CHECK DATA
# ============================================================

if not data:
    raise ValueError(
        "No matching PDF files were found."
    )

print(f"TOTAL FILES FOUND: {len(data)}")


# ============================================================
# GROUP BY YEAR
# ============================================================

years = sorted(
    set(row["year"] for row in data),
    key=lambda x: (
        int(re.sub(r"\D", "", x))
        if re.search(r"\d", x)
        else x
    )
)


# ============================================================
# CREATE GRAPH FOR EACH YEAR
# ============================================================

for year in years:

    year_data = [
        row
        for row in data
        if row["year"] == year
    ]

    # Sort questions numerically
    year_data.sort(
        key=lambda row: row["question"]
    )

    questions = np.array(
        [row["question"] for row in year_data],
        dtype=float
    )

    marks = np.array(
        [row["marks"] for row in year_data],
        dtype=float
    )


    # ========================================================
    # QUADRATIC BEST FIT
    # ========================================================

    if len(year_data) >= 3:

        coefficients = np.polyfit(
            questions,
            marks,
            2
        )

        polynomial = np.poly1d(
            coefficients
        )

        predicted = polynomial(
            questions
        )

        # R²
        ss_res = np.sum(
            (marks - predicted) ** 2
        )

        ss_tot = np.sum(
            (marks - np.mean(marks)) ** 2
        )

        if ss_tot != 0:
            r_squared = (
                1 -
                (ss_res / ss_tot)
            )
        else:
            r_squared = 0

    else:

        polynomial = None
        r_squared = np.nan


    # ========================================================
    # CREATE GRAPH
    # ========================================================

    plt.figure(
        figsize=(12, 7)
    )


    # --------------------------------------------------------
    # Actual data
    # --------------------------------------------------------

    plt.scatter(
        questions,
        marks,
        s=60,
        label="Actual marks"
    )


    # --------------------------------------------------------
    # Connect actual points
    # --------------------------------------------------------

    plt.plot(
        questions,
        marks,
        alpha=0.4
    )


    # --------------------------------------------------------
    # Curved line of best fit
    # --------------------------------------------------------

    if polynomial is not None:

        x_fit = np.linspace(
            questions.min(),
            questions.max(),
            300
        )

        y_fit = polynomial(
            x_fit
        )

        plt.plot(
            x_fit,
            y_fit,
            linestyle="--",
            linewidth=2,
            label=(
                f"Quadratic best fit "
                f"(R² = {r_squared:.3f})"
            )
        )


    # ========================================================
    # LABELS
    # ========================================================

    plt.title(
        f"{year} — Marks per Question",
        fontsize=16
    )

    plt.xlabel(
        "Question Number",
        fontsize=12
    )

    plt.ylabel(
        "Marks",
        fontsize=12
    )

    plt.xticks(
        questions.astype(int)
    )

    plt.grid(
        True,
        alpha=0.3
    )

    plt.legend()


    # ========================================================
    # DISPLAY STATISTICS
    # ========================================================

    if polynomial is not None:

        a, b, c = polynomial.coefficients

        equation = (
            f"y = {a:.4f}x² "
            f"+ {b:.4f}x "
            f"+ {c:.2f}"
        )

        stats_text = (
            f"Questions: {len(year_data)}\n"
            f"{equation}\n"
            f"R²: {r_squared:.4f}"
        )

        plt.text(
            0.02,
            0.97,
            stats_text,
            transform=plt.gca().transAxes,
            verticalalignment="top",
            bbox=dict(
                boxstyle="round",
                facecolor="white",
                alpha=0.8
            )
        )


    plt.tight_layout()


    # ========================================================
    # DISPLAY
    # ========================================================

    print(
        f"\n{year}: "
        f"{len(year_data)} questions"
    )

    if polynomial is not None:

        print(
            f"Quadratic: "
            f"y = {a:.4f}x² "
            f"+ {b:.4f}x "
            f"+ {c:.2f}"
        )

        print(
            f"R² = {r_squared:.4f}"
        )

    plt.show()