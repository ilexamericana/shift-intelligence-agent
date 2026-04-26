import pandas as pd
import streamlit as st


st.set_page_config(page_title="Shift Intelligence Agent", page_icon="🛡️")


GUARDS = [
    {
        "name": "Ava Chen",
        "availability": "yes",
        "certification": "yes",
        "overtime_risk": "low",
        "experience": 6,
    },
    {
        "name": "Marcus Lee",
        "availability": "yes",
        "certification": "yes",
        "overtime_risk": "high",
        "experience": 9,
    },
    {
        "name": "Priya Shah",
        "availability": "yes",
        "certification": "no",
        "overtime_risk": "low",
        "experience": 7,
    },
    {
        "name": "Diego Ramirez",
        "availability": "no",
        "certification": "yes",
        "overtime_risk": "low",
        "experience": 8,
    },
    {
        "name": "Taylor Morgan",
        "availability": "yes",
        "certification": "yes",
        "overtime_risk": "low",
        "experience": 3,
    },
    {
        "name": "Jordan Patel",
        "availability": "yes",
        "certification": "yes",
        "overtime_risk": "high",
        "experience": 5,
    },
]


def rank_guards(guards: list[dict], certification_required: str) -> pd.DataFrame:
    rows = []

    for guard in guards:
        eligible = guard["availability"] == "yes"
        if certification_required == "yes":
            eligible = eligible and guard["certification"] == "yes"

        overtime_score = 1 if guard["overtime_risk"] == "low" else 0
        experience_score = guard["experience"]
        total_score = (overtime_score * 100) + experience_score

        reasons = []
        if guard["availability"] == "yes":
            reasons.append("available")
        else:
            reasons.append("not available")

        if certification_required == "yes":
            if guard["certification"] == "yes":
                reasons.append("has required certification")
            else:
                reasons.append("missing required certification")
        elif guard["certification"] == "yes":
            reasons.append("certified")
        else:
            reasons.append("certification not required")

        if guard["overtime_risk"] == "low":
            reasons.append("low overtime risk")
        else:
            reasons.append("high overtime risk")

        reasons.append(f"{guard['experience']} years of experience")

        rows.append(
            {
                "Rank": None,
                "Name": guard["name"],
                "Available": guard["availability"],
                "Certified": guard["certification"],
                "Overtime Risk": guard["overtime_risk"],
                "Experience": guard["experience"],
                "Eligible": "yes" if eligible else "no",
                "Score": total_score if eligible else -1,
                "Explanation": "; ".join(reasons),
            }
        )

    ranked = pd.DataFrame(rows).sort_values(
        by=["Eligible", "Score"], ascending=[False, False]
    )
    ranked["Rank"] = range(1, len(ranked) + 1)
    return ranked


st.title("Shift Intelligence Agent")
st.caption("Ranks security guards for a shift based on availability, certification, overtime risk, and experience.")

st.sidebar.header("Shift Requirement")
certification_required = st.sidebar.radio(
    "Certification required?",
    ["yes", "no"],
    index=0,
    horizontal=True,
)

guards_df = pd.DataFrame(GUARDS)
ranked_guards = rank_guards(GUARDS, certification_required)

st.subheader("Guard Dataset")
st.dataframe(guards_df, use_container_width=True, hide_index=True)

st.subheader("Ranked Guards")
st.dataframe(
    ranked_guards[
        [
            "Rank",
            "Name",
            "Eligible",
            "Available",
            "Certified",
            "Overtime Risk",
            "Experience",
            "Explanation",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)

st.subheader("Ranking Explanation")
for guard in ranked_guards.to_dict("records"):
    status = "Eligible" if guard["Eligible"] == "yes" else "Not eligible"
    st.markdown(
        f"**{guard['Rank']}. {guard['Name']}** — {status}. {guard['Explanation']}."
    )

