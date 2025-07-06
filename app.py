
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import requests

st.set_page_config(page_title="AI Governance Engine - Turkey", layout="wide")

st.title("🇹🇷 Core AI Governance Engine - Prototype")
st.subheader("Simulating Policy Decisions for Turkey with Real-Time Data")

st.sidebar.header("Policy Simulation Settings")

# --- Real-Time Data Integration ---
def get_real_time_aqi():
    try:
        response = requests.get("https://api.waqi.info/feed/turkey/?token=demo")
        if response.status_code == 200:
            data = response.json()
            return data.get("data", {}).get("aqi", "Unavailable")
    except Exception:
        return "Unavailable"

aqi_value = get_real_time_aqi()
if isinstance(aqi_value, int):
    st.metric("🇹🇷 Current Air Quality Index (PM2.5)", f"{aqi_value}")
else:
    st.warning("Unable to fetch AQI data. Using default simulation values.")

# --- Policy Domains ---
domain = st.sidebar.selectbox("Select Policy Domain", [
    "Health", "Economy", "Education", "Energy", "Justice", "Budget Reallocation"
])

scenarios = {
    "Health": [
        "Increase Preventive Care Budget by 20%",
        "Subsidize Mental Health Services",
        "Reduce Hospital Wait Times by Hiring 5,000 New Staff"
    ],
    "Economy": [
        "Lower VAT by 2% on Essentials",
        "Increase Minimum Wage by 15%",
        "Launch Green Energy Tax Incentive"
    ],
    "Education": [
        "Implement AI-Powered Learning Tools",
        "Raise Teacher Salaries by 10%",
        "Provide Free University Tuition for STEM"
    ],
    "Energy": [
        "Expand Wind Energy Subsidies",
        "Implement Carbon Tax",
        "National Smart Grid Rollout"
    ],
    "Justice": [
        "Digitize Legal Proceedings",
        "Increase Legal Aid Access",
        "Establish AI Legal Review System"
    ],
    "Budget Reallocation": [
        "Defense→Health ₺100B",
        "Defense→Education ₺80B",
        "Defense→Environment ₺60B",
        "Defense→Welfare ₺50B"
    ]
}

scenario = st.sidebar.selectbox("Policy Scenario", scenarios[domain])

# --- Simulate Policy ---
def simulate_policy(scenario):
    np.random.seed(len(scenario))
    years = list(range(datetime.datetime.now().year, datetime.datetime.now().year + 10))
    long_term_impact = np.cumsum(np.random.normal(loc=0.5, scale=0.2, size=10)).tolist()

    if domain == "Budget Reallocation":
        mapping = {
            "Defense→Health ₺100B": {
                "Cost": 100,
                "Public Satisfaction (%)": 78,
                "Metric": "Lives Saved (Thousands)", "Value": 20
            },
            "Defense→Education ₺80B": {
                "Cost": 80,
                "Public Satisfaction (%)": 74,
                "Metric": "School Completion ↑ (%)", "Value": 5
            },
            "Defense→Environment ₺60B": {
                "Cost": 60,
                "Public Satisfaction (%)": 70,
                "Metric": "Air Quality Deaths ↓", "Value": 500
            },
            "Defense→Welfare ₺50B": {
                "Cost": 50,
                "Public Satisfaction (%)": 76,
                "Metric": "Child Poverty ↓ (%)", "Value": 3
            }
        }
        impact = mapping[scenario]
        impact["Estimated Cost (Billion TL)"] = impact["Cost"]
        impact["Long-Term Impact"] = pd.DataFrame({"Year": years, "Projected Index": long_term_impact})
        return impact

    impact = {
        "Impact Index Change (%)": np.random.uniform(1, 8),
        "Public Satisfaction (%)": np.random.uniform(60, 90),
        "Estimated Cost (Billion TL)": np.random.uniform(10, 60),
        "Regions Benefiting Most": np.random.choice([
            "Eastern Anatolia", "Marmara", "Aegean", "Southeastern Anatolia", "Central Anatolia"],
            size=2, replace=False
        ).tolist(),
        "Long-Term Impact": pd.DataFrame({"Year": years, "Projected Index": long_term_impact})
    }

    if domain == "Health" and isinstance(aqi_value, int):
        extra_impact = max(0, (aqi_value - 10) / 10)
        impact["Impact Index Change (%)"] += extra_impact
        impact["Explanation Note"] = f"Adjusted due to AQI impact factor (+{extra_impact:.2f})"

    return impact

# --- Show Results ---
if st.button("Simulate Policy Outcome"):
    results = simulate_policy(scenario)
    st.markdown(f"### 🧠 Policy Recommendation: {scenario}")
    st.write("#### Expected Outcomes:")

    if domain == "Budget Reallocation":
        st.metric(results["Metric"], f"{results['Value']}")
    else:
        st.metric("Impact Index Change (%)", f"{results['Impact Index Change (%)']:.2f}%")
        if "Regions Benefiting Most" in results:
            st.write("#### Regions Benefiting Most:", ", ".join(results["Regions Benefiting Most"]))

    st.metric("Public Satisfaction (%)", f"{results['Public Satisfaction (%)']:.2f}%")
    st.metric("Estimated Cost (Billion TL)", f"₺{results['Estimated Cost (Billion TL)']:.2f}B")

    st.markdown("#### 📊 Long-Term Impact Forecast:")
    st.line_chart(results["Long-Term Impact"].set_index("Year"))

    st.markdown("#### 🧭 Public Feedback Simulation:")
    feedback = st.slider("Public Approval of Policy (%)", min_value=0, max_value=100, value=int(results["Public Satisfaction (%)"]))
    st.write(f"Simulated Approval: {feedback}%")

    st.markdown("#### 🤖 Explanation:")
    st.markdown(results.get("Explanation Note", "This recommendation is based on simulated projections, budget reallocation models, and real-time environmental data."))

st.markdown("---")
st.caption("Proof of Concept – Not for Real-World Policy Deployment")
