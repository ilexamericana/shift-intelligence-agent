# Shift Intelligence Agent

Prototype AI-assisted staffing recommendation tool built with Python and Streamlit.

## Overview
This project demonstrates how AI can support operational decision-making in security staffing by ranking guards for open shifts based on:

- Availability
- Required certification
- Overtime risk
- Experience level

## Problem
Scheduling decisions are often made quickly and manually, which can lead to:
- Missed certification requirements
- Increased overtime costs
- Inefficient staffing decisions

## Solution
This agent evaluates candidate guards against shift requirements and produces:
- A ranked list of candidates
- Clear explanations for each recommendation

## How it works
- Filters for required constraints (availability, certification)
- Applies weighted scoring (overtime risk, experience)
- Outputs ranked results with reasoning

## Tech Stack
- Python
- Streamlit

## Next Steps
- Integrate real scheduling data (e.g., WinTeam)
- Add licensing and compliance tracking
- Incorporate historical performance data
- Introduce learning-based optimization
## Demo

Run locally with:

```bash
streamlit run app.py
Then open http://localhost:8501 in your browser.
