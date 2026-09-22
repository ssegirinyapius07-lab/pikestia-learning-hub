from django.db import migrations


QUESTIONS = [
    {
        "type": "mcq",
        "question": "What is the main purpose of HTML in web development?",
        "options": [
            "To structure the content of a web page",
            "To style a web page",
            "To store data in a database",
            "To manage network traffic",
        ],
        "correct_answer": "To structure the content of a web page",
        "explanation": "HTML defines the structure and meaning of web content, such as headings, paragraphs, links, images and forms.",
        "difficulty": "easy",
    },
    {
        "type": "mcq",
        "question": "Which HTML element is normally used for the main heading of a page?",
        "options": ["<h1>", "<head>", "<title>", "<heading>"],
        "correct_answer": "<h1>",
        "explanation": "The h1 element represents the highest-level heading in the page content.",
        "difficulty": "easy",
    },
    {
        "type": "mcq",
        "question": "What does CSS primarily control?",
        "options": [
            "The presentation and layout of web pages",
            "The structure of database tables",
            "The server's operating system",
            "The domain name of a website",
        ],
        "correct_answer": "The presentation and layout of web pages",
        "explanation": "CSS controls presentation, including typography, spacing, colors, sizing and responsive layouts.",
        "difficulty": "easy",
    },
    {
        "type": "mcq",
        "question": "Which HTML element creates a hyperlink?",
        "options": ["<a>", "<link>", "<href>", "<url>"],
        "correct_answer": "<a>",
        "explanation": "The anchor element, <a>, creates hyperlinks. Its href attribute specifies the destination.",
        "difficulty": "easy",
    },
    {
        "type": "mcq",
        "question": "Which attribute specifies the destination of an HTML hyperlink?",
        "options": ["src", "href", "link", "target"],
        "correct_answer": "href",
        "explanation": "The href attribute contains the URL or other destination that the link points to.",
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
        "type": "mcq",
        "question": "What is responsive web design intended to achieve?",
        "options": [
            "A layout that adapts to different screen sizes and devices",
            "A website that only works on desktop computers",
            "A website with no images",
            "A website that never uses CSS",
        ],
        "correct_answer": "A layout that adapts to different screen sizes and devices",
        "explanation": "Responsive design uses flexible layouts and techniques such as media queries to provide a usable experience across devices.",
        "difficulty": "medium",
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
        "type": "short",
        "question": "What does HTML stand for?",
        "options": [],
        "correct_answer": "HyperText Markup Language",
        "explanation": "HTML stands for HyperText Markup Language. It is used to structure content on the web.",
        "difficulty": "easy",
    },
    {
        "type": "short",
        "question": "What does CSS stand for?",
        "options": [],
        "correct_answer": "Cascading Style Sheets",
        "explanation": "CSS stands for Cascading Style Sheets and is used to control the presentation of HTML documents.",
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
        "question": "Name one technology commonly used to add interactivity to web pages.",
        "options": [],
        "correct_answer": "JavaScript",
        "explanation": "JavaScript is widely used to add dynamic behavior and interactivity to web pages.",
        "difficulty": "easy",
    },
    {
        "type": "short",
        "question": "What is a web browser?",
        "options": [],
        "correct_answer": "Software used to access and display web pages",
        "explanation": "A web browser retrieves web resources and renders them for the user. Examples include browsers such as Chrome, Edge and Firefox.",
        "difficulty": "easy",
    },
    {
        "type": "exercise",
        "question": "Exercise: Describe how HTML, CSS and JavaScript work together when building a web page.",
        "options": [],
        "correct_answer": "HTML provides structure, CSS controls presentation and JavaScript adds behavior or interactivity.",
        "explanation": "A typical web page uses HTML for semantic structure, CSS for visual presentation and JavaScript for behavior and dynamic interaction.",
        "difficulty": "medium",
    },
    {
        "type": "exercise",
        "question": "Exercise: Explain why a developer should consider mobile devices when designing a web page.",
        "options": [],
        "correct_answer": "Because users access websites on different screen sizes, so the layout should remain usable and readable across devices.",
        "explanation": "Considering mobile devices helps developers create responsive interfaces with appropriate sizing, spacing, navigation and readable content.",
        "difficulty": "medium",
    },
]


def seed_practice_questions(apps, schema_editor):
    Topic = apps.get_model("subjects", "Topic")
    PracticeQuestion = apps.get_model("practice", "PracticeQuestion")

    topic = Topic.objects.filter(
        slug="web-development",
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
        topic__slug="web-development",
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("practice", "0001_initial"),
        ("subjects", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            seed_practice_questions,
            remove_practice_questions,
        ),
    ]
