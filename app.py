import pandas as pd
import streamlit as st


st.set_page_config(page_title="Shift Intelligence Agent", page_icon="shield")


GUARDS = [
    {
        "name": "Ava Chen",
        "availability": "yes",
        "certification": "yes",
        "overtime_risk": "low",
        "experience": 6,
        "acceptance_rate": 92,
        "avg_response_minutes": 14,
        "site_experience": 11,
    },
    {
        "name": "Marcus Lee",
        "availability": "yes",
        "certification": "yes",
        "overtime_risk": "high",
        "experience": 9,
        "acceptance_rate": 78,
        "avg_response_minutes": 32,
        "site_experience": 6,
    },
    {
        "name": "Priya Shah",
        "availability": "yes",
        "certification": "no",
        "overtime_risk": "low",
        "experience": 7,
        "acceptance_rate": 88,
        "avg_response_minutes": 18,
        "site_experience": 9,
    },
    {
        "name": "Diego Ramirez",
        "availability": "no",
        "certification": "yes",
        "overtime_risk": "low",
        "experience": 8,
        "acceptance_rate": 96,
        "avg_response_minutes": 10,
        "site_experience": 14,
    },
    {
        "name": "Taylor Morgan",
        "availability": "yes",
        "certification": "yes",
        "overtime_risk": "low",
        "experience": 3,
        "acceptance_rate": 84,
        "avg_response_minutes": 12,
        "site_experience": 4,
    },
    {
        "name": "Jordan Patel",
        "availability": "yes",
        "certification": "yes",
        "overtime_risk": "high",
        "experience": 5,
        "acceptance_rate": 91,
        "avg_response_minutes": 22,
        "site_experience": 8,
    },
]


URGENCY_WEIGHTS = {
    "Normal": {
        "acceptance_rate": 0.35,
        "avg_response_minutes": 0.15,
        "site_experience": 0.25,
        "overtime_risk": 0.15,
        "experience": 0.10,
    },
    "Urgent": {
        "acceptance_rate": 0.25,
        "avg_response_minutes": 0.35,
        "site_experience": 0.15,
        "overtime_risk": 0.15,
        "experience": 0.10,
    },
    "Last-minute": {
        "acceptance_rate": 0.30,
        "avg_response_minutes": 0.35,
        "site_experience": 0.10,
        "overtime_risk": 0.15,
        "experience": 0.10,
    },
}


def normalize(value: int | float, highest_value: int | float) -> float:
    if highest_value == 0:
        return 0
    return value / highest_value


def build_flags(guard: dict, eligible: bool) -> list[str]:
    if not eligible:
        return ["Not eligible"]

    flags = []
    if guard["acceptance_rate"] >= 90 and guard["avg_response_minutes"] <= 15:
        flags.append("Strong fit")
    if guard["avg_response_minutes"] <= 15:
        flags.append("Fast responder")
    if guard["site_experience"] >= 8:
        flags.append("Knows site")
    if guard["acceptance_rate"] >= 90:
        flags.append("High acceptance")
    if guard["overtime_risk"] == "high":
        flags.append("Overtime caution")

    return flags or ["Standard fit"]


def get_action_label(eligible: bool, eligible_rank: int | None) -> str:
    if not eligible:
        return "Do not contact"
    if eligible_rank == 1:
        return "Contact first"
    if eligible_rank in [2, 3]:
        return "Contact next"
    return "Backup"


