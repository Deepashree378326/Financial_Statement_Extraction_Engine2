📊 Financial Research Portal: Structured Extraction Engine
Candidate: Deepashree

Target Role: AI Intern at Money Stories Finserve
Project Goal: Implement a specialized research tool for automated, high-precision financial data extraction.

🚀 Overview
This repository contains a minimal research portal slice designed to transform unstructured financial PDFs (Annual Reports, Earnings Statements) into structured, analyst-ready Excel/CSV files.
Unlike a generic chatbot, this tool uses Structured AI Outputs to ensure that data is extracted into a fixed schema, ready for immediate financial modeling and calculation.

🛠️ Tech Stack
Language: Python 3.10+
UI Framework: Streamlit
PDF Parsing: pdfplumber (optimized for tabular data extraction)
LLM Orchestration: Instructor (guarantees JSON output via Pydantic)
Model: GPT-4o / Gemini 1.5 Pro
Data Handling: Pandas (for CSV/Excel generation)

🏗️ Architecture
Ingestion: PDF is uploaded and parsed locally to preserve formatting.
Schema Enforcement: A Pydantic model defines the strict structure of an Income Statement.
Extraction: The LLM maps unstructured text to the defined schema.
Normalization: Currency, units, and labels are standardized.
Output: A downloadable .csv file is generated.

🎯 Handling the "Judgment Calls"
To meet the requirements of professional financial research, the following logic was implemented:
Numeric Accuracy (Anti-Hallucination): We utilize Source Grounding. Every extracted value is accompanied by the "Original Text" snippet from the PDF, allowing analysts to trace the source of every number.
Semantic Mapping: Using LLM reasoning, the tool automatically maps varied terminology (e.g., "Cost of Sales" vs "COGS") to a standardized line-item framework.
Missing Data: If a line item is not present in the document, the tool returns N/A rather than attempting to guess or hallucinate a value.
Currency/Units: The engine detects global document metadata to identify if figures are in Thousands, Millions, or different currencies ($, ₹, €).

