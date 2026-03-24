"""
knowledge_base.py — Static company/role/skill registry + eligibility requirements

This is the source of truth for:
- Company eligibility criteria (CGPA, branch, experience)
- Required skills per role
- Learning resources
- Interview question templates

To add more companies/roles: edit COMPANIES and LEARNING_RESOURCES.
"""

COMPANIES = {
    "Google": {
        "type": "Product",
        "requirements": {"min_cgpa": 7.0, "branches": [], "min_experience": 0},
        "roles": {
            "Software Engineer": ["Data Structures", "Algorithms", "System Design", "Python", "Java"],
            "ML Engineer": ["Machine Learning", "Deep Learning", "Python", "Statistics", "TensorFlow"],
            "Site Reliability Engineer": ["Linux", "Networking", "Python", "Docker", "Kubernetes"],
        },
    },
    "Amazon": {
        "type": "Product",
        "requirements": {"min_cgpa": 6.0, "branches": [], "min_experience": 0},
        "roles": {
            "Software Development Engineer": ["Data Structures", "Algorithms", "System Design", "Java", "SQL"],
            "Data Engineer": ["SQL", "Python", "AWS", "Data Pipelines", "Spark"],
            "Cloud Support Engineer": ["AWS", "Linux", "Networking", "Python"],
        },
    },
    "Meta": {
        "type": "Product",
        "requirements": {"min_cgpa": 7.5, "branches": [], "min_experience": 0},
        "roles": {
            "Software Engineer": ["Data Structures", "Algorithms", "System Design", "React", "Python"],
            "Research Engineer": ["Deep Learning", "PyTorch", "Python", "Mathematics", "Research Papers"],
        },
    },
    "Microsoft": {
        "type": "Product",
        "requirements": {"min_cgpa": 6.5, "branches": [], "min_experience": 0},
        "roles": {
            "Software Engineer": ["Data Structures", "Algorithms", "System Design", "C#", "Azure"],
            "Data Scientist": ["Python", "Machine Learning", "SQL", "Statistics", "Azure ML"],
        },
    },
    "Netflix": {
        "type": "Product",
        "requirements": {"min_cgpa": 7.0, "branches": [], "min_experience": 2},
        "roles": {
            "Senior Software Engineer": ["Data Structures", "Algorithms", "System Design", "Java", "Microservices"],
        },
    },
    "Flipkart": {
        "type": "E-Commerce",
        "requirements": {"min_cgpa": 6.0, "branches": ["CSE", "IT", "ECE"], "min_experience": 0},
        "roles": {
            "Software Development Engineer": ["Data Structures", "Algorithms", "Java", "System Design", "SQL"],
        },
    },
    "TCS": {
        "type": "Service",
        "requirements": {"min_cgpa": 6.0, "branches": [], "min_experience": 0},
        "roles": {
            "Software Developer": ["Java", "SQL", "Communication", "Problem Solving"],
            "Data Analyst": ["Python", "SQL", "Excel", "Statistics"],
        },
    },
    "Infosys": {
        "type": "Service",
        "requirements": {"min_cgpa": 6.0, "branches": [], "min_experience": 0},
        "roles": {
            "Systems Engineer": ["Java", "Python", "SQL", "Communication"],
            "Digital Specialist Engineer": ["Data Structures", "Algorithms", "Java", "Python"],
        },
    },
    "Razorpay": {
        "type": "Fintech",
        "requirements": {"min_cgpa": 6.5, "branches": [], "min_experience": 0},
        "roles": {
            "Software Development Engineer": ["Data Structures", "Algorithms", "Go", "Python", "System Design"],
        },
    },
    "Zomato": {
        "type": "Startup",
        "requirements": {"min_cgpa": 5.5, "branches": [], "min_experience": 0},
        "roles": {
            "Software Engineer": ["Python", "Data Structures", "Django", "System Design"],
        },
    },
}


