import streamlit as st
import requests
import os
from auth import login_or_signup  # Import the authentication function

# Set up the FastAPI URL
FASTAPI_URL = "http://127.0.0.1:8000/get_disease_info"

# Define disease and symptoms data
diseases_info = {
    "diabetes": ["Frequent urination", "Increased thirst", "Extreme hunger", "Fatigue"],
    "hypertension": ["Headache", "Shortness of breath", "Nosebleeds", "Fatigue"],
    "heart disease": ["Chest pain", "Shortness of breath", "Pain in neck/jaw", "Fatigue"],
    "asthma": ["Shortness of breath", "Chest tightness", "Wheezing", "Coughing"]
}

# Custom CSS for Styling
st.markdown("""<style>
    .header { font-size: 36px; color: #0074D9; font-weight: bold; text-align: center; }
    .subheader { font-size: 24px; color: #FF6F61; text-align: center; }
    .highlight { font-size: 26px; color: #2E8B57; font-weight: bold; }
    .symptom-list { font-size: 18px; color: #333333; line-height: 1.8; }
    .footer { font-size: 16px; color: #808080; text-align: center; padding-top: 20px; }
    .button { background-color: #0074D9; color: white; padding: 12px 30px; font-size: 18px; border-radius: 5px; cursor: pointer; border: none; }
    .button:hover { background-color: #005fa3; }
</style>""", unsafe_allow_html=True)

# Function to handle authentication for the main page
def auth_for_main_page():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    # Show login/signup if user is not logged in
    if not st.session_state.logged_in:
        login_or_signup()  # This will handle login or signup
    else:
        st.success("You are logged in!")
        
        # Show logout button if the user is logged in
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False  # Set the session state to False on logout
            st.session_state.page = "main"  # Reset the page to the main page (login/signup)
            st.rerun()  # Re-run the app to reflect changes
        
