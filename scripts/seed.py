import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','pikestia.settings')
django.setup()
from apps.subjects.models import Subject, Topic
from apps.learning.models import LearningResource
from apps.practice.models import PracticeQuestion
from apps.opportunities.models import Opportunity
from django.utils import timezone

# Subjects
subjects_data = [
  ("Information Technology","IT","Information Technology"),
  ("Computer Science","CS","Computer Science"),
  ("Business Studies","BS","Business"),
  ("Engineering Fundamentals","EF","Engineering"),
]

for title, slug, disc in subjects_data:
    subj, _ = Subject.objects.get_or_create(slug=slug.lower(), defaults={"title":title, "discipline":disc, "description": f"{title} learning materials for university students", "icon":"📚"})

it = Subject.objects.get(slug='it')
cs = Subject.objects.get(slug='cs')

topics = [
  (it, "Programming Fundamentals", "prog-fund", "Variables, control flow, functions"),
  (it, "Web Development", "web-dev", "HTML, CSS, JS, Django basics"),
  (it, "Database Systems", "databases", "Relational design, SQL, normalization"),
  (cs, "Data Structures", "data-structures", "Arrays, lists, stacks, queues, trees"),
  (cs, "Algorithms", "algorithms", "Sorting, searching, complexity"),
]

for subj, ttitle, tslug, summary in topics:
    topic, _ = Topic.objects.get_or_create(subject=subj, slug=tslug, defaults={"title":ttitle, "summary":summary, "learning_objectives":"Understand concepts
Apply examples
Practice exercises"})

    # resource
    if not topic.resources.exists():
        LearningResource.objects.create(
            topic=topic,
            title=f"Introduction to {ttitle}",
            slug=f"intro-{tslug}",
            summary=f"Comprehensive guide to {ttitle} for university students.",
            objectives="Understand core concepts
Identify key terminology
Apply in practical exercises",
            content_raw=f"<h2>Introduction</h2><p>This material covers {ttitle}. {summary}</p><h3>Learning Objectives</h3><ul><li>Understand fundamentals</li><li>Apply knowledge</li></ul><h3>Example</h3><pre><code>// Example code for {ttitle}</code></pre><h3>Summary</h3><p>Master {ttitle} through practice and revision.</p>",
            key_concepts=f"{ttitle}, fundamentals, university level",
            status="published"
        )
        PracticeQuestion.objects.create(
            topic=topic,
            type="mcq",
            question=f"What is the primary purpose of {ttitle}?",
            options=["To confuse students","To build foundational understanding","To waste time","None"],
            correct_answer="To build foundational understanding",
            explanation=f"{ttitle} builds core understanding needed for advanced topics.",
            difficulty="easy"
        )

# opportunity
if not Opportunity.objects.exists():
    Opportunity.objects.create(
        title="Pikestia Hackathon 2026 - Student Innovators",
        slug="pikestia-hackathon-2026",
        description="Build solutions for education. Open to all university students.",
        category="hackathon",
        eligibility="University student, team of 2-4",
        location="Kampala, Uganda",
        is_remote=False,
        source_url="https://example.com/hackathon",
        source_name="Pikestia",
        is_verified=True,
        deadline=timezone.now() + timezone.timedelta(days=60),
        status="active"
    )

print("Seed complete")
