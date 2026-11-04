# Semester 3 answer keys — Dr. Saurashtra University

Four complete question-and-answer books for B.Tech CSE. Each one carries the
previous-year paper analysis where papers were available, every question answered in full,
a formula and complexity revision sheet, and the errata found while verifying the answers.

| Subject | Code | Pages | Read in browser | Download the PDF |
|---|---|---|---|---|
| [DBMS](https://github.com/panditbhavik15/final-/blob/main/sources/DBMS_2BTCO302_PYQ_Answer_Key.md) | 2BTCO302 | 37 | [Markdown](https://github.com/panditbhavik15/final-/blob/main/sources/DBMS_2BTCO302_PYQ_Answer_Key.md) | [PDF](https://raw.githubusercontent.com/panditbhavik15/final-/main/DBMS_2BTCO302_PYQ_Answer_Key.pdf) · [open in a viewer](https://docs.google.com/gview?embedded=true&url=https%3A%2F%2Fraw.githubusercontent.com%2Fpanditbhavik15%2Ffinal-%2Fmain%2FDBMS_2BTCO302_PYQ_Answer_Key.pdf) |
| [OOP with C++](https://github.com/panditbhavik15/final-/blob/main/sources/OOP_Cpp_2BTCO303_PYQ_Answer_Key.md) | 2BTCO303 | 47 | [Markdown](https://github.com/panditbhavik15/final-/blob/main/sources/OOP_Cpp_2BTCO303_PYQ_Answer_Key.md) | [PDF](https://raw.githubusercontent.com/panditbhavik15/final-/main/OOP_Cpp_2BTCO303_PYQ_Answer_Key.pdf) · [open in a viewer](https://docs.google.com/gview?embedded=true&url=https%3A%2F%2Fraw.githubusercontent.com%2Fpanditbhavik15%2Ffinal-%2Fmain%2FOOP_Cpp_2BTCO303_PYQ_Answer_Key.pdf) |
| [Digital Fundamentals](https://github.com/panditbhavik15/final-/blob/main/sources/Digital_Fundamentals_2BTES301_PYQ_Answer_Key.md) | 2BTES301 | 53 | [Markdown](https://github.com/panditbhavik15/final-/blob/main/sources/Digital_Fundamentals_2BTES301_PYQ_Answer_Key.md) | [PDF](https://raw.githubusercontent.com/panditbhavik15/final-/main/Digital_Fundamentals_2BTES301_PYQ_Answer_Key.pdf) · [open in a viewer](https://docs.google.com/gview?embedded=true&url=https%3A%2F%2Fraw.githubusercontent.com%2Fpanditbhavik15%2Ffinal-%2Fmain%2FDigital_Fundamentals_2BTES301_PYQ_Answer_Key.pdf) |
| [Introduction to Data Structures](https://github.com/panditbhavik15/final-/blob/main/sources/Data_Structures_2BTCO301_Question_Bank_Answer_Key.md) | 2BTCO301 | 45 | [Markdown](https://github.com/panditbhavik15/final-/blob/main/sources/Data_Structures_2BTCO301_Question_Bank_Answer_Key.md) | [PDF](https://raw.githubusercontent.com/panditbhavik15/final-/main/Data_Structures_2BTCO301_Question_Bank_Answer_Key.pdf) · [open in a viewer](https://docs.google.com/gview?embedded=true&url=https%3A%2F%2Fraw.githubusercontent.com%2Fpanditbhavik15%2Ffinal-%2Fmain%2FData_Structures_2BTCO301_Question_Bank_Answer_Key.pdf) |

## Why the PDF looked broken

GitHub never previews a PDF on the file page. It tries to show the file as text, fails, and
prints *Unable to render code block*. The upload is fine — the page is the wrong tool.

Three ways that work:

1. **Read the Markdown** in `sources/`. GitHub renders it with headings, tables and code blocks,
   so it is the fastest way to study straight from the browser.
2. **Download the PDF** from the file page with the download icon, or open the raw link, which
   serves the file with the right content type.
3. **Open the PDF in a viewer** through the Google Docs viewer link in the table above. It renders
   the whole book inside a browser tab on phones and desktops alike.

## What is in each book

- **DBMS (2BTCO302)** — 37 pages. Previous-year papers analysed; every question with a model answer.
- **OOP with C++ (2BTCO303)** — 47 pages. Previous-year papers analysed; every question with a model answer and code.
- **Digital Fundamentals (2BTES301)** — 53 pages. Both previous-year papers analysed; assignment bank and revision sheet.
- **Introduction to Data Structures (2BTCO301)** — 45 pages. Unit-wise question bank built from the five unit notes (no PYQs were in that folder).

## Layout

```text
final-/
├── README.md
├── DBMS_2BTCO302_PYQ_Answer_Key.pdf
├── OOP_Cpp_2BTCO303_PYQ_Answer_Key.pdf
├── Digital_Fundamentals_2BTES301_PYQ_Answer_Key.pdf
├── Data_Structures_2BTCO301_Question_Bank_Answer_Key.pdf
├── sources/
│   ├── DBMS_2BTCO302_PYQ_Answer_Key.md
│   ├── OOP_Cpp_2BTCO303_PYQ_Answer_Key.md
│   ├── Digital_Fundamentals_2BTES301_PYQ_Answer_Key.md
│   └── Data_Structures_2BTCO301_Question_Bank_Answer_Key.md
└── code/
    ├── c/                     21 C programs from the Data Structures book
    ├── verify_ds.py           the engine that produces every quoted number
    ├── verification_ds.txt    its 557-line output, zero failing checks
    ├── run_c.py               writes and compiles the 21 C programs
    └── c_compile_check.txt    the 21/21 compile log
```

The PDFs are print-ready A4 with a proper monospace font, so the code listings stay aligned. The
Markdown files are the same content, editable and free to fork.

## Re-run the checks yourself

Nothing here asks you to trust a number. From a clone:

```bash
python code/verify_ds.py     # rewrites every worked answer; expect 557 lines, no False
python code/run_c.py         # needs clang on PATH, or set CLANG=/path/to/clang
```

`verify_ds.py` is pure standard-library Python — no installs. It re-runs the notes' own worked
examples (sparse-matrix counts, address arithmetic, K-map groupings, hash collision probes,
tree counts, sort traces, infix conversions) and prints a mismatch instead of hiding one.
`run_c.py` regenerates the 21 programs in `code/c/` and compiles each with
`clang -std=c99 -Wall -Wextra`.

## Data Structures note

The Data Structures Drive folder held only five unit notes and no previous-year papers, so that
book is a question bank derived from the syllabus and notes rather than a paper analysis. Its
exam pattern is borrowed from three real Semester 3 papers, not confirmed for 2BTCO301.

## Verified before publishing

- Every answer key was checked by an executable Python model; the Data Structures engine reports
  557 lines with zero failing checks.
- All 21 C programs compile clean under `-Wall -Wextra`. Device Guard blocks running freshly
  built executables on this machine, so printed output comes from the equivalent executed model.
- Each PDF was checked for page count, embedded fonts, missing strings and rendering artefacts.
