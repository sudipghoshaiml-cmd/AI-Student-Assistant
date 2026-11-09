import streamlit as st
import json
import datetime
import urllib.request
import urllib.error

# Gemini API Key & Direct REST Function
API_KEY = "AQ.Ab8RN6Ls0iJoH9aQVrz_urlqMImK1QPimpZCzNkFZWVJrDUtxg"

def call_gemini(prompt_text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }]
    }
    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers, method="POST")
        with urllib.request.urlopen(req) as response:
            res_body = json.loads(response.read().decode("utf-8"))
            return res_body["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Error: {e}"

st.title("🎓 AI-Based Student Assistant")

# Sidebar for Navigation (All Features Included)
option = st.sidebar.selectbox(
    "Choose Feature",
    [
        "AI Student Chatbot", 
        "PDF Study Notes Assistant", 
        "AI Quiz Generator", 
        "Smart Study Planner", 
        "Notes Manager"
    ]
)

# ----------------- FEATURE 1: AI CHATBOT -----------------
if option == "AI Student Chatbot":
    st.header("🤖 Student Doubt Solver Chatbot")
    user_query = st.text_input("Ask any academic question or advice:")
    
    if st.button("Get Answer"):
        if user_query:
            prompt = f"You are a helpful academic tutor. Explain simply: {user_query}"
            with st.spinner("Generating answer..."):
                ans = call_gemini(prompt)
            st.success("AI Response:")
            st.write(ans)
        else:
            st.warning("Please enter a question!")

# ----------------- FEATURE 2: PDF STUDY NOTES ASSISTANT -----------------
elif option == "PDF Study Notes Assistant":
    st.header("📄 PDF Study Notes Assistant")
    st.write("Upload a text-based note or study material, and ask questions about it!")
    
    uploaded_file = st.file_uploader("Upload a TXT or text file / document content", type=["txt", "md"])
    
    if uploaded_file is not None:
        file_content = uploaded_file.read().decode("utf-8")
        st.success("File uploaded successfully!")
        
        user_question = st.text_input("What do you want to know from this document?")
        if st.button("Analyze Document"):
            if user_question:
                prompt = f"Here is the study material:\n{file_content}\n\nBased on this material, answer the following question: {user_question}"
                with st.spinner("Analyzing document..."):
                    response = call_gemini(prompt)
                st.success("AI Analysis:")
                st.write(response)
            else:
                st.warning("Please enter a question about the document.")

# ----------------- FEATURE 3: AI QUIZ GENERATOR -----------------
elif option == "AI Quiz Generator":
    st.header("❓ AI Quiz Generator")
    st.write("Test your knowledge by generating a custom quiz on any topic!")
    
    quiz_topic = st.text_input("Enter Topic or Subject (e.g., Python Functions, Calculus Limits):")
    num_questions = st.number_input("Number of questions:", min_value=1, max_value=10, value=5)
    
    if st.button("Generate Quiz"):
        if quiz_topic:
            prompt = f"Create a multiple-choice quiz (MCQ) with {num_questions} questions about '{quiz_topic}'. Include the correct answers and a brief explanation for each at the end."
            with st.spinner("Generating quiz..."):
                quiz_response = call_gemini(prompt)
            st.success("Here is your Quiz:")
            st.write(quiz_response)
        else:
            st.warning("Please enter a topic for the quiz.")

# ----------------- FEATURE 4: SMART STUDY PLANNER -----------------
elif option == "Smart Study Planner":
    st.header("📅 Automated Study Planner")
    subject = st.text_input("Subject Name:")
    days_left = st.number_input("Days left for exam:", min_value=1, value=7)
    hours_per_day = st.number_input("Study hours per day:", min_value=1, value=3)
    
    if st.button("Generate Plan"):
        if subject:
            total_hours = days_left * hours_per_day
            st.info(f"Target: Spend **{total_hours} total hours** on {subject} over {days_left} days.")
            
            prompt = f"Create a daily study schedule for {subject} for {days_left} days with {hours_per_day} hours per day."
            with st.spinner("Generating plan..."):
                plan_text = call_gemini(prompt)
            st.write(plan_text)

# ----------------- FEATURE 5: NOTES MANAGER -----------------
elif option == "Notes Manager":
    st.header("📝 Smart Notes Management")
    
    note_title = st.text_input("Note Title:")
    note_content = st.text_area("Write Note Content:")
    
    if st.button("Save Note"):
        if note_title and note_content:
            new_note = {"title": note_title, "content": note_content, "date": str(datetime.date.today())}
            
            try:
                with open("notes.json", "r") as f:
                    notes = json.load(f)
            except FileNotFoundError:
                notes = []
                
            notes.append(new_note)
            with open("notes.json", "w") as f:
                json.dump(notes, f)
                
            st.success("Note saved successfully!")

    # Display Saved Notes
    st.subheader("Saved Notes")
    try:
        with open("notes.json", "r") as f:
            saved_notes = json.load(f)
            for n in saved_notes:
                with st.expander(f"{n['title']} ({n['date']})"):
                    st.write(n['content'])
                    if st.button("Summarize with AI", key=n['title']):
                        with st.spinner("Summarizing..."):
                            summary_text = call_gemini(f"Summarize this note: {n['content']}")
                        st.write("**Summary:**", summary_text)
    except FileNotFoundError:
        st.write("No notes saved yet.")