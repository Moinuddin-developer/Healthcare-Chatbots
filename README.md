🖥️ Running the Application
Follow the steps below to run both the backend and frontend of the Healthcare Chatbot application.

Backend: Server Setup
Ensure Python Version: Make sure you're using Python 3.9 or higher.

Create a Virtual Environment:
Run the following command to create a virtual environment:
python -m venv env

Activate the Virtual Environment:
On Windows, activate it with:
.\env\Scripts\activate

Install Required Packages:
Install all the necessary dependencies from the requirements.txt file by running:
pip install -r requirements.txt

Run the Server:
Launch the server using Uvicorn with the following command:
uvicorn app:app --reload

Your backend server should now be running and accessible at http://127.0.0.1:8000.


Frontend: UI Setup
Navigate to the Frontend Directory:

The frontend files should be located in the parent directory (in this case, the healthcare-chatbot directory).
Activate the Virtual Environment for the Frontend:

If you haven’t already, activate the virtual environment that you created earlier for the server:
.\env\Scripts\activate

Run the Frontend Application:
Launch the Streamlit UI using the following command:
streamlit run chatbot_ui.py

Your frontend should now be accessible through your browser, and the chatbot UI will be ready for interaction!


Tips for Development
Make sure both the backend server and frontend UI are running simultaneously for the best experience.
some time If you make any changes to the code, restart both the backend and frontend servers to see the updates.