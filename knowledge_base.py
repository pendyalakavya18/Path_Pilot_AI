COMPANIES = {
    'Google': {
        'type': 'Product',
        'roles': {
            'Software Engineer': ['Python', 'Java', 'C++', 'System Design', 'Algorithms', 'Data Structures', 'Distributed Systems'],
            'Data Scientist': ['Python', 'Machine Learning', 'Statistics', 'SQL', 'TensorFlow', 'PyTorch', 'Data Analysis'],
            'Frontend Engineer': ['JavaScript', 'React', 'TypeScript', 'HTML', 'CSS', 'Web Performance', 'Accessibility'],
            'Backend Engineer': ['Python', 'Java', 'Go', 'Microservices', 'Databases', 'API Design', 'Cloud Computing'],
            'Data Analyst': ['SQL', 'Python', 'BigQuery', 'Data Visualization', 'Statistics', 'Looker', 'Excel']
        }
    },
    'Amazon': {
        'type': 'Product',
        'roles': {
            'Software Development Engineer': ['Java', 'Python', 'AWS', 'System Design', 'Algorithms', 'OOP', 'Distributed Systems'],
            'Data Engineer': ['Python', 'Spark', 'SQL', 'ETL', 'AWS', 'Data Warehousing', 'Kafka'],
            'DevOps Engineer': ['AWS', 'Docker', 'Kubernetes', 'CI/CD', 'Linux', 'Python', 'Terraform'],
            'Data Analyst': ['SQL', 'Python', 'Redshift', 'QuickSight', 'Statistics', 'Excel', 'Data Modeling']
        }
    },
    'Microsoft': {
        'type': 'Product',
        'roles': {
            'Software Engineer': ['C#', 'C++', 'Azure', 'System Design', 'Algorithms', '.NET', 'Cloud Services'],
            'AI Engineer': ['Python', 'Machine Learning', 'Azure ML', 'Deep Learning', 'NLP', 'Computer Vision'],
            'Cloud Solution Architect': ['Azure', 'System Design', 'Networking', 'Security', 'DevOps', 'Microservices'],
            'Data Analyst': ['SQL', 'Power BI', 'Excel', 'Python', 'Azure Data Factory', 'Statistics', 'DAX']
        }
    },
    'Meta': {
        'type': 'Product',
        'roles': {
            'Software Engineer': ['Python', 'C++', 'React', 'System Design', 'Algorithms', 'Distributed Systems'],
            'ML Engineer': ['Python', 'PyTorch', 'Machine Learning', 'Deep Learning', 'Computer Vision', 'NLP'],
            'Frontend Engineer': ['JavaScript', 'React', 'GraphQL', 'TypeScript', 'Web Performance'],
            'Data Analyst': ['SQL', 'Python', 'Data Visualization', 'Statistics', 'A/B Testing', 'Tableau']
        }
    },
    'Apple': {
        'type': 'Product',
        'roles': {
            'Software Engineer': ['Swift', 'Objective-C', 'C++', 'iOS Development', 'System Design', 'Algorithms'],
            'ML Engineer': ['Python', 'Core ML', 'Machine Learning', 'Computer Vision', 'NLP', 'TensorFlow'],
            'Frontend Engineer': ['Swift', 'SwiftUI', 'UIKit', 'iOS', 'Accessibility', 'Human Interface Guidelines']
        }
    },
    'Netflix': {
        'type': 'Product',
        'roles': {
            'Software Engineer': ['Java', 'Python', 'Microservices', 'System Design', 'Algorithms', 'AWS', 'Spring Boot'],
            'Data Engineer': ['Python', 'Spark', 'Kafka', 'SQL', 'Flink', 'Data Pipelines', 'AWS'],
            'ML Engineer': ['Python', 'Machine Learning', 'Deep Learning', 'Recommendation Systems', 'A/B Testing', 'Statistics'],
            'Frontend Engineer': ['JavaScript', 'React', 'Node.js', 'TypeScript', 'Web Performance', 'GraphQL']
        }
    },
    'Uber': {
        'type': 'Product',
        'roles': {
            'Software Engineer': ['Java', 'Go', 'Python', 'Microservices', 'System Design', 'Algorithms', 'Distributed Systems'],
            'Data Scientist': ['Python', 'Machine Learning', 'SQL', 'Statistics', 'A/B Testing', 'Deep Learning'],
            'Backend Engineer': ['Go', 'Java', 'Python', 'gRPC', 'Microservices', 'Kafka', 'Databases'],
            'Mobile Engineer': ['Kotlin', 'Swift', 'React Native', 'Mobile Architecture', 'CI/CD', 'Performance']
        }
    },
    'Salesforce': {
        'type': 'Product',
        'roles': {
            'Software Engineer': ['Java', 'Python', 'Apex', 'System Design', 'REST APIs', 'Algorithms', 'Cloud Computing'],
            'Salesforce Developer': ['Apex', 'Lightning', 'Visualforce', 'SOQL', 'JavaScript', 'Integration'],
            'Data Analyst': ['SQL', 'Tableau', 'Python', 'Salesforce Reports', 'Data Modeling', 'CRM Analytics'],
            'DevOps Engineer': ['CI/CD', 'Docker', 'Kubernetes', 'Jenkins', 'AWS', 'Terraform', 'Linux']
        }
    },
    'Adobe': {
        'type': 'Product',
        'roles': {
            'Software Engineer': ['Java', 'C++', 'JavaScript', 'System Design', 'Algorithms', 'Cloud Computing'],
            'Frontend Engineer': ['JavaScript', 'React', 'TypeScript', 'CSS', 'Web Components', 'Accessibility'],
            'Data Scientist': ['Python', 'Machine Learning', 'Statistics', 'NLP', 'Deep Learning', 'SQL'],
            'ML Engineer': ['Python', 'TensorFlow', 'PyTorch', 'Computer Vision', 'Generative AI', 'Deep Learning']
        }
    },
    'Oracle': {
        'type': 'Product',
        'roles': {
            'Software Engineer': ['Java', 'C++', 'SQL', 'System Design', 'Algorithms', 'OCI', 'Cloud Computing'],
            'Database Administrator': ['Oracle DB', 'SQL', 'PL/SQL', 'Performance Tuning', 'Backup Recovery', 'RAC'],
            'Cloud Engineer': ['OCI', 'Terraform', 'Docker', 'Kubernetes', 'Linux', 'Python', 'Networking'],
            'Data Analyst': ['SQL', 'Oracle Analytics', 'Python', 'Data Modeling', 'ETL', 'Statistics']
        }
    },
    'IBM': {
        'type': 'Product',
        'roles': {
            'Software Engineer': ['Java', 'Python', 'Node.js', 'System Design', 'Algorithms', 'Cloud Computing'],
            'Data Scientist': ['Python', 'Machine Learning', 'Watson', 'SQL', 'Statistics', 'NLP'],
            'Cloud Engineer': ['IBM Cloud', 'Docker', 'Kubernetes', 'OpenShift', 'Terraform', 'Linux'],
            'AI Engineer': ['Python', 'Machine Learning', 'Watson AI', 'NLP', 'Deep Learning', 'MLOps']
        }
    },
    'Stripe': {
        'type': 'Product',
        'roles': {
            'Software Engineer': ['Ruby', 'Java', 'Python', 'System Design', 'Algorithms', 'Distributed Systems', 'APIs'],
            'Backend Engineer': ['Ruby', 'Go', 'Java', 'Databases', 'Payment Systems', 'API Design', 'Security'],
            'Frontend Engineer': ['JavaScript', 'React', 'TypeScript', 'CSS', 'Web Performance', 'Accessibility'],
            'Data Scientist': ['Python', 'SQL', 'Machine Learning', 'Statistics', 'A/B Testing', 'Fraud Detection']
        }
    },
    'Spotify': {
        'type': 'Product',
        'roles': {
            'Backend Engineer': ['Java', 'Python', 'Microservices', 'Google Cloud', 'Kafka', 'System Design'],
            'Data Engineer': ['Python', 'Spark', 'SQL', 'Google Cloud', 'Data Pipelines', 'Airflow'],
            'ML Engineer': ['Python', 'Machine Learning', 'Recommendation Systems', 'Deep Learning', 'NLP', 'TensorFlow'],
            'Frontend Engineer': ['JavaScript', 'React', 'TypeScript', 'Web Audio API', 'CSS', 'Web Performance']
        }
    },
    'TCS': {
        'type': 'Service',
        'roles': {
            'Software Developer': ['Java', 'Python', 'SQL', 'Spring Boot', 'REST APIs', 'Agile'],
            'Data Analyst': ['SQL', 'Python', 'Excel', 'Power BI', 'Data Visualization', 'Statistics'],
            'DevOps Engineer': ['AWS', 'Docker', 'Jenkins', 'Linux', 'CI/CD', 'Python'],
            'Full Stack Developer': ['Java', 'JavaScript', 'React', 'Spring Boot', 'SQL', 'REST APIs', 'HTML/CSS']
        }
    },
    'Infosys': {
        'type': 'Service',
        'roles': {
            'Systems Engineer': ['Java', 'Python', 'SQL', 'Web Development', 'Cloud Basics', 'Agile'],
            'Digital Specialist': ['Python', 'Machine Learning', 'Cloud', 'DevOps', 'Automation'],
            'Data Engineer': ['Python', 'SQL', 'Spark', 'ETL', 'Cloud', 'Data Warehousing'],
            'Full Stack Developer': ['Java', 'JavaScript', 'Angular', 'Spring', 'SQL', 'REST APIs']
        }
    },
    'Wipro': {
        'type': 'Service',
        'roles': {
            'Project Engineer': ['Java', 'Python', 'SQL', 'Web Services', 'Testing', 'Agile'],
            'Data Engineer': ['Python', 'SQL', 'ETL', 'Big Data', 'Spark', 'Cloud'],
            'Cloud Engineer': ['AWS', 'Azure', 'Docker', 'Kubernetes', 'Terraform', 'Linux'],
            'Full Stack Developer': ['Java', 'JavaScript', 'React', 'Node.js', 'SQL', 'REST APIs']
        }
    },
    'Zoho': {
        'type': 'Product',
        'roles': {
            'Software Engineer': ['Java', 'Python', 'JavaScript', 'System Design', 'Algorithms', 'Data Structures'],
            'Frontend Engineer': ['JavaScript', 'HTML', 'CSS', 'React', 'TypeScript', 'Web Performance'],
            'QA Engineer': ['Java', 'Selenium', 'Test Automation', 'API Testing', 'Performance Testing', 'Agile'],
            'Technical Writer': ['Technical Writing', 'API Documentation', 'Markdown', 'Content Strategy']
        }
    },
    'Razorpay': {
        'type': 'Fintech',
        'roles': {
            'Software Engineer': ['Go', 'Python', 'PHP', 'System Design', 'Algorithms', 'Payment Systems', 'Microservices'],
            'Backend Engineer': ['Go', 'PHP', 'Python', 'MySQL', 'Redis', 'Kafka', 'API Design'],
            'Frontend Engineer': ['JavaScript', 'React', 'TypeScript', 'CSS', 'Web Security', 'Web Performance'],
            'Data Analyst': ['SQL', 'Python', 'Tableau', 'Statistics', 'Data Modeling', 'Excel']
        }
    },
    'PhonePe': {
        'type': 'Fintech',
        'roles': {
            'Software Engineer': ['Java', 'Kotlin', 'System Design', 'Algorithms', 'Microservices', 'Distributed Systems'],
            'Backend Engineer': ['Java', 'Spring Boot', 'Kafka', 'MySQL', 'Redis', 'System Design'],
            'Mobile Engineer': ['Kotlin', 'Android', 'MVVM', 'Jetpack Compose', 'Performance', 'CI/CD'],
            'Data Analyst': ['SQL', 'Python', 'Data Visualization', 'Statistics', 'Excel', 'Redash']
        }
    },
    'Flipkart': {
        'type': 'Product',
        'roles': {
            'Software Development Engineer': ['Java', 'Python', 'System Design', 'Algorithms', 'Distributed Systems', 'Microservices'],
            'Data Scientist': ['Python', 'Machine Learning', 'Statistics', 'SQL', 'Deep Learning', 'A/B Testing'],
            'Frontend Engineer': ['JavaScript', 'React', 'TypeScript', 'Node.js', 'Web Performance', 'CSS'],
            'Data Analyst': ['SQL', 'Python', 'Tableau', 'Statistics', 'Data Modeling', 'Excel', 'Hive']
        }
    }
}

