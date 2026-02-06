import os
import redis
from sentence_transformers import SentenceTransformer
import numpy as np

class redis_storage:
  def __init__(self):
    self.r=redis.Redis(host="redis-18193.c301.ap-south-1-1.ec2.cloud.redislabs.com",port=18193,password="BupHh5wCElXHWdseCGcqt55lDfqSwEcd",ssl=False,decode_responses=False)
    self.model=SentenceTransformer("all-MiniLM-L6-v2")


  def concat_resume(self,resume):
    self.s=""
    for key,value in resume.items():
      if value != "null" and key not in ["name","phone","email","raw_text","file_path"]:
        self.s=self.s+key+":"
        if isinstance(value,list):
            for element in value:
              if isinstance(element,str):
                self.s=self.s+element+","
              else:
                for k,v in element.items():
                  self.s=self.s+k+":"
                  if isinstance(v,str):
                    self.s=self.s+v+","
                  else:
                    for j in v:
                      self.s=self.s+j+","
        elif isinstance(value,dict):
            for k,v in value.items():
              self.s=self.s+k+":"  
              for j in v:
                self.s=self.s+j+","
        else:
            self.s=self.s+value+","

  def embedding_generator(self):
    self.embedding=self.model.encode(self.s,convert_to_numpy=True)


  def store_embedding(self,user_id):

    self.r.json().set(user_id,"$", {"embedding":self.embedding.tolist()})

def main():
    ob=redis_storage()
    resume={
      "name": "Monisha Jegadeesan",
      "email": "monishaj.65@gmail.com",
      "phone": "+91 9035212894",
      "linkedin": "https://www.linkedin.com/in/monisha-jegadeesan",
      "github": "https://github.com/monisha-jega",
      "location": "",
      "work_experience": "Approximately 4 years and 5 months of professional experience in software engineering and research.",
      "job_roles": [
        "Software Engineer",
        "Research Intern",
        "Teaching Assistant"
      ],
      "summary": "",
      "skills": {
        "Languages": [
          "C",
          "C++",
          "C#",
          "Java",
          "Python",
          "HTML",
          "CSS",
          "Javascript",
          "Web Assembly"
        ],
        "Tools": [
          "Unity",
          "ARCore",
          "Android Studio",
          "Stanford CoreNLP",
          "Git",
          "Bootstrap",
          "jQuery",
          "Emscripten",
          "Blaze",
          "j2Cl"
        ],
        "Libraries": [
          "NLTK",
          "django",
          "scipy",
          "pandas",
          "sklearn",
          "gensim",
          "keras",
          "tensorflow",
          "pytorch"
        ]
      },
      "experience": [
        {
          "title": "Software Engineer, Level IV",
          "company": "Google LLC",
          "location": "New York",
          "start_date": "Dec 2022",
          "end_date": "Present",
          "description": "Working on Keep, a notetaking editor in Google Workspace."
        },
        {
          "title": "Software Engineer, Level IV",
          "company": "Google India Pvt Ltd",
          "location": "Bangalore",
          "start_date": "Aug 2020",
          "end_date": "Nov 2022",
          "description": "Developing intelligent features for the Google Workspace Editors (Docs, Slides, Keep, etc) using my expertise on the products’ client-side software, supporting tools and libraries, and natural language processing infrastructure. Using cutting-edge frontend tools like Web Assembly and Emscripten, and Google-internal technologies like j2Cl, client-side cross-platform frameworks and build systems, to develop user-facing features such as spellcheck in encrypted documents for ﬁve languages and writing style suggestions for English text. Formulating technical designs for independent end-to-end problems, driving cross-team collaboration, upholding software reliability practices, technical-debt resolution and documentation, and proactively identifying areas of future work. Guiding junior engineers on programming and software design tasks to enable timely delivery of products to customers."
        },
        {
          "title": "Software Engineering Intern",
          "company": "Google India Pvt Ltd",
          "location": "Bangalore",
          "start_date": "May 2019",
          "end_date": "July 2019",
          "description": "Worked on the Editors client-side software infrastructure to develop a user interface with control options to undo or provide feedback on the correction and a logging framework, for the Google Docs text auto-correction feature."
        },
        {
          "title": "Research Intern",
          "company": "Big Data Experience Labs, Adobe Research",
          "location": "Bangalore",
          "start_date": "May 2018",
          "end_date": "July 2018",
          "description": "Developed a mobile application for Text to Scene Conversion in Augmented Reality, based on novel research techniques for prediction of three-dimensional object sizes and positions from textual features."
        },
        {
          "title": "Master’s Thesis: Paraphrase Generation with a Bilingual Model and Continuous Embeddings",
          "company": "Language Technologies Institute, Carnegie Mellon University",
          "location": "",
          "start_date": "Sep 2019",
          "end_date": "May 2020",
          "description": "Machinated a novel technique for paraphrase generation using the von Mises-Fisher (vMF) Loss on a transformer network, and showed that it produces superior paraphrases as compared to the log-likelihood model by employing bilingual data to induce zero-shot paraphrasing, guided by Prof. Yulia Tsvetkov."
        },
        {
          "title": "Research Intern: Cognitive Approach to Natural Language Processing",
          "company": "Department of Computer Science and Automation, Indian Institute of Science (IISc)",
          "location": "Bangalore",
          "start_date": "May 2017",
          "end_date": "July 2017",
          "description": "Developed a cognitive text parser that combines syntactic and semantic approaches, to process textual data into cognitive structural representations, to be used as a feature extractor for downstream NLP tasks, and demonstrated the correlation of the extracted cognitive features with semantic and syntactic text features, guided by Prof. Veni Madhavan."
        },
        {
          "title": "Course Teaching Assistant",
          "company": "Indian Institute of Technology Madras",
          "location": "",
          "start_date": "Jan 2020",
          "end_date": "May 2020",
          "description": "Designed and evaluated theoretical and practical assignments on various topics in Natural Language Processing. Presented lectures on Edit Distance and the Cocke-Young-Kasami (CYK) algorithm, to a class of 70 students. Mentored sixteen pairs of students on research projects, with supervision through regular team-wise progress meetings."
        }
      ],
      "projects": [
        {
          "name": "Graph Neural Networks for Extreme Summarization",
          "description": "Formulated appropriate graph-based deep neural models for the Extreme Summarization (XSum) task with sentence-level and/or document-level graphs, and obtained better performance than simple recurrent and hierarchical models.",
          "technologies": [
            "Graph Neural Networks",
            "Deep Learning"
          ]
        },
        {
          "name": "Risk-Sensitivity in Multi-Armed Bandits",
          "description": "Surveyed and implemented risk-sensitivity methods for stochastic bandit problems, and upgraded the Explore-Then-Commit algorithm for VaR and cVaR measures with competent performance.",
          "technologies": [
            "Multi-Armed Bandits",
            "Reinforcement Learning"
          ]
        },
        {
          "name": "Leveraging Ontological Knowledge for Neural Language Models",
          "description": "Incorporated Weight Initialization in learning word embeddings using the WordNet Ontology for a task in the Construction domain, resulting in a faster convergence rate and better representation of domain-speciﬁc terms.",
          "technologies": [
            "Neural Language Models",
            "Word Embeddings",
            "WordNet Ontology"
          ]
        },
        {
          "name": "Multimodal Dialogue Generation",
          "description": "Developed a deep neural model to establish the positive eﬀect of domain features in the performance of image retrieval in multimodal dialogue systems and explored the performance of attention and memory-based models with adaptations for multimodal dialogue and domain knowledge integration.",
          "technologies": [
            "Deep Neural Models",
            "Multimodal Dialogue Systems",
            "Attention Models",
            "Memory-based Models"
          ]
        },
        {
          "name": "Risk-Sensitive Reinforcement Learning",
          "description": "Empirically analyzed the existing methods for risk-sensitive reinforcement learning, tested the eﬀectiveness of modiﬁed versions and proposed a new distance-based risk measure and algorithm for Gridworld.",
          "technologies": [
            "Reinforcement Learning"
          ]
        },
        {
          "name": "Summarization and Keyword Extraction using TextRank",
          "description": "Analysed the TextRank algorithm for keyword extraction with syntactic ﬁlters and augmentation via Explicit Semantic Analysis, and for text summarization with exploration of various textual similarity methods.",
          "technologies": [
            "TextRank",
            "Keyword Extraction",
            "Text Summarization",
            "Explicit Semantic Analysis"
          ]
        },
        {
          "name": "Scaling Graph Algorithms",
          "description": "Implemented optimized graph algorithms for maximum network ﬂow and ﬁnding a maximum matching in a bipartite graph for real data graphs with up to 10,000 vertices and 100,000 edges.",
          "technologies": [
            "Graph Algorithms"
          ]
        },
        {
          "name": "Skin Disease Diagnostic System",
          "description": "Designed a web application that attempts to diagnose skin diseases based on images of the user’s skin powered by a deep neural model trained on a dataset created by scraping images from the web.",
          "technologies": [
            "Web Application",
            "Deep Neural Model"
          ]
        },
        {
          "name": "Breakout Game",
          "description": "Developed an Android application for the Breakout game with basic playing and scoring features.",
          "technologies": [
            "Android Application"
          ]
        }
      ],
      "education": [
        {
          "degree": "Dual Degree (B.Tech + M.Tech) in Computer Science and Engineering",
          "institution": "Indian Institute of Technology Madras, Chennai, India",
          "start_date": "2015",
          "end_date": "2020",
          "cgpa": "8.78"
        },
        {
          "degree": "XII",
          "institution": "Karnataka Board, KLE Society’s Independent PU College, Bangalore",
          "start_date": "",
          "end_date": "2015",
          "cgpa": "97.30 %"
        },
        {
          "degree": "X",
          "institution": "ICSE, B P Indian Public School, Bangalore",
          "start_date": "",
          "end_date": "2013",
          "cgpa": "96.33%"
        }
      ],
      "certifications": [
        "Advanced Deep Learning",
        "Deep Learning",
        "Machine Learning",
        "Natural Language Processing",
        "Reinforcement Learning",
        "Multi-Armed Bandits",
        "Probabilistic Graphical Models",
        "Computational Models of Cognition",
        "Computer Networks",
        "Database Systems",
        "Operating Systems",
        "Data Structures and Algorithms",
        "Object-Oriented Programming",
        "Probability-Statistics-Stochastic Processes",
        "Discrete Mathematics",
        "Linear Algebra",
        "Graph Theory"
      ],
      "achievements": [
        "First runner-up in the AWS Deep Learning Hackathon held during Shaastra 2018, IIT Madras: Developed a prototype for image-translation of English text on signboards and posters into vernacular languages.",
        "State Rank 17 in Karnataka Common Entrance Test for Engineering, 2015, out of approximately 1.2 lakh students.",
        "Topped respective academic institutions in both Class X and Class XII board exams.",
        "Improving the Diversity of Unsupervised Paraphrasing with Embedding Outputs (Paper, Poster) Monisha Jegadeesan, Sachin Kumar, John Wieting, Yulia Tsvetkov In Workshop on Multilingual Representation Learning, The 2021 Conference on Empirical Methods in Natural Language Processing (EMNLP 2021)",
        "Adversarial Demotion of Gender Bias in Natural Language Generation (Paper, Poster) Monisha Jegadeesan In ACM CODS-COMAD 2020 - Young Researchers’ Symposium",
        "ARComposer: Authoring Augmented Reality Experiences through Text (Poster) Sumit Kumar, Paridhi Maheshwari, Monisha Jegadeesan, Amrit Singhal, Kush Kumar Singh, Kundan Krishna In ACM User Interface Software and Technology Symposium 2019 (ACM UIST 2019)",
        "Visualizing Natural Language through 3D Scenes in Augmented Reality Sumit Kumar, Paridhi Maheshwari, Monisha Jegadeesan, Amrit Singhal, Kush Kumar Singh, Kundan Krishna Filed at the US PTO (Application Number: 16/247,235)",
        "Leveraging Ontological Knowledge for Neural Language Models (Paper, Poster) Ameet Deshpande, Monisha Jegadeesan In ACM CODS-COMAD 2019 - Young Researchers’ Symposium"
      ]
    }
    ob.concat_resume(resume)
    ob.embedding_generator()
    ob.store_embedding("k")
    print(ob.s)
    print(ob.r.json().get("k")["embedding"])

if __name__ == "__main__":

  main()