LEARNING_RESOURCES = {
    "Data Structures": [
        {"title": "NeetCode DSA Roadmap", "url": "https://neetcode.io/roadmap", "type": "Interactive", "description": "Visual DSA learning path"},
        {"title": "LeetCode Explore", "url": "https://leetcode.com/explore/", "type": "Practice", "description": "Structured problem sets"},
        {"title": "GeeksForGeeks DSA", "url": "https://www.geeksforgeeks.org/data-structures/", "type": "Article", "description": "Detailed explanations with code"},
    ],
    "Algorithms": [
        {"title": "MIT OpenCourseWare 6.006", "url": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/", "type": "Course", "description": "MIT algorithms course"},
        {"title": "Abdul Bari Algorithms", "url": "https://www.youtube.com/channel/UCZCFT11CWBi3MHNlGf019nw", "type": "YouTube", "description": "Visual algorithm explanations"},
        {"title": "LeetCode Patterns", "url": "https://seanprashad.com/leetcode-patterns/", "type": "Practice", "description": "LeetCode problems by pattern"},
    ],
    "System Design": [
        {"title": "Grokking System Design", "url": "https://www.designgurus.io/course/grokking-the-system-design-interview", "type": "Course", "description": "Most popular system design course"},
        {"title": "System Design Primer", "url": "https://github.com/donnemartin/system-design-primer", "type": "GitHub", "description": "Free comprehensive guide on GitHub"},
        {"title": "ByteByteGo YouTube", "url": "https://www.youtube.com/@ByteByteGo", "type": "YouTube", "description": "Visual system design explanations"},
    ],
    "Python": [
        {"title": "Python Official Docs", "url": "https://docs.python.org/3/", "type": "Documentation", "description": "Official Python documentation"},
        {"title": "Real Python", "url": "https://realpython.com/", "type": "Article", "description": "In-depth Python tutorials"},
        {"title": "Python for Everybody", "url": "https://www.coursera.org/specializations/python", "type": "Course", "description": "Coursera beginner Python course"},
    ],
    "Machine Learning": [
        {"title": "Andrew Ng ML Course", "url": "https://www.coursera.org/specializations/machine-learning-introduction", "type": "Course", "description": "Stanford ML course on Coursera"},
        {"title": "Kaggle Learn", "url": "https://www.kaggle.com/learn", "type": "Interactive", "description": "Hands-on ML with notebooks"},
        {"title": "Hands-On ML Book", "url": "https://www.oreilly.com/library/view/hands-on-machine-learning/9781492032632/", "type": "Book", "description": "Aurélien Géron's classic ML book"},
    ],
    "SQL": [
        {"title": "SQLZoo", "url": "https://sqlzoo.net/", "type": "Interactive", "description": "Interactive SQL tutorialss"},
        {"title": "Mode SQL Tutorial", "url": "https://mode.com/sql-tutorial/", "type": "Article", "description": "Beginner to advanced SQL"},
        {"title": "LeetCode Database Problems", "url": "https://leetcode.com/problemset/database/", "type": "Practice", "description": "SQL interview questions"},
    ],
    "Java": [
        {"title": "Java Brains", "url": "https://www.youtube.com/@Java.Brains", "type": "YouTube", "description": "Core Java concepts"},
        {"title": "Effective Java", "url": "https://www.oreilly.com/library/view/effective-java/9780134686097/", "type": "Book", "description": "Best Java practices"},
        {"title": "Baeldung", "url": "https://www.baeldung.com/", "type": "Article", "description": "Java tutorials and Spring"},
    ],
    "React": [
        {"title": "React Official Docs", "url": "https://react.dev/", "type": "Documentation", "description": "Official React documentation"},
        {"title": "Full Stack Open", "url": "https://fullstackopen.com/", "type": "Course", "description": "Free full-stack course by Helsinki University"},
        {"title": "Scrimba React Course", "url": "https://scrimba.com/learn/learnreact", "type": "Interactive", "description": "Interactive React learning"},
    ],
    "Docker": [
        {"title": "Docker Getting Started", "url": "https://docs.docker.com/get-started/", "type": "Documentation", "description": "Official Docker tutorial"},
        {"title": "TechWorld with Nana Docker", "url": "https://www.youtube.com/watch?v=3c-iBn73dDE", "type": "YouTube", "description": "Docker full course"},
    ],
    "AWS": [
        {"title": "AWS Free Tier", "url": "https://aws.amazon.com/free/", "type": "Hands-on", "description": "Free AWS services for practice"},
        {"title": "AWS Skill Builder", "url": "https://skillbuilder.aws/", "type": "Course", "description": "Official AWS learning platform"},
        {"title": "A Cloud Guru", "url": "https://www.pluralsight.com/cloud-guru", "type": "Course", "description": "Cloud certification training"},
    ],
    "Deep Learning": [
        {"title": "fast.ai", "url": "https://www.fast.ai/", "type": "Course", "description": "Practical deep learning for coders"},
        {"title": "DeepLearning.AI Specialization", "url": "https://www.coursera.org/specializations/deep-learning", "type": "Course", "description": "Andrew Ng's DL specialization"},
        {"title": "PyTorch Tutorials", "url": "https://pytorch.org/tutorials/", "type": "Documentation", "description": "Official PyTorch guides"},
    ],
    "Statistics": [
        {"title": "StatQuest with Josh Starmer", "url": "https://www.youtube.com/@statquest", "type": "YouTube", "description": "Visual stats and ML explanations"},
        {"title": "Khan Academy Statistics", "url": "https://www.khanacademy.org/math/statistics-probability", "type": "Course", "description": "Free probability & statistics"},
    ],
    "Go": [
        {"title": "A Tour of Go", "url": "https://go.dev/tour/", "type": "Interactive", "description": "Official interactive Go tutorial"},
        {"title": "Go by Example", "url": "https://gobyexample.com/", "type": "Article", "description": "Practical Go examples"},
    ],
    "Kubernetes": [
        {"title": "Kubernetes Official Docs", "url": "https://kubernetes.io/docs/tutorials/", "type": "Documentation", "description": "Official K8s tutorials"},
        {"title": "TechWorld with Nana K8s", "url": "https://www.youtube.com/watch?v=X48VuDVv0do", "type": "YouTube", "description": "Kubernetes full course"},
    ],
}


INTERVIEW_QUESTION_TEMPLATES = {
    "easy": {
        "Arrays": [
            "What is the difference between an array and a linked list?",
            "How would you find the maximum element in an unsorted array?",
            "Explain what a two-pointer technique is with an example.",
        ],
        "Strings": [
            "How would you check if a string is a palindrome?",
            "What is the difference between String and StringBuilder in Java?",
            "How do you reverse words in a sentence without reversing characters?",
        ],
        "Python": [
            "What are Python list comprehensions? Give an example.",
            "Explain the difference between a list and a tuple in Python.",
            "What does the `*args` and `**kwargs` syntax mean in Python?",
        ],
    },
    "medium": {
        "Trees": [
            "Implement in-order traversal of a binary tree both recursively and iteratively.",
            "How would you check if two binary trees are identical?",
            "Explain the difference between DFS and BFS traversal of a tree.",
        ],
        "Dynamic Programming": [
            "Solve the 0/1 Knapsack problem and explain your approach.",
            "Describe the difference between top-down and bottom-up DP.",
            "How would you compute the Longest Common Subsequence of two strings?",
        ],
        "System Design": [
            "Design a URL shortener like bit.ly. What components are needed?",
            "How would you design the backend for a rate limiter?",
            "Explain what a CDN is and when you would use one.",
        ],
    },
    "hard": {
        "Graphs": [
            "Implement Dijkstra's algorithm and explain its time complexity.",
            "How would you detect a cycle in a directed graph? Explain two approaches.",
            "Solve the Minimum Spanning Tree problem. Compare Prim's vs Kruskal's.",
        ],
        "System Design": [
            "Design a distributed cache like Redis. How do you handle cache invalidation?",
            "How would you design a real-time messaging system that scales to 100M users?",
            "Explain consistent hashing and how it solves the distributed rebalancing problem.",
        ],
        "Concurrency": [
            "Explain the reader-writer problem and describe a solution.",
            "What is a race condition? How do you prevent it using locks?",
            "Design a thread-safe queue that supports multiple producers and consumers.",
        ],
    },
}


# ── Helper functions ─────────────────────────────────────────────────

def get_company_skills(company: str, role: str) -> list[str]:
    company_data = COMPANIES.get(company, {})
    return company_data.get("roles", {}).get(role, [])


def get_all_companies() -> list[str]:
    return list(COMPANIES.keys())


def get_company_roles(company: str) -> list[str]:
    return list(COMPANIES.get(company, {}).get("roles", {}).keys())


def get_learning_resources(skill: str) -> list[dict]:
    return LEARNING_RESOURCES.get(skill, [])


def get_interview_questions(topic: str, difficulty: str) -> list[str]:
    return INTERVIEW_QUESTION_TEMPLATES.get(difficulty, {}).get(topic, [])