LEARNING_RESOURCES = {
    'Python': [
        {'title': 'Python Official Documentation', 'url': 'https://docs.python.org', 'type': 'documentation'},
        {'title': 'Python for Everybody', 'url': 'https://www.py4e.com', 'type': 'course'},
        {'title': 'Real Python Tutorials', 'url': 'https://realpython.com', 'type': 'tutorial'}
    ],
    'Machine Learning': [
        {'title': 'Coursera ML by Andrew Ng', 'url': 'https://www.coursera.org/learn/machine-learning', 'type': 'course'},
        {'title': 'Scikit-learn Documentation', 'url': 'https://scikit-learn.org', 'type': 'documentation'},
        {'title': 'Kaggle Learn', 'url': 'https://www.kaggle.com/learn', 'type': 'tutorial'}
    ],
    'System Design': [
        {'title': 'System Design Primer', 'url': 'https://github.com/donnemartin/system-design-primer', 'type': 'tutorial'},
        {'title': 'Designing Data-Intensive Applications', 'url': 'https://dataintensive.net', 'type': 'book'},
        {'title': 'Grokking System Design', 'url': 'https://www.educative.io/courses/grokking-the-system-design-interview', 'type': 'course'}
    ],
    'Algorithms': [
        {'title': 'LeetCode', 'url': 'https://leetcode.com', 'type': 'practice'},
        {'title': 'Introduction to Algorithms (CLRS)', 'url': 'https://mitpress.mit.edu/books/introduction-algorithms', 'type': 'book'},
        {'title': 'AlgoExpert', 'url': 'https://www.algoexpert.io', 'type': 'course'}
    ],
    'JavaScript': [
        {'title': 'MDN Web Docs', 'url': 'https://developer.mozilla.org', 'type': 'documentation'},
        {'title': 'JavaScript.info', 'url': 'https://javascript.info', 'type': 'tutorial'},
        {'title': 'Eloquent JavaScript', 'url': 'https://eloquentjavascript.net', 'type': 'book'}
    ],
    'React': [
        {'title': 'React Official Docs', 'url': 'https://react.dev', 'type': 'documentation'},
        {'title': 'React Tutorial for Beginners', 'url': 'https://www.youtube.com/watch?v=SqcY0GlETPk', 'type': 'video'},
        {'title': 'Full Stack Open', 'url': 'https://fullstackopen.com', 'type': 'course'}
    ],
    'AWS': [
        {'title': 'AWS Documentation', 'url': 'https://docs.aws.amazon.com', 'type': 'documentation'},
        {'title': 'AWS Certified Solutions Architect', 'url': 'https://aws.amazon.com/certification', 'type': 'certification'},
        {'title': 'A Cloud Guru', 'url': 'https://acloudguru.com', 'type': 'course'}
    ],
    'SQL': [
        {'title': 'SQLZoo', 'url': 'https://sqlzoo.net', 'type': 'practice'},
        {'title': 'PostgreSQL Tutorial', 'url': 'https://www.postgresqltutorial.com', 'type': 'tutorial'},
        {'title': 'Mode SQL Tutorial', 'url': 'https://mode.com/sql-tutorial', 'type': 'tutorial'}
    ],
    'Docker': [
        {'title': 'Docker Official Docs', 'url': 'https://docs.docker.com', 'type': 'documentation'},
        {'title': 'Docker for Beginners', 'url': 'https://docker-curriculum.com', 'type': 'tutorial'},
        {'title': 'KodeKloud Docker Course', 'url': 'https://kodekloud.com/courses/docker-for-the-absolute-beginner', 'type': 'course'}
    ],
    'Kubernetes': [
        {'title': 'Kubernetes Official Docs', 'url': 'https://kubernetes.io/docs', 'type': 'documentation'},
        {'title': 'Kubernetes the Hard Way', 'url': 'https://github.com/kelseyhightower/kubernetes-the-hard-way', 'type': 'tutorial'},
        {'title': 'KodeKloud CKA Course', 'url': 'https://kodekloud.com/courses/certified-kubernetes-administrator', 'type': 'course'}
    ],
    'Go': [
        {'title': 'A Tour of Go', 'url': 'https://tour.golang.org', 'type': 'tutorial'},
        {'title': 'Go by Example', 'url': 'https://gobyexample.com', 'type': 'tutorial'},
        {'title': 'Effective Go', 'url': 'https://golang.org/doc/effective_go', 'type': 'documentation'}
    ],
    'TypeScript': [
        {'title': 'TypeScript Official Docs', 'url': 'https://www.typescriptlang.org/docs', 'type': 'documentation'},
        {'title': 'TypeScript Deep Dive', 'url': 'https://basarat.gitbook.io/typescript', 'type': 'book'},
        {'title': 'Total TypeScript', 'url': 'https://www.totaltypescript.com', 'type': 'course'}
    ],
    'Java': [
        {'title': 'Oracle Java Tutorials', 'url': 'https://docs.oracle.com/javase/tutorial', 'type': 'documentation'},
        {'title': 'Java Programming MOOC', 'url': 'https://java-programming.mooc.fi', 'type': 'course'},
        {'title': 'Baeldung', 'url': 'https://www.baeldung.com', 'type': 'tutorial'}
    ],
    'Data Structures': [
        {'title': 'Visualgo', 'url': 'https://visualgo.net', 'type': 'tutorial'},
        {'title': 'GeeksForGeeks DSA', 'url': 'https://www.geeksforgeeks.org/data-structures', 'type': 'tutorial'},
        {'title': 'NeetCode', 'url': 'https://neetcode.io', 'type': 'practice'}
    ],
    'Deep Learning': [
        {'title': 'Deep Learning Specialization', 'url': 'https://www.coursera.org/specializations/deep-learning', 'type': 'course'},
        {'title': 'Fast.ai', 'url': 'https://www.fast.ai', 'type': 'course'},
        {'title': 'PyTorch Tutorials', 'url': 'https://pytorch.org/tutorials', 'type': 'tutorial'}
    ],
    'Statistics': [
        {'title': 'Khan Academy Statistics', 'url': 'https://www.khanacademy.org/math/statistics-probability', 'type': 'course'},
        {'title': 'StatQuest YouTube', 'url': 'https://www.youtube.com/c/joshstarmer', 'type': 'video'},
        {'title': 'Think Stats', 'url': 'https://greenteapress.com/thinkstats', 'type': 'book'}
    ]
}

