

# ⚡ FinBot Core: Autonomous NLP Financial Tracker

FinBot Core is an autonomous, full-stack financial tracking system that leverages Natural Language Processing (NLP) to transform unstructured conversational text into structured financial insights. Built with a focus on security and performance, it provides a seamless "Secure Access Terminal" for multi-user expense management.

## 🚀 Key Features

* **Autonomous NLP Engine:** Utilizes Regular Expressions and fuzzy matching logic to intelligently extract monetary values and categorize expenses from free-form text.
* **Secure Access Terminal:** Implements a robust authentication gateway using salted SHA-256 password hashing and session management to ensure data privacy between users.
* **Real-Time Analytics Dashboard:** Features interactive Plotly visualizations, including spending timelines and category distributions, alongside real-time budget utilization tracking.
* **Performance Optimized:** Incorporates Streamlit `@st.cache_data` and database indexing to deliver a lightning-fast UI and efficient data retrieval.

## 🛠️ Tech Stack

* **Language:** Python
* **Frontend:** Streamlit, Custom CSS
* **Data Visualization:** Plotly Express
* **Data Manipulation:** Pandas
* **Database & Security:** SQLite3, Hashlib, Secrets
* **Intelligence:** Python `re` (Regular Expressions), `difflib` (Fuzzy Matching)

## ⚙️ Local Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/K-ShivamZad/FinBot_Project.git
    cd FinBot_Project
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Launch the Application:**
    ```bash
    streamlit run app.py
    ```

4.  **Initialize Your Session:**
    Upon first launch, navigate to the **REGISTER** tab in the Secure Access Terminal to create your account. The system will automatically initialize the indexed SQLite database.

## 📂 Project Structure

* `app.py`: The main entry point featuring the Secure Access Terminal and Analytics Dashboard.
* `brain.py`: The NLP logic for text parsing and intelligent categorization.
* `db_handler.py`: The database engine managing user authentication and transaction logs.
* `requirements.txt`: Project dependencies (Streamlit, Pandas, Plotly).

## 🔮 Future Roadmap
* Transitioning to zero-shot classification using HuggingFace Transformers for deeper NLP understanding.
* Integration with PostgreSQL for scalable cloud deployment.
* Adding automated recurring bill reminders and SMS/Email notifications.

---
**Developed by:** [Kumar Shivam Azad ]
