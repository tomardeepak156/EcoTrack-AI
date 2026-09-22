🌱 EcoTrack AI

Measure → Understand → Simulate → Act → Track

EcoTrack AI is an AI-powered personal carbon footprint tracking application that helps users understand the environmental impact of their everyday activities.

Users can log activities such as transportation, electricity consumption, and meals, calculate their CO₂ footprint using predefined emission factors, monitor a weekly carbon target, analyze their activity history, and receive personalized recommendations from an AI sustainability coach.

🆔 Hackathon Information

Hackathon ID: AZIS-M6AXSQ

Team: Haridwar Team 38

College: Haridwar University

Project: EcoTrack AI

🚀 Live Demo

🌱 EcoTrack AI – Live Demo

🎯 Problem Statement

People often want to reduce their environmental impact but do not have a simple way to measure how their everyday activities contribute to their carbon footprint.

EcoTrack AI provides a simple and interactive way to record everyday activities and understand their estimated CO₂ emissions.

The application transforms activity data into:

📊 Carbon footprint insights

🎯 Weekly carbon targets

📈 Historical activity tracking

🔎 Category-level breakdowns

🤖 Personalized AI recommendations

✨ Features

EcoTrack AI implements all five required features of the hackathon brief.

1. 📝 Log an Activity

Users can log everyday activities by selecting an activity type and entering a quantity.

Supported Activities

🚗 Car travel

🚌 Bus travel

✈️ Flight

⚡ Electricity consumption

🥗 Vegetarian meal

🍗 Non-vegetarian meal

Example

Activity: Car
Quantity: 10 km
CO₂e: 2.00 kg

The activity is stored in the application's SQLite database and becomes available in the activity history.

2. 🧮 CO₂ Calculation

EcoTrack AI uses fixed emission factors to calculate CO₂ emissions.

Activity

Emission Factor

🚗 Car

0.20 kg CO₂e / km

🚌 Bus

0.08 kg CO₂e / km

✈️ Flight

0.25 kg CO₂e / km

⚡ Electricity

0.80 kg CO₂e / kWh

🥗 Veg Meal

0.50 kg CO₂e / meal

🍗 Non-Veg Meal

2.00 kg CO₂e / meal

Calculation Formula

CO₂e = Quantity × Emission Factor

Example

10 km × 0.20 kg CO₂e/km
= 2.00 kg CO₂e

The calculation engine is deterministic.

The AI model does not calculate, modify, or invent emission factors.

3. 📊 Dashboard

The dashboard provides a visual overview of the user's carbon footprint.

It includes:

Total CO₂ footprint

Category breakdown

Carbon Score

Largest contributing category

Visual charts

Footprint insights

Users can quickly identify which areas contribute most to their footprint.

4. 🎯 Weekly CO₂ Target

Users can set their own weekly carbon target.

EcoTrack AI defines the weekly period as:

Monday 00:00 → Sunday 23:59

The application calculates the user's current weekly emissions and compares them against the configured target.

The dashboard shows

Current weekly CO₂

Weekly target

Progress percentage

Remaining allowance

Target exceeded warning

When the target is approached or exceeded, EcoTrack AI warns and encourages the user rather than blocking activity logging.

5. 📜 History & Filters

Every logged activity is stored locally using SQLite.

The history section displays:

Activity ID

Activity type

Quantity

Unit

CO₂ emissions

Date and time

Users can filter their history by:

Activity type

Start date

End date

This allows users to track their carbon footprint over time.

🤖 AI Carbon Coach

EcoTrack AI includes an AI-powered sustainability coach using the Groq API.

The AI analyzes the user's calculated footprint and generates personalized recommendations.

The AI provides

A personalized insight

Identification of major contributing areas

Exactly three practical actions

Example

INSIGHT:
Your largest carbon impact comes from transportation.

ACTIONS:
1. Consider public transport for shorter trips.
2. Carpool when possible.
3. Combine multiple trips into one journey.

🧠 AI Design

EcoTrack AI separates deterministic carbon calculations from AI recommendations.

The calculation engine

Calculates CO₂ emissions

Uses predefined emission factors

Produces deterministic results

The AI coach

Analyzes the provided footprint

Identifies important patterns

Generates personalized recommendations

The AI does not

❌ Calculate emission factors

❌ Invent emission numbers

❌ Modify calculated CO₂ values

❌ Replace the deterministic calculation engine

🔄 Product Flow

┌───────────────┐
│    MEASURE    │
└───────┬───────┘
        ↓
┌───────────────┐
│   UNDERSTAND  │
└───────┬───────┘
        ↓
┌───────────────┐
│    SIMULATE   │
└───────┬───────┘
        ↓
