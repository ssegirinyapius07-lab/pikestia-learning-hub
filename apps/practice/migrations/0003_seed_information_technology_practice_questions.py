from django.db import migrations


QUESTIONS = [
    {
        "type": "mcq",
        "question": "What is the main purpose of HTML in web development?",
        "options": ["To structure the content of a web page", "To style a web page", "To store data in a database", "To manage network traffic"],
        "correct_answer": "To structure the content of a web page",
        "explanation": "HTML defines the structure and meaning of web content, including headings, paragraphs, links and other elements.",
        "difficulty": "easy",
    },
    {
        "type": "mcq",
        "question": "Which technology is primarily responsible for the visual presentation of a web page?",
        "options": ["HTML", "CSS", "JavaScript", "SQL"],
        "correct_answer": "CSS",
        "explanation": "CSS controls presentation such as typography, spacing, sizing, layout and other visual styles.",
        "difficulty": "easy",
    },
    {
        "type": "mcq",
        "question": "Which technology is commonly used to add behavior and interactivity to web pages?",
        "options": ["HTML", "CSS", "JavaScript", "HTTP"],
        "correct_answer": "JavaScript",
        "explanation": "JavaScript can respond to user actions and change page behavior dynamically.",
        "difficulty": "easy",
    },
    {
        "type": "mcq",
        "question": "Which HTML element represents the main heading of a page or section?",
        "options": ["<h1>", "<head>", "<title>", "<heading>"],
        "correct_answer": "<h1>",
        "explanation": "The h1 element represents the highest-level heading in the document content.",
        "difficulty": "easy",
    },
    {
        "type": "mcq",
        "question": "Which HTML element is used to create a paragraph?",
        "options": ["<paragraph>", "<p>", "<text>", "<para>"],
        "correct_answer": "<p>",
        "explanation": "The p element represents a paragraph of text.",
        "difficulty": "easy",
    },
    {
        "type": "mcq",
        "question": "Which HTML element creates a hyperlink?",
        "options": ["<a>", "<link>", "<href>", "<url>"],
        "correct_answer": "<a>",
        "explanation": "The anchor element, <a>, creates a hyperlink.",
        "difficulty": "easy",
    },
    {
        "type": "mcq",
        "question": "Which attribute specifies the destination of an HTML hyperlink?",
        "options": ["src", "href", "target", "link"],
        "correct_answer": "href",
        "explanation": "The href attribute specifies the URL or other destination of the link.",
        "difficulty": "easy",
    },
    {
        "type": "mcq",
        "question": "Which CSS property is commonly used to change the text color?",
        "options": ["font-color", "text-color", "color", "foreground"],
        "correct_answer": "color",
        "explanation": "The CSS color property sets the foreground color of text.",
        "difficulty": "easy",
    },
    {
        "type": "short",
        "question": "What does HTML stand for?",
        "options": [],
        "correct_answer": "HyperText Markup Language",
        "explanation": "HTML stands for HyperText Markup Language and is used to structure web content.",
        "difficulty": "easy",
    },
    {
        "type": "short",
        "question": "What does CSS stand for?",
        "options": [],
        "correct_answer": "Cascading Style Sheets",
        "explanation": "CSS stands for Cascading Style Sheets and controls the presentation of HTML documents.",
        "difficulty": "easy",
    },
    {
        "type": "short",
        "question": "What is the purpose of the href attribute in an anchor element?",
        "options": [],
        "correct_answer": "It specifies the destination URL of the link",
        "explanation": "The href attribute tells the browser where the hyperlink should navigate.",
        "difficulty": "medium",
    },
    {
        "type": "short",
        "question": "What is a web browser?",
        "options": [],
        "correct_answer": "Software used to access and display web pages",
        "explanation": "A web browser retrieves web resources and renders them for the user.",
        "difficulty": "easy",
    },
    {
        "type": "exercise",
        "question": "Exercise: Describe how HTML, CSS and JavaScript work together when building a web page.",
        "options": [],
        "correct_answer": "HTML provides structure, CSS controls presentation and JavaScript adds behavior or interactivity.",
        "explanation": "A typical page uses HTML for structure, CSS for presentation and JavaScript for behavior and dynamic interaction.",
        "difficulty": "medium",
    },
    {
        "type": "exercise",
        "question": "Exercise: Write a simple HTML example containing one main heading, one paragraph and a link.",
        "options": [],
        "correct_answer": "A correct answer should use <h1> for the heading, <p> for the paragraph and <a href=\"...\"> for the link.",
        "explanation": "The exercise checks whether you can apply the HTML elements covered in the learning materials.",
        "difficulty": "medium",
    },
    {
        "type": "exercise",
        "question": "Exercise: Explain why a web page should be designed to work on both mobile phones and larger screens.",
        "options": [],
        "correct_answer": "Because users access websites on different screen sizes, so the layout should remain readable, usable and adaptable across devices.",
        "explanation": "Responsive design helps a page adapt its layout and sizing to different devices and screen sizes.",
        "difficulty": "medium",
    },
]


def seed_practice_questions(apps, schema_editor):
    Topic = apps.get_model("subjects", "Topic")
    PracticeQuestion = apps.get_model("practice", "PracticeQuestion")

    topic = Topic.objects.filter(
        id=1,
        slug="information-technology",
        status="published",
    ).first()

    if not topic:
        return

    for item in QUESTIONS:
        PracticeQuestion.objects.get_or_create(
            topic=topic,
            question=item["question"],
            defaults={
                "type": item["type"],
                "options": item["options"],
                "correct_answer": item["correct_answer"],
                "explanation": item["explanation"],
                "difficulty": item["difficulty"],
                "status": "published",
            },
        )


def remove_practice_questions(apps, schema_editor):
    PracticeQuestion = apps.get_model("practice", "PracticeQuestion")
    questions = [item["question"] for item in QUESTIONS]
    PracticeQuestion.objects.filter(
        question__in=questions,
        topic__slug="information-technology",
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("practice", "0002_seed_web_development_questions"),
    ]

    operations = [
        migrations.RunPython(seed_practice_questions, remove_practice_questions),
    ]
