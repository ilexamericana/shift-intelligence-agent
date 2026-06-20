<img width="1589" height="983" alt="Screenshot SIA 06-2026" src="https://github.com/user-attachments/assets/5eb7bea0-ca24-4eae-a5e4-ff0090b163f3" />
# Shift Intelligence Agent

Shift Intelligence Agent is a workforce decision-support prototype that helps security operations teams fill open shifts by combining compliance requirements, site familiarity, historical acceptance behavior, response speed, overtime risk, and urgency-based ranking into an explainable recommendation engine. It helps scheduling managers compare available guards using practical operational signals and transparent recommendation logic.

The project is intentionally simple and explainable. It does not currently use machine learning, external APIs, or external databases. Compliance eligibility is incorporated as a decision gate, while automated compliance-expiry monitoring is planned as a future enhancement. The focus is on transparent recommendations that a manager can understand and act on quickly.

## Overview

The app ranks security guards for a selected site and shift urgency. It combines hard eligibility checks with weighted decision factors to produce a ranked list, contact recommendation, operational flags, and plain-language explanations.

Current sample sites:

- Edmonton Tower
- Stantec Tower
- AGLC

## Key Capabilities
All recommendations are accompanied by plain-language explanations so managers can understand why a candidate was recommended.

- Site-specific ranking based on how many times each guard has worked the selected site
- Urgency-based scoring for Normal, Urgent, and Last-minute shifts
- Historical acceptance rate to estimate likelihood of accepting the shift
- Average response time to prioritize faster responders when time matters
- Certification and availability checks before ranking eligible guards
- Overtime risk consideration to support practical staffing decisions
- Contact recommendations: Contact first, Contact next, Backup, or Do not contact
- Operational flags such as Strong fit, Fast responder, Knows site, High acceptance, Overtime caution, and Not eligible
- Plain-language explanations for each ranking

## How Ranking Works

The app first determines whether each guard is eligible:

- The guard must be available.
- If certification is required, the guard must be certified.

Eligible guards are then scored using weighted factors. The weights change based on shift urgency:

- Normal: emphasizes acceptance rate and site experience
- Urgent: emphasizes faster response time
- Last-minute: emphasizes response speed and acceptance rate while still preserving eligibility first

The selected site's experience value is used in ranking. For example, a guard may have strong experience at Edmonton Tower but little or no experience at AGLC, and the recommendation changes accordingly.

## Example Use Case

A scheduling manager needs to fill a last-minute certified shift at Stantec Tower. The manager selects:

- Site: Stantec Tower
- Certification required: yes
- Shift urgency: Last-minute

The app returns a ranked list of eligible guards, highlights who should be contacted first, and explains the recommendation using operational factors such as response speed, acceptance rate, and Stantec Tower experience.

Instead of manually comparing every guard, the manager can quickly see:

- Who is eligible
- Who is most likely to accept
- Who responds fastest
- Who already knows the site
- Who should be treated as a backup
- Who should not be contacted for this shift

## Application Screenshot

![Shift Intelligence Agent](Screenshot SIA 06-2026.png)

## Business Value

Scheduling decisions are often dependent on individual manager knowledge and memory.

This prototype demonstrates how operational expertise can be translated into a repeatable decision-support process that:

- Reduces time spent identifying shift candidates
- Improves consistency in staffing decisions
- Prioritizes compliance and eligibility requirements
- Highlights operational risks such as overtime exposure
- Provides explainable recommendations instead of black-box scoring

## Tech Stack

- Python
- Streamlit
- Pandas

## Running Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

## Future Roadmap

Potential next steps while keeping the tool simple and explainable:


- Add shift length and start time as decision inputs
- Add compliance expiry tracking and renewal alerts
- Add configurable scoring weights for scheduling managers
- Separate eligible, backup, and unavailable guards into clearer sections
- Add a small editable guard dataset inside the app for scenario testing
- Add exportable recommendation summaries for shift handoff notes
- Add simple fairness guardrails, such as showing recent assignment load, without introducing complex optimization
- Add comments or manager notes for why a final staffing decision was made

## Portfolio Note

This prototype demonstrates how operational decision-support tools can improve staffing workflows without requiring complex infrastructure. It is designed to show clear product thinking, practical ranking logic, and manager-friendly explanations in a lightweight Streamlit application.


