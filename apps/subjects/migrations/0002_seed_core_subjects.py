from django.db import migrations


SUBJECTS = [
    {
        "title": "Computer Science",
        "slug": "computer-science",
        "description": "Core computing concepts including algorithms, programming, software development and computer systems.",
        "discipline": "Computer Science",
        "icon": "code",
        "order": 20,
    },
    {
        "title": "Computer Networks",
        "slug": "computer-networks",
        "description": "Learning resources covering network concepts, communication, protocols, addressing and network security fundamentals.",
        "discipline": "Information Technology",
        "icon": "network",
        "order": 30,
    },
    {
        "title": "Database Systems",
        "slug": "database-systems",
        "description": "Study relational databases, data modelling, SQL, database design and practical data management.",
        "discipline": "Information Technology",
        "icon": "database",
        "order": 40,
    },
    {
        "title": "Cybersecurity",
        "slug": "cybersecurity",
        "description": "Explore cybersecurity principles, threats, protection techniques, security awareness and incident response.",
        "discipline": "Information Technology",
        "icon": "shield",
        "order": 50,
    },
    {
        "title": "Business Administration",
        "slug": "business-administration",
        "description": "University learning resources covering management, entrepreneurship, business operations and organisational principles.",
        "discipline": "Business",
        "icon": "briefcase",
        "order": 60,
    },
    {
        "title": "Mathematics",
        "slug": "mathematics",
        "description": "Foundational and university-level mathematics resources for problem solving, quantitative reasoning and academic study.",
        "discipline": "Mathematics",
        "icon": "calculator",
        "order": 70,
    },
]


def seed_subjects(apps, schema_editor):
    Subject = apps.get_model("subjects", "Subject")

    for data in SUBJECTS:
        Subject.objects.update_or_create(
            slug=data["slug"],
            defaults={
                "title": data["title"],
                "description": data["description"],
                "discipline": data["discipline"],
                "icon": data["icon"],
                "order": data["order"],
                "status": "published",
            },
        )


def unseed_subjects(apps, schema_editor):
    Subject = apps.get_model("subjects", "Subject")
    Subject.objects.filter(
        slug__in=[subject["slug"] for subject in SUBJECTS]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("subjects", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_subjects, unseed_subjects),
    ]