def rank_guards(
    guards: list[dict], certification_required: str, shift_urgency: str
) -> pd.DataFrame:
    rows = []
    weights = URGENCY_WEIGHTS[shift_urgency]
    max_response_minutes = max(guard["avg_response_minutes"] for guard in guards)
    max_site_experience = max(guard["site_experience"] for guard in guards)
    max_experience = max(guard["experience"] for guard in guards)

    for guard in guards:
        eligible = guard["availability"] == "yes"
        if certification_required == "yes":
            eligible = eligible and guard["certification"] == "yes"

        overtime_score = 1 if guard["overtime_risk"] == "low" else 0
        acceptance_score = guard["acceptance_rate"] / 100
        response_score = 1 - normalize(
            guard["avg_response_minutes"], max_response_minutes
        )
        site_score = normalize(guard["site_experience"], max_site_experience)
        experience_score = normalize(guard["experience"], max_experience)
        weighted_score = (
            acceptance_score * weights["acceptance_rate"]
            + response_score * weights["avg_response_minutes"]
            + site_score * weights["site_experience"]
            + overtime_score * weights["overtime_risk"]
            + experience_score * weights["experience"]
        )

        reasons = []
        if guard["availability"] == "yes":
            reasons.append("is available for the shift")
        else:
            reasons.append("is not available for the shift")

        if certification_required == "yes":
            if guard["certification"] == "yes":
                reasons.append("has the required certification")
            else:
                reasons.append("does not have the required certification")
        elif guard["certification"] == "yes":
            reasons.append("is certified, although certification is not required")
        else:
            reasons.append("certification is not required for this shift")

        reasons.append(
            f"historically accepts {guard['acceptance_rate']}% of offered shifts"
        )
        reasons.append(
            f"usually responds in {guard['avg_response_minutes']} minutes"
        )
        reasons.append(f"has worked this site {guard['site_experience']} times")

        if guard["overtime_risk"] == "low":
            reasons.append("has low overtime risk")
        else:
            reasons.append("has high overtime risk")

        reasons.append(f"has {guard['experience']} years of general experience")
        reasons.append(
            f"ranking for a {shift_urgency.lower()} shift emphasizes "
            f"{int(weights['acceptance_rate'] * 100)}% acceptance, "
            f"{int(weights['avg_response_minutes'] * 100)}% response speed, "
            f"{int(weights['site_experience'] * 100)}% site experience, "
            f"{int(weights['overtime_risk'] * 100)}% overtime risk, and "
            f"{int(weights['experience'] * 100)}% general experience"
        )

        flags = build_flags(guard, eligible)

        rows.append(
            {
                "Rank": None,
                "Action": None,
                "Name": guard["name"],
                "Available": guard["availability"],
                "Certified": guard["certification"],
                "Acceptance Rate": guard["acceptance_rate"],
                "Avg Response Minutes": guard["avg_response_minutes"],
                "Site Experience": guard["site_experience"],
                "Overtime Risk": guard["overtime_risk"],
                "Experience": guard["experience"],
                "Eligible": "yes" if eligible else "no",
                "Overtime Score": overtime_score,
                "Decision Score": round(weighted_score * 100, 1) if eligible else 0,
                "Flags": ", ".join(flags),
                "Explanation": "; ".join(reasons),
            }
        )

    ranked = pd.DataFrame(rows).sort_values(
        by=[
            "Eligible",
            "Decision Score",
            "Acceptance Rate",
            "Avg Response Minutes",
            "Site Experience",
            "Overtime Score",
            "Experience",
        ],
        ascending=[False, False, False, True, False, False, False],
    )
    ranked["Rank"] = range(1, len(ranked) + 1)

    eligible_rank = 0
    action_labels = []
    for guard in ranked.to_dict("records"):
        if guard["Eligible"] == "yes":
            eligible_rank += 1
            action_labels.append(get_action_label(True, eligible_rank))
        else:
            action_labels.append(get_action_label(False, None))
    ranked["Action"] = action_labels

    return ranked


st.title("Shift Intelligence Agent")
st.caption(
    "Ranks security guards for a shift based on eligibility, reliability, response speed, site familiarity, overtime risk, and experience."
)

st.sidebar.header("Shift Requirement")
certification_required = st.sidebar.radio(
    "Certification required?",
    ["yes", "no"],
    index=0,
    horizontal=True,
)
shift_urgency = st.sidebar.radio(
    "Shift urgency",
    ["Normal", "Urgent", "Last-minute"],
    index=0,
)

guards_df = pd.DataFrame(GUARDS)
ranked_guards = rank_guards(GUARDS, certification_required, shift_urgency)

st.subheader("Guard Dataset")
st.dataframe(guards_df, use_container_width=True, hide_index=True)

st.subheader("Ranked Guards")
st.dataframe(
    ranked_guards[
        [
            "Rank",
            "Action",
            "Name",
            "Eligible",
            "Flags",
            "Decision Score",
            "Available",
            "Certified",
            "Acceptance Rate",
            "Avg Response Minutes",
            "Site Experience",
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
        f"**{guard['Rank']}. {guard['Name']}** - {guard['Action']} ({status}). "
        f"Flags: {guard['Flags']}. {guard['Explanation']}."
    )
