# PDF Splitter by Beneficiary with Password Protection

Python automation for splitting a single PDF containing multiple reports into individual files per beneficiary, with automatic password protection.

## Overview

This project automates the process of handling consolidated PDF reports, commonly used in payroll or benefits distribution. Instead of manually separating each document, the script reads the PDF page by page, identifies the beneficiary and CPF, groups pages by beneficiary, generates individual PDF files, and applies password protection using the CPF.

## Technologies Used

Python 3.x  
pdfplumber for text extraction  
PyPDF2 for PDF manipulation and encryption  
re for pattern matching  
os and string for file handling  

## Input

A single PDF file containing multiple beneficiaries, such as Informes.pdf. Each page must contain the beneficiary name and CPF in a consistent format.

## Output

A folder named informes_separados containing individual PDF files for each beneficiary. Each file is named after the beneficiary and protected with a password based on their CPF (numbers only).

## How It Works

The script opens the PDF file and iterates through each page. It extracts the text and searches for CPF and beneficiary name patterns using regular expressions. Based on this information, it groups pages belonging to the same person. After grouping, it creates a new PDF for each beneficiary, adds the corresponding pages, applies password protection using the CPF, and saves the file in the output directory.

## How to Run

Install dependencies:

pip install pdfplumber PyPDF2

Place your input PDF in the project directory.

Update the file name in the script if needed:

arquivo_entrada = "Informes.pdf"

Run the script:

python script.py

## Project Structure

project/
│
├── script.py
├── Informes.pdf
└── informes_separados/

## Notes

The PDF must contain consistent patterns for CPF and beneficiary name. If the beneficiary name is not found, a fallback name will be used. File names are cleaned to remove invalid characters.

## Possible Improvements

Support for different document layouts  
User interface for easier usage  
Batch processing for multiple PDFs  
Integration with email systems for automatic delivery  
Logging and reporting features  

## Author

Filipe Mendes  
Focused on process automation and data solutions
