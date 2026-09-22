import streamlit as st
import pandas as pd
import plotly.express as px
from textwrap import dedent

from calculator import (
    calculate_activity,
    get_activity_unit,
    ACTIVITY_TYPES,
    calculate_transport,
    calculate_electricity,
    calculate_total,
    calculate_breakdown
)

from services.database import (
    initialize_database,
    save_footprint,
    get_history,
    save_activity,
    get_activities,
    get_weekly_co2,
    set_weekly_target,
    get_weekly_target
)

from services.ai_coach import generate_ai_coach


# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="EcoTrack AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

initialize_database()


# ============================================================
# HTML HELPER
# ============================================================

def render_html(html):
    st.html(dedent(html))


# ============================================================
# CARBON SCORE
# ============================================================

def get_carbon_score(total):
    """
    Generate a simple 0-100 daily carbon score.

    Higher score = lower estimated footprint.
    """

    if total <= 5:
        return 95

    elif total <= 10:
        return 85

    elif total <= 15:
        return 75

    elif total <= 20:
        return 65

    elif total <= 30:
        return 50

    elif total <= 40:
        return 35

    else:
        return 20


# ============================================================
# PREMIUM CSS
# ============================================================

st.markdown(
    """
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap'
    );

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 10% 0%,
                rgba(34,197,94,0.10),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 0%,
                rgba(16,185,129,0.07),
                transparent 25%
            ),
            #07110d;

        color: #f4f8f5;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: #f4f8f5 !important;
    }

    h1 {
        font-size: 42px !important;
        letter-spacing: -1.5px;
    }

    h2 {
        font-size: 29px !important;
    }

    h3 {
        font-size: 20px !important;
    }

    /* ======================================================
       SIDEBAR
       ====================================================== */

    section[data-testid="stSidebar"] {
        background: #081610;
        border-right: 1px solid rgba(255,255,255,0.07);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }

    /* ======================================================
       HERO
       ====================================================== */

    .hero {
        position: relative;
        overflow: hidden;

        padding: 38px;

        border-radius: 26px;

        margin-bottom: 30px;

        background:
            linear-gradient(
                135deg,
                rgba(20,83,45,0.60),
                rgba(7,24,16,0.96)
            );

        border: 1px solid rgba(74,222,128,0.18);

        box-shadow:
            0 20px 70px rgba(0,0,0,0.25);
    }

    .hero-title {
        font-family: 'Space Grotesk', sans-serif;

        font-size: 46px;
        line-height: 1.05;

        font-weight: 700;

        letter-spacing: -2px;

        margin-top: 18px;

        color: #f4f8f5;
    }

    .hero-subtitle {
        color: #a8bcb1;

        font-size: 17px;

        max-width: 720px;

        line-height: 1.6;

        margin-top: 12px;
    }

    .badge {
        display: inline-block;

        padding: 7px 13px;

        border-radius: 999px;

        background:
            rgba(74,222,128,0.10);

        border:
            1px solid rgba(74,222,128,0.20);

        color: #86efac;

        font-size: 11px;

        font-weight: 700;

        letter-spacing: 0.7px;
    }

    /* ======================================================
       KPI
       ====================================================== */

    .kpi {
        padding: 22px;

        min-height: 130px;

        border-radius: 19px;

        background:
            linear-gradient(
                145deg,
                rgba(20,37,28,0.96),
                rgba(10,23,17,0.96)
            );

        border:
            1px solid rgba(255,255,255,0.07);

        box-shadow:
            0 10px 30px rgba(0,0,0,0.12);
    }

    .kpi-label {
        color: #81978c;

        font-size: 11px;

        font-weight: 700;

        letter-spacing: 0.8px;
    }

    .kpi-value {
        font-family: 'Space Grotesk', sans-serif;

        color: #f3f8f4;

        font-size: 31px;

        font-weight: 700;

        margin-top: 9px;
    }

    .kpi-desc {
        color: #71867b;

        font-size: 12px;

        margin-top: 4px;
    }

    /* ======================================================
       PANEL
       ====================================================== */

    .panel {
        padding: 24px;

        border-radius: 20px;

        background:
            rgba(12,27,20,0.90);

        border:
            1px solid rgba(255,255,255,0.065);
    }

    /* ======================================================
       SCORE
       ====================================================== */

    .score-number {
        font-family: 'Space Grotesk', sans-serif;

        font-size: 68px;

        font-weight: 700;

        line-height: 1;
    }

    .score-track {
        width: 100%;

        height: 8px;

        background: #172820;

        border-radius: 20px;

        overflow: hidden;

        margin-top: 18px;
    }

    .score-fill {
        height: 100%;

        border-radius: 20px;
    }

    /* ======================================================
       INPUTS
       ====================================================== */

    .stSelectbox > div > div,
    .stNumberInput > div > div {
        background: #0d1c15 !important;

        border-color:
            rgba(255,255,255,0.10) !important;

        border-radius: 12px !important;
    }

    /* ======================================================
       BUTTON
       ====================================================== */

    .stButton > button {

        min-height: 46px;

        border-radius: 12px;

        border:
            1px solid rgba(74,222,128,0.25);

        background:
            linear-gradient(
                135deg,
                #16a34a,
                #15803d
            );

        color: white;

        font-weight: 700;

        transition:
            all 0.2s ease;
    }

    .stButton > button:hover {

        border-color: #4ade80;

        box-shadow:
            0 10px 30px rgba(34,197,94,0.20);

        transform:
            translateY(-1px);
    }

    /* ======================================================
       METRICS
       ====================================================== */

    div[data-testid="stMetric"] {

        background:
            rgba(15,31,23,0.85);

        padding: 18px;

        border-radius: 16px;

        border:
            1px solid rgba(255,255,255,0.06);
    }

    div[data-testid="stMetricLabel"] {
        color: #8fa69a !important;
    }

    div[data-testid="stMetricValue"] {

        color: #f3f8f4 !important;

        font-family:
            'Space Grotesk', sans-serif;
    }

    hr {
        border-color:
            rgba(255,255,255,0.07);
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background:
            transparent !important;
    }


    .activity-card {
        padding: 20px;
        border-radius: 18px;
        background: rgba(12,27,20,0.90);
        border: 1px solid rgba(255,255,255,0.065);
    }

    .target-progress {
        height: 12px;
        background: #172820;
        border-radius: 20px;
        overflow: hidden;
        margin-top: 14px;
    }

    .target-fill {
        height: 100%;
        border-radius: 20px;
        transition: width 0.3s ease;
    }

    /* ======================================================
       MOBILE
       ====================================================== */

    @media (max-width: 768px) {

        .hero {
            padding: 25px;
        }

        .hero-title {
            font-size: 34px;
        }

        h1 {
            font-size: 32px !important;
        }

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    render_html(
        """
        <div style="
            font-family:'Space Grotesk',sans-serif;
            font-size:26px;
            font-weight:700;
            color:#f4f8f5;
        ">
            🌱 EcoTrack
        </div>

        <div style="
            color:#71867b;
            font-size:13px;
            margin-top:5px;
            margin-bottom:28px;
        ">
            AI-powered climate intelligence
        </div>
        """
    )

    render_html(
        """
        <div style="
            color:#71867b;
            font-size:11px;
            font-weight:700;
            letter-spacing:1px;
            margin-bottom:10px;
        ">
            WORKSPACE
        </div>
        """
    )

    page = st.radio(
        "Navigation",
        [
            "🏠 Overview",
            "📊 Analytics",
            "🔮 What-If Lab",
            "📜 History"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    render_html(
        """
        <div style="
            padding:17px;
            border-radius:15px;
            background:rgba(74,222,128,0.055);
            border:1px solid rgba(74,222,128,0.10);
        ">

            <div style="
                color:#71867b;
                font-size:10px;
                font-weight:700;
                letter-spacing:1px;
            ">
                YOUR MISSION
            </div>

            <div style="
                margin-top:8px;
                color:#d9e7df;
                font-size:14px;
                line-height:1.5;
            ">
                Make one better choice every day. 🌍
            </div>

        </div>
        """
    )


# ============================================================
# HERO FUNCTION
# ============================================================

def show_hero(
    badge,
    title,
    subtitle
):

    render_html(
        f"""
        <div class="hero">

            <span class="badge">
                {badge}
            </span>

            <div class="hero-title">
                {title}
            </div>

            <div class="hero-subtitle">
                {subtitle}
            </div>

        </div>
        """
    )


# ============================================================
# OVERVIEW
# ============================================================

if page == "🏠 Overview":

    show_hero(
        "● CLIMATE INTELLIGENCE PLATFORM",
        "Understand your impact.",
        "Track everyday choices, discover your biggest emissions, "
        "and simulate a cleaner lifestyle."
    )

    st.header("Your Daily Footprint")

    st.caption(
        "Adjust your activities and see your estimated impact instantly."
    )

    # --------------------------------------------------------
    # MOBILITY
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 🚗 Mobility")

        vehicle = st.selectbox(
            "Primary transport",
            [
                "car_petrol",
                "car_diesel",
                "motorcycle",
                "bus",
                "train"
            ],
            format_func=lambda x: {
                "car_petrol": "🚗 Petrol Car",
                "car_diesel": "🚙 Diesel Car",
                "motorcycle": "🏍️ Motorcycle",
                "bus": "🚌 Bus",
                "train": "🚆 Train"
            }[x]
        )

        distance = st.slider(
            "Daily distance (km)",
            0.0,
            300.0,
            10.0,
            1.0
        )

    # --------------------------------------------------------
    # ENERGY
    # --------------------------------------------------------

    with col2:

        st.markdown("### ⚡ Energy")

        electricity = st.slider(
            "Daily electricity consumption (kWh)",
            0.0,
            100.0,
            5.0,
            1.0
        )

        st.caption(
            "Estimated daily household electricity usage."
        )

    # --------------------------------------------------------
    # LIFESTYLE
    # --------------------------------------------------------

    st.markdown("### 🌍 Lifestyle")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        food = st.number_input(
            "🍔 Food",
            min_value=0.0,
            value=2.0,
            step=0.5
        )

    with c2:

        flight = st.number_input(
            "✈️ Flights",
            min_value=0.0,
            value=0.0,
            step=1.0
        )

    with c3:

        shopping = st.number_input(
            "🛍️ Shopping",
            min_value=0.0,
            value=1.0,
            step=0.5
        )

    with c4:

        waste = st.number_input(
            "🗑️ Waste",
            min_value=0.0,
            value=0.5,
            step=0.5
        )

    # --------------------------------------------------------
    # CALCULATIONS
    # --------------------------------------------------------

    transport_emission = calculate_transport(
        distance,
        vehicle
    )

    electricity_emission = calculate_electricity(
        electricity
    )

    total = calculate_total(
        transport=transport_emission,
        electricity=electricity_emission,
        food=food,
        flight=flight,
        shopping=shopping,
        waste=waste
    )

    breakdown = calculate_breakdown(
        transport=transport_emission,
        electricity=electricity_emission,
        food=food,
        flight=flight,
        shopping=shopping,
        waste=waste
    )

    # ========================================================
    # LOG ACTIVITY
    # ========================================================

    st.divider()
    st.markdown("### ➕ Log an Activity")
    st.caption(
        "Record one activity. EcoTrack calculates CO₂e using the "
        "hackathon's fixed emission factors."
    )

    log_col1, log_col2, log_col3 = st.columns([1.2, 1, 0.8])

    with log_col1:
        activity_type = st.selectbox(
            "Activity type",
            list(ACTIVITY_TYPES.keys()),
            format_func=lambda x: {
                "car": "🚗 Car travel",
                "bus": "🚌 Bus travel",
                "flight": "✈️ Flight",
                "electricity": "⚡ Electricity",
                "veg_meal": "🥗 Veg meal",
                "non_veg_meal": "🍗 Non-veg meal"
            }[x],
            key="activity_type"
        )

    activity_unit = get_activity_unit(activity_type)

    with log_col2:
        if activity_unit == "km":
            max_quantity = 1000.0
            default_quantity = 10.0
            quantity_label = "Distance (km)"
        elif activity_unit == "kWh":
            max_quantity = 500.0
            default_quantity = 5.0
            quantity_label = "Consumption (kWh)"
        else:
            max_quantity = 100.0
            default_quantity = 1.0
            quantity_label = "Number of meals"

        activity_quantity = st.number_input(
            quantity_label,
            min_value=0.0,
            max_value=max_quantity,
            value=default_quantity,
            step=1.0,
            key="activity_quantity"
        )

    with log_col3:
        st.write("")
        st.write("")
        log_activity_clicked = st.button(
            "➕ Log Activity",
            use_container_width=True,
            type="primary"
        )

    activity_co2 = 0.0
    if activity_quantity > 0:
        try:
            activity_co2 = calculate_activity(
                activity_type,
                activity_quantity
            )
            st.caption(
                f"Estimated impact: **{activity_co2:.2f} kg CO₂e**"
            )
        except ValueError:
            st.error("Please enter a valid quantity.")

    if log_activity_clicked:
        if activity_quantity <= 0:
            st.error("Quantity must be greater than zero.")
        else:
            save_activity(
                activity_type=ACTIVITY_TYPES[activity_type],
                quantity=activity_quantity,
                unit=activity_unit,
                co2=activity_co2
            )
            st.success(
                f"✅ Activity logged: {ACTIVITY_TYPES[activity_type]} · "
                f"{activity_quantity:g} {activity_unit} · "
                f"{activity_co2:.2f} kg CO₂e"
            )

    # ========================================================
    # WEEKLY TARGET
    # ========================================================

    st.markdown("### 🎯 Weekly Target")

    target_col1, target_col2 = st.columns([1, 1.5])

    current_week_total, week_start, week_end = get_weekly_co2()
    saved_target = get_weekly_target()

    with target_col1:
        weekly_target = st.number_input(
            "Weekly CO₂ target (kg)",
            min_value=1.0,
            max_value=10000.0,
            value=float(saved_target),
            step=1.0,
            key="weekly_target_input"
        )

        if st.button("💾 Save Weekly Target", use_container_width=True):
            set_weekly_target(weekly_target)
            st.success(
                f"Weekly target saved: {weekly_target:.1f} kg CO₂e"
            )

    with target_col2:
        target_progress = (
            current_week_total / weekly_target
            if weekly_target > 0 else 0
        )
        progress_percent = min(target_progress * 100, 100)

        if current_week_total > weekly_target:
            progress_color = "#fb7185"
            status_title = "⚠️ Weekly target exceeded"
            status_text = (
                f"You are {current_week_total - weekly_target:.2f} kg "
                "CO₂e above your target. You can still make lower-carbon "
                "choices for the rest of the week."
            )
        else:
            progress_color = "#4ade80"
            remaining = weekly_target - current_week_total
            status_title = "🌱 You're within your weekly target"
            status_text = (
                f"{remaining:.2f} kg CO₂e remaining before you reach "
                "your weekly target."
            )

        render_html(
            f"""
                <div class="activity-card">
                    <div style="
                        color:#86efac;
                        font-size:11px;
                        font-weight:700;
                        letter-spacing:1px;
                    ">
                        THIS WEEK · MONDAY–SUNDAY
                    </div>

                    <div style="
                        display:flex;
                        justify-content:space-between;
                        align-items:end;
                        margin-top:10px;
                    ">
                        <div>
                            <div style="
                                font-family:'Space Grotesk',sans-serif;
                                font-size:30px;
                                font-weight:700;
                                color:#f4f8f5;
                            ">
                                {current_week_total:.2f} kg
                            </div>
                            <div style="
                                color:#81978c;
                                font-size:12px;
                            ">
                                of {weekly_target:.1f} kg target
                            </div>
                        </div>

                        <div style="
                            color:{progress_color};
                            font-size:18px;
                            font-weight:700;
                        ">
                            {target_progress * 100:.0f}%
                        </div>
                    </div>

                    <div class="target-progress">
                        <div class="target-fill" style="
                            width:{progress_percent:.1f}%;
                            background:{progress_color};
                        "></div>
                    </div>

                    <div style="
                        color:{progress_color};
                        font-size:14px;
                        font-weight:700;
                        margin-top:15px;
                    ">
                        {status_title}
                    </div>

                    <div style="
                        color:#8fa69a;
                        font-size:13px;
                        line-height:1.5;
                        margin-top:5px;
                    ">
                        {status_text}
                    </div>

                    <div style="
                        color:#71867b;
                        font-size:11px;
                        margin-top:10px;
                    ">
                        Week: {week_start} → {week_end}
                    </div>
                </div>
            """
        )

    # ========================================================
    # KPI
    # ========================================================

    st.markdown("### 🌱 Current Impact")

    k1, k2, k3, k4 = st.columns(4)

    projection = total * 30

    with k1:

        render_html(
            f"""
            <div class="kpi">

                <div class="kpi-label">
                    TOTAL FOOTPRINT
                </div>

                <div class="kpi-value">
                    {total:.1f}
                </div>

                <div class="kpi-desc">
                    kg CO₂e / day
                </div>

            </div>
            """
        )

    with k2:

        render_html(
            f"""
            <div class="kpi">

                <div class="kpi-label">
                    TRANSPORT
                </div>

                <div class="kpi-value">
                    {transport_emission:.1f}
                </div>

                <div class="kpi-desc">
                    kg CO₂e
                </div>

            </div>
            """
        )

    with k3:

        render_html(
            f"""
            <div class="kpi">

                <div class="kpi-label">
                    ELECTRICITY
                </div>

                <div class="kpi-value">
                    {electricity_emission:.1f}
                </div>

                <div class="kpi-desc">
                    kg CO₂e
                </div>

            </div>
            """
        )

    with k4:

        render_html(
            f"""
            <div class="kpi">

                <div class="kpi-label">
                    30-DAY PROJECTION
                </div>

                <div class="kpi-value">
                    {projection:.0f}
                </div>

                <div class="kpi-desc">
                    kg CO₂e
                </div>

            </div>
            """
        )

    st.write("")

    # ========================================================
    # EMISSION CHART
    # ========================================================

    chart_data = {
        category: value
        for category, value in breakdown.items()
        if category != "Total" and value > 0
    }

    left, right = st.columns(
        [1.35, 0.65]
    )

    with left:

        st.markdown("### Emission Composition")

        df = pd.DataFrame(
            list(chart_data.items()),
            columns=[
                "Category",
                "CO₂e"
            ]
        )

        fig = px.pie(
            df,
            names="Category",
            values="CO₂e",
            hole=0.62
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#b7c8bf"
            ),
            margin=dict(
                t=20,
                b=20,
                l=10,
                r=10
            ),
            legend=dict(
                orientation="h",
                y=-0.05
            )
        )

        fig.update_traces(
            textinfo="percent",
            textfont_size=13
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )

    # ========================================================
    # BIGGEST CONTRIBUTOR
    # ========================================================

    with right:

        biggest = max(
            chart_data,
            key=chart_data.get
        )

        biggest_value = chart_data[biggest]

        percentage = (
            biggest_value / total * 100
            if total > 0
            else 0
        )

        render_html(
            f"""
            <div class="panel">

                <div style="
                    color:#71867b;
                    font-size:11px;
                    font-weight:700;
                    letter-spacing:1px;
                ">
                    BIGGEST CONTRIBUTOR
                </div>

                <div style="
                    font-family:'Space Grotesk',sans-serif;
                    font-size:31px;
                    font-weight:700;
                    margin-top:12px;
                    color:#f4f8f5;
                ">
                    {biggest}
                </div>

                <div style="
                    color:#86efac;
                    font-size:19px;
                    margin-top:5px;
                ">
                    {percentage:.0f}% of footprint
                </div>

                <div style="
                    color:#8fa69a;
                    margin-top:18px;
                    line-height:1.6;
                    font-size:14px;
                ">
                    This category currently has the largest
                    contribution to your estimated footprint.
                </div>

            </div>
            """
        )

    # ========================================================
    # IMPACT STATUS
    # ========================================================

    if total < 10:

        st.success(
            "🌱 **Low impact today.** Keep making sustainable choices."
        )

    elif total < 25:

        st.warning(
            "🌤️ **Moderate impact.** There are opportunities "
            "to reduce your biggest emission sources."
        )

    else:

        st.error(
            "⚠️ **High impact day.** Check your emission breakdown "
            "to identify reduction opportunities."
        )

    # ========================================================
    # AI CARBON COACH
    # ========================================================

    st.divider()

    st.markdown("### 🤖 AI Carbon Coach")

    score = get_carbon_score(total)

    coach_left, coach_right = st.columns(
        [0.75, 1.25]
    )

    # --------------------------------------------------------
    # SCORE
    # --------------------------------------------------------

    with coach_left:

        if score >= 75:
            score_color = "#4ade80"
            score_label = "Excellent"

        elif score >= 50:
            score_color = "#facc15"
            score_label = "Room to improve"

        else:
            score_color = "#fb7185"
            score_label = "High impact"

        render_html(
            f"""
                <div class="panel">

                    <div style="
                        color:#81978c;
                        font-size:11px;
                        font-weight:700;
                        letter-spacing:1px;
                    ">
                        YOUR CARBON SCORE
                    </div>

                    <div
                        class="score-number"
                        style="
                            color:{score_color};
                            margin-top:12px;
                        "
                    >
                        {score}
                    </div>

                    <div style="
                        color:#71867b;
                        font-size:13px;
                        margin-top:5px;
                    ">
                        out of 100 · {score_label}
                    </div>

                    <div class="score-track">
                        <div
                            class="score-fill"
                            style="
                                width:{score}%;
                                background:{score_color};
                            "
                        >
                        </div>
                    </div>

                    <div style="
                        color:#81978c;
                        font-size:12px;
                        margin-top:14px;
                        line-height:1.5;
                    ">
                        Your score is based on your current
                        estimated daily footprint.
                    </div>

                </div>
            """
        )

    # --------------------------------------------------------
    # REAL GROQ AI COACH
    # --------------------------------------------------------

    with coach_right:

        render_html(
            """
                <div class="panel">

                    <div style="
                        color:#86efac;
                        font-size:11px;
                        font-weight:700;
                        letter-spacing:1px;
                    ">
                        GROQ AI · PERSONALIZED COACH
                    </div>

                    <div style="
                        font-family:'Space Grotesk',sans-serif;
                        font-size:24px;
                        font-weight:700;
                        margin-top:10px;
                        color:#f4f8f5;
                    ">
                        Get advice based on your actual footprint.
                    </div>

                    <div style="
                        color:#8fa69a;
                        font-size:13px;
                        margin-top:6px;
                        line-height:1.5;
                    ">
                        EcoTrack calculates your emissions first.
                        AI then analyzes the breakdown and suggests
                        practical actions.
                    </div>

                </div>
            """
        )

        ai_col1, ai_col2 = st.columns([1, 1])

        with ai_col1:
            generate_clicked = st.button(
                "🤖 Generate AI Advice",
                use_container_width=True,
                type="primary"
            )

        with ai_col2:
            clear_clicked = st.button(
                "↻ Clear Advice",
                use_container_width=True
            )

        if clear_clicked:
            st.session_state.pop("ai_coach_result", None)
            st.rerun()

        if generate_clicked:
            with st.spinner("EcoTrack AI is analyzing your footprint..."):
                try:
                    ai_result = generate_ai_coach(
                        total=total,
                        breakdown=breakdown,
                        vehicle=vehicle,
                        distance=distance
                    )

                    st.session_state["ai_coach_result"] = ai_result

                except Exception as e:
                    st.session_state["ai_coach_result"] = None
                    st.error(
                        "AI Coach could not connect right now. "
                        "Please check your Groq API configuration."
                    )
                    st.caption(f"Technical detail: {e}")

        ai_result = st.session_state.get("ai_coach_result")

        if ai_result:
            render_html(
                f"""
                    <div class="panel" style="
                        margin-top:14px;
                        border-color:rgba(74,222,128,0.14);
                    ">
                        <div style="
                            color:#c6d6ce;
                            font-size:14px;
                            line-height:1.75;
                            white-space:pre-wrap;
                        ">
                            {ai_result}
                        </div>
                    </div>
                """
            )
        else:
            render_html(
                """
                    <div style="
                        margin-top:14px;
                        padding:16px;
                        border-radius:14px;
                        background:rgba(74,222,128,0.04);
                        border:1px solid rgba(74,222,128,0.08);
                        color:#81978c;
                        font-size:13px;
                        line-height:1.5;
                    ">
                        Click <b style="color:#86efac;">
                        Generate AI Advice</b> to get personalized
                        recommendations from your current footprint.
                    </div>
                """
            )

    # ========================================================
    # SAVE
    # ========================================================

    st.divider()

    if st.button(
        "💾 Save Today's Footprint",
        type="primary",
        use_container_width=True
    ):

        save_footprint(
            transport=transport_emission,
            electricity=electricity_emission,
            food=food,
            flight=flight,
            shopping=shopping,
            waste=waste,
            total=total
        )

        st.success(
            f"Saved successfully — {total:.2f} kg CO₂e."
        )


# ============================================================
# ANALYTICS
# ============================================================

elif page == "📊 Analytics":

    show_hero(
        "● PERSONAL ANALYTICS",
        "Your climate dashboard.",
        "Discover patterns and understand how your footprint "
        "changes over time."
    )

    # ========================================================
    # ACTIVITY HISTORY + FILTERS
    # ========================================================

    st.subheader("📜 Activity History")

    filter_col1, filter_col2, filter_col3 = st.columns([1, 1, 1])

    with filter_col1:
        history_type = st.selectbox(
            "Filter by type",
            ["All"] + list(ACTIVITY_TYPES.values())
        )

    with filter_col2:
        history_start = st.date_input("From date", value=None)

    with filter_col3:
        history_end = st.date_input("To date", value=None)

    filtered_activities = get_activities(
        activity_type=history_type,
        start_date=history_start,
        end_date=history_end
    )

    if filtered_activities:
        activity_df = pd.DataFrame(
            filtered_activities,
            columns=[
                "ID",
                "Activity",
                "Quantity",
                "Unit",
                "CO₂e (kg)",
                "Logged At"
            ]
        )
        activity_df["CO₂e (kg)"] = activity_df["CO₂e (kg)"].round(2)

        st.dataframe(
            activity_df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No activities match the selected filters.")

    st.divider()

    history = get_history()

    if not history:

        st.info(
            "No historical data yet. Save a footprint first."
        )

    else:

        history_df = pd.DataFrame(
            history,
            columns=[
                "ID",
                "Date",
                "Transport",
                "Electricity",
                "Food",
                "Flight",
                "Shopping",
                "Waste",
                "Total"
            ]
        )

        history_df["Date"] = pd.to_datetime(
            history_df["Date"]
        )

        total_recorded = history_df["Total"].sum()
        average = history_df["Total"].mean()
        lowest = history_df["Total"].min()
        highest = history_df["Total"].max()

        a, b, c, d = st.columns(4)

        a.metric(
            "🌍 Total",
            f"{total_recorded:.1f} kg"
        )

        b.metric(
            "📊 Average",
            f"{average:.1f} kg"
        )

        c.metric(
            "↓ Lowest",
            f"{lowest:.1f} kg"
        )

        d.metric(
            "↑ Highest",
            f"{highest:.1f} kg"
        )

        st.divider()

        st.subheader("📈 Footprint Trend")

        trend_df = history_df.sort_values(
            "Date"
        )

        fig = px.area(
            trend_df,
            x="Date",
            y="Total"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#9fb2a8"
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )

        st.subheader("🌍 Category Analysis")

        categories = [
            "Transport",
            "Electricity",
            "Food",
            "Flight",
            "Shopping",
            "Waste"
        ]

        category_totals = {
            category:
            history_df[category].sum()
            for category in categories
        }

        category_df = pd.DataFrame(
            list(
                category_totals.items()
            ),
            columns=[
                "Category",
                "CO₂e"
            ]
        )

        fig = px.bar(
            category_df,
            x="Category",
            y="CO₂e",
            text_auto=".1f"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#9fb2a8"
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )


# ============================================================
# WHAT-IF LAB
# ============================================================

elif page == "🔮 What-If Lab":

    show_hero(
        "● SIMULATION ENGINE",
        "What if you chose differently?",
        "Simulate a transport switch and instantly see "
        "the potential difference."
    )

    st.subheader("🚗 Current Choice")

    current = st.selectbox(
        "Current transport",
        [
            "car_petrol",
            "car_diesel",
            "motorcycle",
            "bus",
            "train"
        ],
        format_func=lambda x: {
            "car_petrol": "🚗 Petrol Car",
            "car_diesel": "🚙 Diesel Car",
            "motorcycle": "🏍️ Motorcycle",
            "bus": "🚌 Bus",
            "train": "🚆 Train"
        }[x]
    )

    distance = st.slider(
        "Daily distance (km)",
        1.0,
        200.0,
        20.0,
        1.0
    )

    st.subheader("🌱 Alternative Choice")

    alternative = st.selectbox(
        "Alternative transport",
        [
            "car_petrol",
            "car_diesel",
            "motorcycle",
            "bus",
            "train"
        ],
        index=3,
        format_func=lambda x: {
            "car_petrol": "🚗 Petrol Car",
            "car_diesel": "🚙 Diesel Car",
            "motorcycle": "🏍️ Motorcycle",
            "bus": "🚌 Bus",
            "train": "🚆 Train"
        }[x]
    )

    current_emission = calculate_transport(
        distance,
        current
    )

    alternative_emission = calculate_transport(
        distance,
        alternative
    )

    saving = (
        current_emission -
        alternative_emission
    )

    st.divider()

    x1, x2, x3 = st.columns(3)

    x1.metric(
        "Current",
        f"{current_emission:.2f} kg"
    )

    x2.metric(
        "Alternative",
        f"{alternative_emission:.2f} kg"
    )

    x3.metric(
        "Potential Difference",
        f"{saving:.2f} kg"
    )

    comparison_df = pd.DataFrame(
        {
            "Choice": [
                "Current",
                "Alternative"
            ],
            "CO₂e": [
                current_emission,
                alternative_emission
            ]
        }
    )

    fig = px.bar(
        comparison_df,
        x="Choice",
        y="CO₂e",
        text_auto=".2f"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#9fb2a8"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )

    if saving > 0:

        st.success(
            f"🌱 Switching could save approximately "
            f"**{saving:.2f} kg CO₂e/day** "
            f"or **{saving * 30:.1f} kg CO₂e/month**."
        )

    elif saving < 0:

        st.warning(
            "The selected alternative has a higher "
            "estimated footprint."
        )

    else:

        st.info(
            "Both choices have the same estimated footprint."
        )


# ============================================================
# HISTORY
# ============================================================

elif page == "📜 History":

    show_hero(
        "● YOUR JOURNEY",
        "Every choice counts.",
        "Review your recorded footprint and track "
        "your journey over time."
    )

    history = get_history()

    if not history:

        st.info(
            "Your history is empty. "
            "Start tracking your footprint!"
        )

    else:

        history_df = pd.DataFrame(
            history,
            columns=[
                "ID",
                "Date",
                "Transport",
                "Electricity",
                "Food",
                "Flight",
                "Shopping",
                "Waste",
                "Total"
            ]
        )

        total = history_df["Total"].sum()

        records = len(history_df)

        c1, c2 = st.columns(2)

        c1.metric(
            "🌍 Recorded Footprint",
            f"{total:.1f} kg CO₂e"
        )

        c2.metric(
            "📅 Records",
            records
        )

        st.divider()

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )