# Pikestia Learning Content Guide

This guide defines how to organise material in the Pikestia administration area. The aim is a reliable curriculum that students can follow in order, rather than a collection of unrelated pages.

## 1. Use the catalogue hierarchy consistently

Use each field for one purpose:

1. **Discipline** — the broad academic group, such as **Science & Technology**, **Business**, or **Humanities**.
2. **Subject** — the field of study within that group, such as **Information Technology**.
3. **Main topic** — a coherent course or learning pathway inside the subject, such as **Web Design**.
4. **Subtopic** — a teachable unit inside the main topic, such as **HTML Fundamentals**.
5. **Learning material** — one focused lesson attached to a subtopic. Give each lesson a clear position using its **Order** value.
6. **Practice question** — an exercise attached to the same subtopic as the skill it checks.

Example catalogue:

    Science & Technology                      Discipline
    └── Information Technology                Subject
        └── Web Design                        Main topic
            ├── Web Concepts and Setup        Subtopic, Order 1
            │   ├── How the Web Works         Lesson, Order 1
            │   └── Setting Up a First Page   Lesson, Order 2
            ├── HTML Fundamentals             Subtopic, Order 2
            │   ├── Document Structure        Lesson, Order 1
            │   ├── Headings, Links and Lists Lesson, Order 2
            │   └── Images and Accessible Text Lesson, Order 3
            ├── CSS Fundamentals              Subtopic, Order 3
            ├── Layout and Responsive Design  Subtopic, Order 4
            ├── Accessibility and Usability   Subtopic, Order 5
            ├── JavaScript Fundamentals       Subtopic, Order 6
            └── Build and Publish a Website   Subtopic, Order 7

These are suggested course headings, not a claim that the corresponding content is already in the database. Create and publish only material that has been written and reviewed.

### Important administration rules

- Set **Discipline** before creating subjects. Use the same spelling for subjects in the same academic group.
- Create a main topic with **Parent topic** left empty.
- Create a subtopic by selecting the appropriate main topic in **Parent topic**.
- Keep a parent and its children in the same subject.
- Do not place a subtopic underneath another subtopic. Pikestia supports one grouping level below a main topic.
- Give lessons sequential **Order** values: 1, 2, 3, and so on. Do not rely on the title alphabetically to teach a skill.
- Attach practice questions to the subtopic whose material prepares students to answer them.
- Keep unfinished material as **Draft**. Publish a topic only when its page has enough explanation, resources, and practice to be useful.

## 2. Write lessons students can actually study

A learning material should teach one manageable idea. Avoid titles such as “Introduction”, “Notes”, “Topic 1”, or “More about computers” unless the scope is clearly explained.

Fill these fields:

- **Title:** specific and searchable; for example, “HTML Document Structure”.
- **Summary:** one or two plain sentences saying what the lesson teaches and why it matters.
- **Objectives:** 2–5 observable outcomes, one per line. Start with verbs such as *identify*, *explain*, *compare*, *design*, *write*, or *test*.
- **Key concepts:** separate concise terms with commas. Include the words a student might reasonably search for.
- **Order:** where the lesson belongs within its subtopic.
- **Content:** a complete explanation with practical examples, not only a list of definitions.

### Recommended lesson sequence

Use the parts that genuinely help the subject; do not add headings merely to make every page look identical.

1. **Purpose and context.** Explain the problem or idea in straightforward language.
2. **Prerequisites.** Mention what the learner should already know, if anything.
3. **Explanation.** Introduce terms, principles and steps in an order that builds understanding.
4. **Worked example.** Walk through a realistic example and explain why each step is taken.
5. **Common mistakes or comparison.** Explain mistakes the learner is likely to make and how to avoid them.
6. **Try it.** Give the learner a small task or reflection question. Link to the matching practice section where appropriate.
7. **Recap.** Restate the central ideas briefly and point to the next lesson.

For technical subjects, include code samples, tables or diagrams where they make the idea easier to understand. Explain the sample instead of leaving it unexplained. Use meaningful alternative text for images. Check that links work and the lesson remains readable on a phone.

## 3. Content quality and publishing checklist

Before setting a lesson to **Published**, check:

- [ ] The lesson belongs to the correct subject, main topic and subtopic.
- [ ] The title identifies the actual skill or concept.
- [ ] The summary, objectives and key concepts are complete and accurate.
- [ ] The explanation is in your own clear words and suits the intended learner.
- [ ] Examples work, code is formatted, diagrams have alternative text, and links lead to useful resources.
- [ ] Practice questions assess the stated objectives and do not reveal answers before submission.
- [ ] Spelling, grammar, headings and lesson order have been checked.
- [ ] Sources are recorded where needed, and third-party material is used within its licence or permission.
- [ ] A second person has reviewed the material where possible.

Do not copy an entire lesson from another platform. Use reputable sources to check facts, then write an original explanation and attribute external references where appropriate.

## 4. Search and recommendations

Search uses lesson titles, summaries, objectives, key concepts, lesson body, topic information and subject group. To make material discoverable, include the terms students actually use naturally in these fields.

Use **Featured** only for a small selection of dependable starting lessons. Featured lessons appear in recommendation areas first; if there are fewer than the available recommendation slots, the remaining places are filled by published lessons in curriculum order. This fallback is deliberate and is not personalised to a student's ability.

## 5. Keeping the catalogue healthy

Use the administration dashboard's **Catalogue quality** section to find:

- published subjects with no published main topics;
- published topics with neither lessons nor subtopics;
- published lessons missing a summary, objectives or key concepts.

Review these counts after adding or reorganising a course. The counters identify likely gaps; an editor must still read the content and judge its quality.

## Reference principles

Pikestia's curriculum organisation takes inspiration from public learning resources that separate beginner foundations, core skills, practice and more advanced extensions. The structure is informed by the [MDN Curriculum](https://developer.mozilla.org/en-US/curriculum/) and its [Learn Web Development pathways](https://developer.mozilla.org/en-US/docs/Learn_web_development). Pikestia should use these as quality references, not copy their lesson text.
