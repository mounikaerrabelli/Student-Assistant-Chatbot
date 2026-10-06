from django.shortcuts import render, redirect
from .models import ChatHistory, Student


# ---------------- LOGIN ----------------

def login_view(request):
    error = ""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        student = Student.objects.filter(
            username=username,
            password=password
        ).first()

        if student:
            request.session["student_id"] = student.id
            request.session["username"] = student.username
            return redirect("home")
        else:
            error = "Invalid username or password."

    return render(
        request,
        "login.html",
        {"error": error}
    )


# ---------------- LOGOUT ----------------

def logout_view(request):
    request.session.flush()
    return redirect("login")


# ---------------- CHATBOT ----------------

def home(request):

    if "student_id" not in request.session:
        return redirect("login")

    answer = ""

    if request.method == "POST":

        question = request.POST.get("question", "").lower()
        subject = request.POST.get("subject", "")

        if subject == "Python":

            if "what is" in question or "python" in question:
                answer = "Python is a simple and powerful programming language."
            else:
                answer = "Python is used for programming, automation, web development, data science, and AI."

        elif subject == "DBMS":

            if "normalization" in question:
                answer = "Normalization is the process of organizing data in a database to reduce redundancy and improve data consistency."
            else:
                answer = "DBMS is software used to store, manage, and retrieve data efficiently."

        elif subject == "Java":

            if "oop" in question:
                answer = "OOP stands for Object-Oriented Programming. Java uses classes and objects along with inheritance, polymorphism, abstraction, and encapsulation."
            else:
                answer = "Java is an object-oriented programming language used to develop many types of applications."

        elif subject == "Machine Learning":

            answer = "Machine Learning is a branch of Artificial Intelligence that allows computers to learn patterns from data and make predictions."

        elif subject == "Computer Networks":

            answer = "A Computer Network is a group of connected computers and devices that communicate and share data and resources."

        else:

            answer = "Please select a subject and ask your question."

        ChatHistory.objects.create(
            subject=subject,
            question=question,
            answer=answer
        )

    history = ChatHistory.objects.order_by("-created_at")

    username = request.session.get("username")

    return render(
        request,
        "home.html",
        {
            "answer": answer,
            "history": history,
            "username": username
        }
    )


# ---------------- QUIZ ----------------

def quiz(request):

    if "student_id" not in request.session:
        return redirect("login")

    score = None

    if request.method == "POST":

        score = 0

        if request.POST.get("q1") == "python":
            score += 1

        if request.POST.get("q2") == "#":
            score += 1

        return render(
            request,
            "quiz.html",
            {
                "score": score
            }
        )

    return render(
        request,
        "quiz.html",
        {
            "score": None
        }
    )


# ---------------- DASHBOARD ----------------

def dashboard(request):

    if "student_id" not in request.session:
        return redirect("login")

    username = request.session.get("username")

    total_questions = ChatHistory.objects.count()

    python_questions = ChatHistory.objects.filter(
        subject="Python"
    ).count()

    dbms_questions = ChatHistory.objects.filter(
        subject="DBMS"
    ).count()

    java_questions = ChatHistory.objects.filter(
        subject="Java"
    ).count()

    return render(
        request,
        "dashboard.html",
        {
            "username": username,
            "total_questions": total_questions,
            "python_questions": python_questions,
            "dbms_questions": dbms_questions,
            "java_questions": java_questions
        }
    )


# ---------------- STUDY MATERIALS ----------------

def materials(request):

    if "student_id" not in request.session:
        return redirect("login")

    return render(
        request,
        "materials.html"
    )

