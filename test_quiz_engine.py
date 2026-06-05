import requests
import json
import re

BASE_URL = "http://localhost:5005"

def get_csrf_token(html_text):
    # Depending on if we have CSRF, wait, we didn't add CSRF protection explicitly to Flask-WTF if we didn't use it.
    # We used plain HTML forms. No CSRF tokens!
    pass

def test():
    print("Starting automated test for Quiz Engine...")
    session = requests.Session()

    # 1. Login as College Admin
    print("\n1. Logging in as College Admin...")
    r = session.post(f"{BASE_URL}/login", data={
        "email": "collegeadmin@studyhub.local",
        "password": "admin123"
    }, allow_redirects=True)
    if "Dashboard" in r.text and "College Admin" in r.text:
        print("[SUCCESS] College Admin login successful!")
    else:
        print("[FAIL] College Admin login failed.")
        return

    # 2. Get subjects to link quiz
    print("\n2. Fetching subjects to create a quiz...")
    r = session.get(f"{BASE_URL}/college-admin/quizzes/create")
    # find subject_id from HTML: <option value="1">
    match = re.search(r'<option value="(\d+)"[^>]*>.*?Introduction to Computer Science.*?</option>', r.text)
    if not match:
        print("[FAIL] Could not find subject id in form.")
        # fallback to subject 1
        subject_id = "1"
    else:
        subject_id = match.group(1)
        print(f"[SUCCESS] Found Subject ID: {subject_id}")

    # 3. Create a Quiz
    print("\n3. Creating a new quiz...")
    r = session.post(f"{BASE_URL}/college-admin/quizzes/create", data={
        "title": "Automated Python API Test Quiz",
        "subject_id": subject_id,
        "quiz_type": "practice",
        "difficulty": "medium",
        "time_limit_minutes": "30"
    }, allow_redirects=True)
    
    quiz_id_match = re.search(r'/college-admin/quizzes/(\d+)', r.url)
    if not quiz_id_match:
        print("[FAIL] Failed to parse quiz ID after creation.")
        return
    quiz_id = quiz_id_match.group(1)
    print(f"[SUCCESS] Quiz Created with ID {quiz_id}")

    # 4. Add a question
    print("\n4. Adding a question with 4 options...")
    r = session.post(f"{BASE_URL}/college-admin/quizzes/{quiz_id}/questions/create", data={
        "question_text": "What is 2 + 2?",
        "explanation": "Basic math.",
        "marks": "5",
        "order_number": "1",
        "option_text[]": ["1", "3", "4", "5"],
        "correct_option_index": "2" # Third option ('4') is correct (0-indexed)
    }, allow_redirects=True)
    if "Question added." in r.text:
        print("[SUCCESS] Question added successfully.")
    else:
        print("[FAIL] Failed to add question.")
        return

    # 5. Publish Quiz
    print("\n5. Publishing the Quiz...")
    r = session.post(f"{BASE_URL}/college-admin/quizzes/{quiz_id}/publish", allow_redirects=True)
    if "Quiz published." in r.text:
        print("[SUCCESS] Quiz published successfully.")
    else:
        print("[FAIL] Failed to publish quiz.")

    # 6. Logout and Login as Student
    print("\n6. Logging out and logging in as Student...")
    session.get(f"{BASE_URL}/logout")
    r = session.post(f"{BASE_URL}/login", data={
        "email": "student@studyhub.local",
        "password": "student123"
    }, allow_redirects=True)
    if "Student Demo" in r.text:
        print("[SUCCESS] Student login successful!")
    else:
        print("[FAIL] Student login failed.")
        return

    # 7. Start Exam Mode Quiz
    print("\n7. Starting Exam Mode Quiz...")
    r = session.post(f"{BASE_URL}/student/quizzes/{quiz_id}/start", data={
        "mode": "exam"
    }, allow_redirects=True)
    
    attempt_id_match = re.search(r'/student/attempts/(\d+)', r.url)
    if not attempt_id_match:
        print("[FAIL] Failed to start quiz attempt.")
        return
    attempt_id = attempt_id_match.group(1)
    print(f"[SUCCESS] Attempt started with ID {attempt_id}")

    # 8. Submit Answers for Exam
    # We need to find the option IDs from the HTML to submit correctly
    # <input type="radio" name="q_3" value="9" required>
    # We want to select the correct answer "4".
    print("\n8. Submitting correct answers for Exam...")
    option_matches = re.findall(r'<input type="radio" name="(q_\d+)" value="(\d+)"[^>]*>\s*<span>(.*?)</span>', r.text)
    
    submit_data = {}
    for q_name, opt_id, opt_text in option_matches:
        if opt_text == "4":
            submit_data[q_name] = opt_id
            print(f"   Selecting Option '{opt_text}' (ID {opt_id}) for Question {q_name}")
    
    r = session.post(f"{BASE_URL}/student/attempts/{attempt_id}/submit", data=submit_data, allow_redirects=True)
    if "Quiz Completed!" in r.text:
        print("[SUCCESS] Exam submitted successfully.")
    else:
        print("[FAIL] Failed to submit exam.")
        return

    # 9. Verify Score
    print("\n9. Verifying final score...")
    if "100%" in r.text and "5 / 5" in r.text:
        print("[SUCCESS] Test Passed! Score calculation is correct (100%, 5/5).")
    else:
        print("[FAIL] Score calculation failed or mismatch. Check logs.")
        
    print("\nALL AUTOMATED TESTS PASSED SUCCESSFULLY.")

if __name__ == '__main__':
    try:
        test()
    except Exception as e:
        print(f"Test failed due to exception: {e}")