┌───────────────┐
│      ACT      │
└───────┬───────┘
        ↓
┌───────────────┐
│     TRACK     │
└───────┬───────┘
        │
        └──────────────→ Measure Again

🏗️ Technology Stack

Frontend

Streamlit

HTML

CSS

Plotly

Backend / Application Logic

Python

SQLite

Pandas

AI

Groq API

openai/gpt-oss-20b

Configuration

JSON

Python environment variables

.env

📁 Project Structure

EcoTrack-AI/
│
├── app.py
├── calculator.py
├── emission_factors.json
├── README.md
├── DECISIONS.md
├── requirements.txt
├── .gitignore
│
├── services/
│   ├── ai_coach.py
│   └── database.py
│
└── data/
    └── ecotrack.db

data/ecotrack.db is local application data and is excluded from GitHub using .gitignore.

⚙️ Local Installation

1. Clone the repository

git clone https://github.com/tomardeepak156/EcoTrack-AI.git
cd EcoTrack-AI

2. Create a virtual environment

python -m venv .venv

Windows PowerShell

.venv\Scripts\Activate.ps1

3. Install dependencies

pip install -r requirements.txt

4. Configure Groq API

Create a .env file in the project root:

GROQ_API_KEY=your_groq_api_key

Never commit your .env file or API key to GitHub.

5. Run the application

streamlit run app.py

The application will open in your browser.

🔐 Authentication

EcoTrack AI does not implement authentication.

There is:

❌ No login

❌ No signup

❌ No account creation

❌ No authentication wall

Judges can access the application directly.

🗄️ Data Storage

EcoTrack AI uses SQLite for local data persistence.

Activity records contain:

activity_type
quantity
unit
co2
logged_at

Weekly target settings are also stored locally.

The application also maintains historical footprint data for analytics functionality.

🧪 Example Calculations

🚗 Car

10 km × 0.20 = 2.00 kg CO₂e

🚌 Bus

10 km × 0.08 = 0.80 kg CO₂e

✈️ Flight

10 km × 0.25 = 2.50 kg CO₂e

⚡ Electricity

10 kWh × 0.80 = 8.00 kg CO₂e

🥗 Veg Meal

1 meal × 0.50 = 0.50 kg CO₂e

🍗 Non-Veg Meal

1 meal × 2.00 = 2.00 kg CO₂e

🧩 Decision Points

The complete Decision Point documentation is available in DECISIONS.md.

Decision Point 1 — User Nudge Behavior

Choice: Warn + Encourage

EcoTrack warns users when their footprint is high or when they approach/exceed their weekly target. The application does not shame users or block them from logging activities, keeping the experience supportive and encouraging continued tracking.

Decision Point 2 — Absurd Input Handling

Choice: Reject / Warn

EcoTrack does not silently calculate clearly unrealistic activity values. Inputs outside reasonable limits are rejected or flagged so that incorrect data does not distort the user's carbon footprint.

Decision Point 3 — Week Definition

Choice: Monday 00:00 → Sunday 23:59

EcoTrack defines a week from Monday through Sunday. Weekly CO₂ progress is calculated using activities logged during the current Monday–Sunday period and compared against the user's configured weekly target.

🔌 Standard API

Standard API: Not implemented.

EcoTrack AI is implemented as an interactive Streamlit web application. The required functionality is exposed directly through the browser interface rather than through a separate standard API.

🧪 Hackathon Requirements Checklist

Requirement

Status

Log an activity

✅

CO₂ calculation

✅

Dashboard

✅

Weekly CO₂ target

✅

History & filters

✅

No authentication

✅

Public GitHub repository

✅

README

✅

Hackathon ID

✅

DECISIONS.md

✅

Standard API declaration

✅

Public deployment

✅

3–4 minute demo recording

⏳

🌍 Sustainability Goal

EcoTrack AI is designed to make carbon footprint tracking simple and actionable.

Instead of only showing a number, the application helps users move from:

Awareness
    ↓
Measurement
    ↓
Understanding
    ↓
Action
    ↓
Tracking

The goal is to make everyday environmental choices more measurable and easier to understand.

👨‍💻 Team

Haridwar Team 38

College: Haridwar University

Hackathon ID: AZIS-M6AXSQ

📌 Hackathon Submission Information

Project: EcoTrack AI

Hackathon ID: AZIS-M6AXSQ

Team: Haridwar Team 38

Institution: Haridwar University

GitHub Repository

https://github.com/tomardeepak156/EcoTrack-AI

Public Application

https://ecotrack-ai-gkura3yjr3ysafc9bgk7q5.streamlit.app/

🌱 EcoTrack AI

Make your footprint visible.
Make your next action count.