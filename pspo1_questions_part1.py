#!/usr/bin/env python3
"""
Add large batch of PSPO1 questions to database - Part 1
"""

# Extended PSPO1 Questions Set 1 (Questions 21-70)
questions_part1 = [
    # Product Backlog Management (21-35)
    {
        "text": "What is the purpose of a Product Backlog?",
        "choices": ["To list all features that will ever be developed", "To provide a detailed plan for the next release", "To serve as a single source of requirements for any changes to be made to the product", "To document all defects found during testing"],
        "correct": [2]
    },
    {
        "text": "Who can add items to the Product Backlog?",
        "choices": ["Only the Product Owner", "Only the Scrum Master", "Anyone, but the Product Owner remains accountable", "Only the Development Team"],
        "correct": [2]
    },
    {
        "text": "What is Product Backlog refinement?",
        "choices": ["A Sprint event that happens at the end of the Sprint", "The act of breaking down and further defining Product Backlog items", "A meeting where only the Product Owner participates", "The process of removing old items from the Product Backlog"],
        "correct": [1]
    },
    {
        "text": "True or False: Product Backlog items must have estimates before they can be selected for a Sprint.",
        "choices": ["True", "False"],
        "correct": [1]
    },
    {
        "text": "What variables should a Product Owner consider when ordering the Product Backlog?",
        "choices": ["Value, risk, dependencies, and learning opportunities", "Only business value", "Technical difficulty only", "Team preferences"],
        "correct": [0]
    },
    {
        "text": "How often should Product Backlog refinement occur?",
        "choices": ["Once per Sprint", "Continuously throughout the Sprint", "Only during Sprint Planning", "At the end of each Sprint"],
        "correct": [1]
    },
    {
        "text": "What percentage of the Development Team's capacity should be spent on Product Backlog refinement?",
        "choices": ["Exactly 10%", "No more than 10%", "At least 20%", "As much as needed"],
        "correct": [1]
    },
    {
        "text": "True or False: The Product Owner can delegate writing Product Backlog items to others.",
        "choices": ["True", "False"],
        "correct": [0]
    },
    {
        "text": "What makes a Product Backlog item ready for selection in Sprint Planning?",
        "choices": ["It has been estimated", "It has acceptance criteria", "It can be completed within one Sprint", "All of the above"],
        "correct": [3]
    },
    {
        "text": "Who is responsible for the size estimates of Product Backlog items?",
        "choices": ["The Product Owner", "The Scrum Master", "The Development Team", "The Project Manager"],
        "correct": [2]
    },
    {
        "text": "What should happen to undone Product Backlog items at the end of a Sprint?",
        "choices": ["They are automatically moved to the next Sprint", "They are put back on the Product Backlog", "They are removed from the product", "They are marked as defects"],
        "correct": [1]
    },
    {
        "text": "True or False: The Product Backlog should contain tasks for the Development Team.",
        "choices": ["True", "False"],
        "correct": [1]
    },
    {
        "text": "What is the relationship between Product Backlog items and user stories?",
        "choices": ["They are the same thing", "User stories are a format for Product Backlog items", "Product Backlog items are more detailed than user stories", "They are completely different"],
        "correct": [1]
    },
    {
        "text": "Who decides the order of Product Backlog items during refinement?",
        "choices": ["The Development Team", "The Scrum Master", "The Product Owner", "The stakeholders"],
        "correct": [2]
    },
    {
        "text": "What happens when a Product Backlog item cannot be completed within one Sprint?",
        "choices": ["The Sprint is extended", "The item is removed from the Sprint", "The item is broken down into smaller items", "The Definition of Done is changed"],
        "correct": [2]
    },
    
    # Sprint Planning & Goals (36-50)
    {
        "text": "Who creates the Sprint Goal?",
        "choices": ["The Product Owner", "The Scrum Master", "The Development Team", "The Scrum Team"],
        "correct": [3]
    },
    {
        "text": "What is the purpose of the Sprint Goal?",
        "choices": ["To provide guidance to the Development Team on why it is building the increment", "To define exactly what will be delivered", "To ensure all Product Backlog items are completed", "To prevent any changes during the Sprint"],
        "correct": [0]
    },
    {
        "text": "True or False: The Product Owner must be present during Sprint Planning.",
        "choices": ["True", "False"],
        "correct": [0]
    },
    {
        "text": "What is the maximum duration of Sprint Planning for a one-month Sprint?",
        "choices": ["4 hours", "8 hours", "1 day", "2 days"],
        "correct": [1]
    },
    {
        "text": "Who determines how much work can be accomplished in a Sprint?",
        "choices": ["The Product Owner", "The Scrum Master", "The Development Team", "Management"],
        "correct": [2]
    },
    {
        "text": "What are the topics addressed in Sprint Planning?",
        "choices": ["What can be delivered and how the work will be achieved", "Only what will be delivered", "Only how the work will be done", "The team's velocity"],
        "correct": [0]
    },
    {
        "text": "True or False: The Sprint Goal can be changed during the Sprint.",
        "choices": ["True", "False"],
        "correct": [1]
    },
    {
        "text": "Who selects the Product Backlog items for the Sprint?",
        "choices": ["The Product Owner", "The Development Team", "The Scrum Master", "The Product Owner and Development Team together"],
        "correct": [3]
    },
    {
        "text": "What should the Development Team do when they realize they have overcommitted during Sprint Planning?",
        "choices": ["Work overtime to complete everything", "Extend the Sprint", "Renegotiate the scope with the Product Owner", "Cancel the Sprint"],
        "correct": [2]
    },
    {
        "text": "True or False: Sprint Planning should result in a detailed plan for the entire Sprint.",
        "choices": ["True", "False"],
        "correct": [1]
    },
    {
        "text": "What is the Sprint Backlog?",
        "choices": ["A subset of the Product Backlog", "The plan for delivering the Sprint Goal", "A list of tasks to complete Product Backlog items", "All of the above"],
        "correct": [3]
    },
    {
        "text": "Who owns the Sprint Backlog?",
        "choices": ["The Product Owner", "The Scrum Master", "The Development Team", "The entire Scrum Team"],
        "correct": [2]
    },
    {
        "text": "When can the Sprint Backlog be updated?",
        "choices": ["Only during Sprint Planning", "Only during the Daily Scrum", "Throughout the Sprint", "Only at the end of the Sprint"],
        "correct": [2]
    },
    {
        "text": "True or False: The Product Owner can add items to the Sprint Backlog during the Sprint.",
        "choices": ["True", "False"],
        "correct": [1]
    },
    {
        "text": "What happens if the Development Team cannot complete all Sprint Backlog items?",
        "choices": ["The Sprint is considered failed", "The unfinished items go back to the Product Backlog", "The Sprint is extended", "The team works overtime"],
        "correct": [1]
    },
    
    # Increment & Definition of Done (51-65)
    {
        "text": "What is an Increment in Scrum?",
        "choices": ["A plan for the next Sprint", "The sum of all Product Backlog items completed during a Sprint", "A meeting to inspect the product", "The sum of all completed and valuable Product Backlog items since the beginning of the project"],
        "correct": [3]
    },
    {
        "text": "Who is responsible for the Definition of Done?",
        "choices": ["The Product Owner", "The Scrum Master", "The Development Team", "The organization or the Scrum Team if not defined by the organization"],
        "correct": [3]
    },
    {
        "text": "True or False: An Increment must be released to production at the end of each Sprint.",
        "choices": ["True", "False"],
        "correct": [1]
    },
    {
        "text": "What must be true about every Increment?",
        "choices": ["It must be potentially releasable", "It must be released", "It must be perfect", "It must include all planned features"],
        "correct": [0]
    },
    {
        "text": "Who decides when to release the Increment?",
        "choices": ["The Scrum Master", "The Development Team", "The Product Owner", "The stakeholders"],
        "correct": [2]
    },
    {
        "text": "What is the relationship between Definition of Done and acceptance criteria?",
        "choices": ["They are the same thing", "Definition of Done is more general than acceptance criteria", "Acceptance criteria is more general than Definition of Done", "They are unrelated"],
        "correct": [1]
    },
    {
        "text": "True or False: The Definition of Done can be improved during the Sprint Retrospective.",
        "choices": ["True", "False"],
        "correct": [0]
    },
    {
        "text": "What happens when a Product Backlog item does not meet the Definition of Done?",
        "choices": ["It is included in the Increment anyway", "It cannot be released", "It is automatically moved to the next Sprint", "The Definition of Done is lowered"],
        "correct": [1]
    },
    {
        "text": "Who ensures that the Definition of Done is understood?",
        "choices": ["The Product Owner", "The Scrum Master", "The Development Team", "All team members"],
        "correct": [3]
    },
    {
        "text": "True or False: Multiple Scrum Teams working on the same product should have the same Definition of Done.",
        "choices": ["True", "False"],
        "correct": [0]
    },
    {
        "text": "What should happen if the Definition of Done for an increment is part of the organizational standard?",
        "choices": ["The Scrum Team must follow it exactly", "The Scrum Team can ignore it", "The Scrum Team can supplement it", "The Scrum Team should create their own"],
        "correct": [2]
    },
    {
        "text": "When should the Definition of Done be created?",
        "choices": ["During the first Sprint", "Before the first Sprint Planning", "During Sprint Planning", "After the first Sprint Review"],
        "correct": [1]
    },
    {
        "text": "True or False: The Definition of Done should include performance criteria.",
        "choices": ["True", "False"],
        "correct": [0]
    },
    {
        "text": "Who can suggest changes to the Definition of Done?",
        "choices": ["Only the Product Owner", "Only the Development Team", "Anyone on the Scrum Team", "Only the Scrum Master"],
        "correct": [2]
    },
    {
        "text": "What is the minimum frequency for updating the Definition of Done?",
        "choices": ["Every Sprint", "Every release", "As needed", "Never"],
        "correct": [2]
    }
]

print(f"Prepared {len(questions_part1)} questions for addition to database")