# Main page
def main_page():
    # Authentication check for the main page
    auth_for_main_page()

    # Only show content if logged in
    if st.session_state.logged_in:
        st.markdown('<div class="header">💬 Healthcare Chatbot</div>', unsafe_allow_html=True)
        st.markdown('<div class="subheader">Get detailed information about Selected diseases and symptoms.</div>', unsafe_allow_html=True)
        
        # Disease selection dropdown
        st.sidebar.header("Search by Disease or Symptom")
        disease_list = list(diseases_info.keys())
        disease = st.sidebar.selectbox("Select a Disease", [""] + disease_list, index=0, help="Choose a disease to get more details.")

        # Symptom selection dropdown - dynamically updated based on disease selection
        if disease:
            symptoms_options = diseases_info[disease]
        else:
            symptoms_options = sorted({symptom for symptoms in diseases_info.values() for symptom in symptoms})

        symptom = st.sidebar.selectbox("Select a Symptom", [""] + symptoms_options, index=0, help="Choose a symptom to see related diseases.")

        if st.sidebar.button("Get Disease Info", key="get_info", help="Click to get disease details"):
            st.markdown("---")
            col1, col2 = st.columns([2, 1])

            with col1:
                if disease:
                    response = requests.post(FASTAPI_URL, json={"disease": disease})
                    if response.status_code == 200:
                        data = response.json()
                        st.markdown(
                            f"""
                            <div style="
                                background-color:#f7f7f7;
                                padding:10px;
                                border-radius:8px;
                                border: 1px solid #ddd;
                                text-align: center;
                                font-size: 20px;
                                color: #333;
                                font-weight: bold;">
                                {disease.capitalize()}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            "<div style='color: red; font-weight: bold;'>Description</div>", 
                            unsafe_allow_html=True
                        )
                        st.write(data.get("description", "No description available"))
                        st.markdown(
                            "<div style='color: red; font-weight: bold;'>Symptoms</div>", 
                            unsafe_allow_html=True
                        )
                        st.markdown(f"<ul class='symptom-list'>", unsafe_allow_html=True)
                        for symptom in data.get("symptoms", []):
                            st.markdown(f"<li>{symptom}</li>", unsafe_allow_html=True)
                        st.markdown("</ul>", unsafe_allow_html=True)
                        st.markdown(
                            "<div style='color: red; font-weight: bold;'>Treatment</div>", 
                            unsafe_allow_html=True
                        )
                        st.markdown(f"<div>{data.get('treatment', 'No treatment information available')}</div>", unsafe_allow_html=True)
                    else:
                        st.error("Error fetching data. Please try again.")
                elif symptom:
                    related_diseases = [dis for dis, syms in diseases_info.items() if symptom in syms["symptoms"]]
                    if related_diseases:
                        st.markdown(f"<div class='highlight'>Diseases related to symptom '{symptom}'</div>", unsafe_allow_html=True)
                        for related_disease in related_diseases:
                            response = requests.post(FASTAPI_URL, json={"disease": related_disease})
                            data = response.json()
                            st.write(f"**{related_disease.capitalize()}**")
                            st.write(data.get("description", "No description available"))
                            st.write(f"**Treatment:** {data.get('treatment', 'No treatment available')}")
                    else:
                        st.info("No related diseases found for this symptom.")
            with col2:
                if disease:
                    response = requests.post(FASTAPI_URL, json={"disease": disease})
                    if response.status_code == 200:
                        datas = response.json()
                        st.markdown(
                            "<div style='color: red; font-weight: bold;'>Recommendations</div>", 
                            unsafe_allow_html=True
                        )
                        st.markdown(
                            "<div style='color: yellow; font-weight: bold;'>Exercise:</div>", 
                            unsafe_allow_html=True
                        )
                        st.write(data.get("exercise", "No specific recommendations"))

                        st.markdown(
                            "<div style='color: yellow; font-weight: bold;'>Sleep Hours:</div>", 
                            unsafe_allow_html=True
                        )
                        st.write(data.get("sleep_hours", "No specific recommendations"))

                        st.markdown(
                            "<div style='color: yellow; font-weight: bold;'>Diet:</div>", 
                            unsafe_allow_html=True
                        )
                        st.write(data.get("diet", "No specific recommendations"))

                    else:
                        st.error("Error fetching data. Please try again.")

                st.markdown(
                    "<div style='color: red; font-weight: bold;'>Health Tips</div>", 
                    unsafe_allow_html=True
                )
                tips = {
                    "diabetes": "Maintain a healthy diet with low sugar intake, and exercise regularly.",
                    "hypertension": "Reduce salt intake, manage stress, and exercise regularly.",
                    "heart disease": "Quit smoking, eat heart-healthy foods, and monitor blood pressure.",
                    "asthma": "Avoid triggers, use prescribed inhalers, and maintain good air quality."
                }
                st.write(tips.get(disease.lower(), "No specific health tips available for this disease."))

        else:
            st.warning("Please select a disease or symptom and click the 'Get Disease Info' button to get detailed information.")
    
        if st.sidebar.button("Go to Health Risk Assessment"):
            st.session_state.page = "health_risk_assessment"  # Set state to health risk assessment page
            st.rerun()

        # Button to go to the bot page
        if st.sidebar.button("Start Diagnosis Simulation"):
            st.session_state["navigate_to_bot"] = True
            st.rerun()  # Force a rerun of the app, ensuring the button's state is updated immediately


        # Button to go to the developer info page
        if st.sidebar.button("Developed By"):
            st.session_state.page = "Developed_By"  # Set the page state to Developed_By
            st.rerun()  # Force a rerun of the app, ensuring the button's state is updated immediately

        # # Display developer info page based on state
        # if st.session_state.get("page") == "Developed_By":
        #     Developed_By()

    else:
        st.write("Please log in to access the Healthcare Diagnosis Chatbot.")
    # Footer
    st.markdown('<div class="footer">Healthcare Chatbot - Powered by AI for better healthcare.</div>', unsafe_allow_html=True)


# Check if navigate_to_bot flag is set to True
if "navigate_to_bot" in st.session_state and st.session_state["navigate_to_bot"]:
    os.system("streamlit run bot_page.py")  # Run the bot page as a separate Streamlit app
    st.session_state["navigate_to_bot"] = False  # Reset flag

# Health Risk Assessment page with more options and improved layout
def health_risk_assessment_page():
    st.markdown('<div class="header">Health Risk Assessment</div>', unsafe_allow_html=True)   
    with st.form("risk_assessment_form"):
        # Basic Information
        st.subheader("Basic Information")
        age = st.number_input("Enter your age", min_value=1, max_value=100, value=25)
        gender = st.selectbox("Select your gender", ["Male", "Female", "Other"])
        smoker = st.radio("Do you smoke?", ["Yes", "No"])
        
        # Lifestyle and Physical Health
        st.subheader("Lifestyle & Physical Health")
        physical_activity = st.slider("Physical activity (days per week)", 0, 7, 3)
        sleep_quality = st.slider("Sleep quality (1=Poor, 10=Excellent)", 1, 10, 7)
        bmi = st.number_input("Enter your Body Mass Index (BMI)", min_value=10.0, max_value=50.0, value=22.5)
        
        # Diet and Mental Health
        st.subheader("Diet & Mental Health")
        diet_habits = st.radio("Diet Type", ["Balanced", "High in Fat/Sugar", "Vegetarian", "Vegan"])
        stress_level = st.slider("Stress Level (1=Low, 10=High)", 1, 10, 5)

        # Medical History
        st.subheader("Medical History")
        family_history = st.checkbox("Family history of chronic diseases")
        existing_conditions = st.multiselect(
            "Select any existing health conditions",
            ["Diabetes", "Hypertension", "Heart Disease", "Asthma", "None"]
        )

        # Calculate Risk Score
        risk_score = 0
        if age > 45:
            risk_score += 1
        if smoker == "Yes":
            risk_score += 1
        if physical_activity < 3:
            risk_score += 1
        if bmi >= 25:
            risk_score += 1
        if family_history:
            risk_score += 1
        if sleep_quality < 5:
            risk_score += 1
        if stress_level > 7:
            risk_score += 1
        if "Diabetes" in existing_conditions or "Hypertension" in existing_conditions:
            risk_score += 2  # Higher weight for chronic conditions

        # Submit Button
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write("Your health risk score is:", risk_score)
            if risk_score <= 3:
                st.success("Low Risk: Continue maintaining a healthy lifestyle.")
            elif 4 <= risk_score <= 6:
                st.warning("Moderate Risk: Consider regular health check-ups and lifestyle adjustments.")
            else:
                st.error("High Risk: Consult with a healthcare provider for a detailed evaluation.")

        # Button to go back to the main page
    if st.sidebar.button("Back to Healthcare Chatbot"):
        st.session_state.page = "main"
        st.rerun()  # Force a rerun of the app, ensuring the button's state is updated immediately

    # Button to go to the bot page
    if st.sidebar.button("Start Diagnosis Simulation"):
        st.session_state["navigate_to_bot"] = True
        st.rerun()  # Force a rerun of the app, ensuring the button's state is updated immediately

    # Button to go to the developer info page
    if st.sidebar.button("Developed By"):
        st.session_state.page = "Developed_By"  # Set the page state to Developed_By
        st.rerun()  # Force a rerun of the app, ensuring the button's state is updated immediately


def Developed_By():
    # Developer info dictionary
    Developed_By = {
        "name": "Md Moinuddin",
        "bio": "Hi! I am Md Moinuddin, a Data Scientist with experience in Machine Learning, Data Analysis, and building impactful AI-driven solutions. I specialize in working with Python, Streamlit, FastAPI, and various data science libraries.",
        "image": "me.jpeg"
    }
    
    # Add custom CSS for styling
    st.markdown("""
        <style>
        .developer-info {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            background-color: #f1f1f1;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
            border: 2px solid #0077b6;  /* Improved border */
        }
        .developer-info h2 {
            color: #2c3e50;  /* Dark blue for name */
            font-size: 2.4em;
            margin-top: 20px;
            font-weight: bold;
        }
        .developer-info p {
            color: #34495e;  /* Soft greyish blue for bio text */
            font-size: 1.1em;
            margin-top: 15px;
            line-height: 1.7;
            max-width: 300px;
        }
        .bio-text {
            color: #555;
            font-size: 1.1em;
            margin-top: 10px;
            text-align: justify;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Display developer info in a styled container
    # st.markdown('<div class="developer-info">', unsafe_allow_html=True)

    # Display the image using st.image()
    st.image(Developed_By['image'], width=200) 

    # Display the name and bio
    st.markdown(f"<h2>{Developed_By['name']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p class='bio-text'>{Developed_By['bio']}</p>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


    if st.sidebar.button("Back to Healthcare Chatbot"):
        st.session_state.page = "main"
        st.rerun()  # Force a rerun of the app, ensuring the button's state is updated immediately

    # Button to go to the bot page
    if st.sidebar.button("Start Diagnosis Simulation"):
        st.session_state["navigate_to_bot"] = True
        st.rerun()  # Force a rerun of the app, ensuring the button's state is updated immediately

    if st.sidebar.button("Go to Health Risk Assessment"):
        st.session_state.page = "health_risk_assessment"  # Set state to health risk assessment page
        st.rerun()  # Force a rerun of the app, ensuring the button's state is updated immediately


# Page navigation logic
if 'page' not in st.session_state:
    st.session_state.page = "main"

if st.session_state.page == "main":
    main_page()
elif st.session_state.page == "health_risk_assessment":
    health_risk_assessment_page()
elif st.session_state.page == "Developed_By":
    Developed_By()
