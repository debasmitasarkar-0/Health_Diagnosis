import time
import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Google Gemini API
def get_disease_prediction(primary_symptom, other_symptoms, age, sex, medical_history):
    model = genai.GenerativeModel('gemini-2.0-pro-exp')

    prompt = f"""
You are a highly experienced medical professional. Based on the provided symptoms, predict the possible disease and suggest necessary clinical tests. Also, provide a temporary solution with the name of the medicine composition.

**Patient Information:**
- **Age:** {age}
- **Sex:** {sex}
- **Medical History (if any):** {medical_history}

**Primary Symptom (Required):** {primary_symptom}

**Other Symptoms (Optional):** {other_symptoms}

### Response Format:
| Category                | Details                          |
|-------------------------|---------------------------------|
| **Possible Disease**    | [Disease Name]                 |
| **Recommended Tests**   | - Test 1                       |
|                         | - Test 2                       |
|                         | - Test 3 (if applicable)       |
| **Temporary Solution**  | - Medicine 1 (Composition)     |
|                         | - Medicine 2 (if applicable)   |

- The medicine should be **OTC or commonly prescribed** for symptomatic relief.
- Do NOT include dosage; only provide the generic composition.
"""

    try:
        response = model.generate_content([prompt])
        return response.text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# Streamlit App Configuration

st.header("🩺 Health Diagnosis AI")
st.subheader("Enter Your Symptoms Below")

# Input Fields in a single row
col1, col2, col3 = st.columns(3)
with col1:
    age = st.text_input("Age", key="age", placeholder="Enter Age")
with col2:
    sex = st.selectbox("Sex", ["Male", "Female", "Other"], key="sex")
with col3:
    medical_history = st.text_input("Previous Medical History (Optional)", key="medical_history", placeholder="E.g., Diabetes, Hypertension")

# Primary and Other Symptoms
primary_symptom = st.text_input("Primary Symptom (Required)", key="primary_symptom")
other_symptoms = st.text_area("Other Symptoms (Optional)", key="other_symptoms")

# Submit Button with session state handling
if "submit_button" not in st.session_state:
    st.session_state["submit_button"] = False

submit = st.button("🔍 Predict Disease & Suggest Tests", disabled=st.session_state["submit_button"])

# Ensure Primary Symptom is provided
if submit:
    if not primary_symptom.strip():
        st.error("❌ Primary Symptom is required!")
    else:
        st.session_state["submit_button"] = True  # Disable button

        with st.spinner("🔄 Analyzing symptoms... Please wait"):
            time.sleep(2)  # Simulating delay
            response = get_disease_prediction(primary_symptom, other_symptoms, age, sex, medical_history)

        st.subheader("📋 Diagnosis Result")
        st.markdown(response, unsafe_allow_html=True)

        st.session_state["submit_button"] = False  # Re-enable button