INTERVIEW_QUESTION_TEMPLATES = {
    'Easy': {
        'Python': [
            'What are the differences between lists and tuples in Python?',
            'Explain list comprehension with an example.',
            'What is the difference between == and is in Python?',
            'How do you handle exceptions in Python?',
            'What is the difference between a shallow copy and a deep copy?',
            'Explain the difference between append() and extend() methods in Python lists.'
        ],
        'Algorithms': [
            'Implement a function to reverse a string.',
            'Find the maximum element in an array.',
            'Check if a number is prime.',
            'Implement binary search on a sorted array.',
            'What is the difference between linear search and binary search?',
            'Explain the concept of time complexity and space complexity.'
        ],
        'System Design': [
            'What is the difference between SQL and NoSQL databases?',
            'Explain what a load balancer does.',
            'What is caching and why is it important?',
            'Describe the client-server architecture.',
            'What is the difference between horizontal and vertical scaling?',
            'Explain what a CDN is and why it is used.'
        ],
        'JavaScript': [
            'What is the difference between let, const, and var?',
            'Explain closures in JavaScript.',
            'What is the DOM and how do you interact with it?',
            'Describe the difference between == and === in JavaScript.',
            'What are arrow functions and how do they differ from regular functions?',
            'Explain what event bubbling is in JavaScript.'
        ],
        'SQL': [
            'What is the difference between INNER JOIN and LEFT JOIN?',
            'Explain the purpose of GROUP BY clause.',
            'What is the difference between WHERE and HAVING?',
            'What are primary keys and foreign keys?',
            'Explain normalization and its different forms.',
            'What is the difference between DELETE and TRUNCATE?'
        ],
        'Java': [
            'What is the difference between an abstract class and an interface?',
            'Explain the concept of polymorphism in Java.',
            'What is garbage collection in Java?',
            'What is the difference between ArrayList and LinkedList?',
            'Explain the concept of encapsulation with an example.',
            'What are the access modifiers in Java?'
        ],
        'Data Structures': [
            'Explain the difference between a stack and a queue.',
            'What is a linked list and when would you use one?',
            'What is a hash table and how does it work?',
            'Explain the difference between an array and a linked list.',
            'What is a binary tree? Describe its basic operations.',
            'What is the difference between BFS and DFS?'
        ],
        'Machine Learning': [
            'What is the difference between supervised and unsupervised learning?',
            'Explain what overfitting is and how to prevent it.',
            'What is a confusion matrix?',
            'Explain the difference between classification and regression.',
            'What is cross-validation and why is it used?',
            'What is the bias-variance tradeoff?'
        ]
    },
    'Medium': {
        'Python': [
            'Explain decorators in Python with an example.',
            'What are generators and how do they differ from regular functions?',
            'Implement a custom context manager.',
            'Explain the GIL and its implications.',
            'How does Python handle memory management?',
            'Explain metaclasses in Python and give a use case.'
        ],
        'Algorithms': [
            'Find the longest substring without repeating characters.',
            'Implement merge sort algorithm.',
            'Detect a cycle in a linked list.',
            'Find the kth largest element in an array.',
            'Implement a function to check if a binary tree is balanced.',
            'Explain dynamic programming and solve the coin change problem.'
        ],
        'System Design': [
            'Design a URL shortening service like bit.ly.',
            'How would you design a rate limiter?',
            'Design a notification system.',
            'Explain how you would implement a cache with LRU eviction.',
            'Design a simple key-value store.',
            'How would you design an API gateway?'
        ],
        'JavaScript': [
            'Explain the event loop in JavaScript.',
            'What are Promises and how do they work?',
            'Explain the prototype chain in JavaScript.',
            'What is the difference between synchronous and asynchronous code?',
            'Implement a debounce function.',
            'Explain how async/await works internally.'
        ],
        'SQL': [
            'Explain window functions with practical examples.',
            'What is a CTE and when would you use one?',
            'How do you optimize a slow SQL query?',
            'Explain the difference between clustered and non-clustered indexes.',
            'Write a query to find the second highest salary in a table.',
            'Explain transaction isolation levels.'
        ],
        'Java': [
            'Explain the Java Collections Framework hierarchy.',
            'What is the difference between HashMap and ConcurrentHashMap?',
            'Explain the concept of generics in Java.',
            'What are design patterns? Explain Singleton and Factory patterns.',
            'How does the JVM garbage collector work?',
            'Explain multithreading in Java with synchronization.'
        ],
        'Data Structures': [
            'Implement an LRU cache.',
            'Explain AVL trees and how they maintain balance.',
            'Implement a trie and explain its use cases.',
            'What is a graph? Explain adjacency list vs adjacency matrix.',
            'Implement a min-heap and explain its operations.',
            'Explain the concept of a segment tree.'
        ],
        'Machine Learning': [
            'Explain gradient descent and its variants.',
            'What is regularization? Compare L1 and L2.',
            'Explain how random forests work.',
            'What is the curse of dimensionality?',
            'Explain precision, recall, and F1 score.',
            'How does a neural network learn through backpropagation?'
        ]
    },
    'Hard': {
        'Python': [
            'Implement a metaclass and explain its use case.',
            'Explain the difference between threading and multiprocessing.',
            'How would you optimize a slow Python application?',
            'Implement a custom iterator protocol.',
            'Explain how Python async/await and the event loop work internally.',
            'Design a plugin system using Python metaprogramming.'
        ],
        'Algorithms': [
            'Find the median of two sorted arrays.',
            'Implement a trie data structure.',
            'Solve the N-Queens problem.',
            'Find the minimum window substring.',
            'Implement Dijkstra\'s shortest path algorithm.',
            'Solve the longest increasing subsequence problem in O(n log n).'
        ],
        'System Design': [
            'Design a distributed file storage system like Google Drive.',
            'How would you design Instagram?',
            'Design a real-time chat application like WhatsApp.',
            'Design a distributed cache system.',
            'Design a search engine like Google.',
            'How would you design a video streaming platform like Netflix?'
        ],
        'JavaScript': [
            'Implement a virtual DOM and explain reconciliation.',
            'Design a state management system like Redux from scratch.',
            'Explain garbage collection strategies in V8.',
            'Implement a custom module bundler.',
            'Explain how React Fiber architecture works.',
            'Implement a reactive data binding system.'
        ],
        'SQL': [
            'Design a database schema for a social media platform.',
            'Explain query execution plans and how to read them.',
            'How would you handle a database migration with zero downtime?',
            'Explain sharding strategies and their trade-offs.',
            'Design an efficient schema for a multi-tenant application.',
            'Explain MVCC and how PostgreSQL handles concurrent transactions.'
        ],
        'Java': [
            'Explain the Java Memory Model and happens-before relationship.',
            'Design a thread-safe connection pool from scratch.',
            'Explain how the JIT compiler optimizes Java bytecode.',
            'Implement a custom class loader and explain its use cases.',
            'Design a microservice architecture using Spring Boot.',
            'Explain the internals of how HashMap works including rehashing.'
        ],
        'Data Structures': [
            'Implement a B-tree and explain its use in databases.',
            'Design a skip list and analyze its time complexity.',
            'Implement a concurrent hash map from scratch.',
            'Explain and implement a bloom filter.',
            'Design a data structure for real-time top-K tracking.',
            'Implement a persistent data structure.'
        ],
        'Machine Learning': [
            'Explain attention mechanisms and transformers architecture.',
            'Design an end-to-end ML pipeline for a recommendation system.',
            'Explain how GANs work and their training challenges.',
            'How would you deploy and monitor ML models in production?',
            'Explain federated learning and its applications.',
            'Design an A/B testing framework with statistical rigor.'
        ]
    }
}

def get_company_skills(company, role):
    if company in COMPANIES and role in COMPANIES[company]['roles']:
        return COMPANIES[company]['roles'][role]
    return []

def get_all_companies():
    return list(COMPANIES.keys())

def get_company_roles(company):
    if company in COMPANIES:
        return list(COMPANIES[company]['roles'].keys())
    return []

def get_learning_resources(skill):
    return LEARNING_RESOURCES.get(skill, [])

def get_interview_questions(topic, difficulty):
    if difficulty in INTERVIEW_QUESTION_TEMPLATES and topic in INTERVIEW_QUESTION_TEMPLATES[difficulty]:
        return INTERVIEW_QUESTION_TEMPLATES[difficulty][topic]
    return []
