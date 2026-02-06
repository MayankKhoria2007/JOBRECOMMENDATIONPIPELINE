import os
import redis
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sentence_transformers import SentenceTransformer

class content_based_recommendation:
  def __init__(self,k):
    self.r=redis.Redis(host=os.getenv("REDIS_HOST"),port=int(os.getenv("REDIS_PORT")),password=os.getenv("REDIS_PASSWORD"),ssl=False,decode_responses=False)
    self.model=SentenceTransformer("all-MiniLM-L6-v2")
    self.knn=NearestNeighbors(n_neighbors=k,metric="cosine")
    self.job_descriptions=[]
    self.job_ids=[]

  def concatenate_job_fields(self,jobs):
    for job in jobs:
      self.job_ids.append(job["id"])
      s=""
      for key,value in job.items():
        if value!="null" and key!="id":
          s=s+key+":"
          if isinstance(value,list):
            for element in value:
              s=s+element+","
          else:
            s=s+str(value)+","
      self.job_descriptions.append(s)

  def recommendation(self,user_id):
      job_embeddings=self.model.encode(self.job_descriptions,convert_to_numpy=True)
      self.knn.fit(job_embeddings)
      resume_embeddings=[self.r.json().get(user_id)["embedding"]]
      distances,indices=self.knn.kneighbors(resume_embeddings)
      c=0
      self.job_recommendations={}
      for i in indices:
        c=0
        for j in i:
          c=c+1
          self.job_recommendations[c]=self.job_ids[j]
        
  

def main():
  ob=content_based_recommendation(3)
  job=[{
  "_id": "6975d78fb492bb6064087c5f",
  "id": "in-92e93758af906bf5",
  "site": "indeed",
  "job_url": "https://www.indeed.com/viewjob?jk=92e93758af906bf5",
  "job_url_direct": "https://www.amazon.jobs/jobs/3156628/software-development-engineer-ama…",
  "title": "software development engineer, amazon ads",
  "company": "amazon.com",
  "location": "new york, ny, us",
  "job_type": "fulltime",
  "interval": "yearly",
  "min_amount": 143700.0,
  "max_amount": 213800.0,
  "currency": "USD",
  "is_remote": False,
  "description": "*DESCRIPTION* --------------- Amazon Ads is re-imagining the adverti…",
  "company_industry": "Internet And Software",
  "company_url": "https://www.indeed.com/cmp/Amazon.com",
  "company_logo": "https://d2q79iu7y748jz.cloudfront.net/s/_squarelogo/256x256/3e9d43f5c2…",
  "company_url_direct": "https://www.amazon.jobs",
  "company_addresses": "440 Terry Ave N, Seattle, WA, United States, Washington",
  "company_num_employees": "10,000+",
  "skills": [
    "JavaScript",
    "React",
    "Node.js"
  ],
  "experience_range": "",
  "work_from_home_type": "",
  "search_term": "software engineer",
  "country": "USA",
  "location_query": "New York, NY",
  "degree_required": "Bachelor's degree",
  "employment_type": "full-time",
  "experience_years": 5,
  "languages": [
    "English"
  ],
  "llm_enriched": True,
  "remote_type": "hybrid",
  "salary_min": 80000,
  "salary_max": 120000,
  "seniority": "mid"
  },{"id":"ruh383","role":"software developer"},{"id":"47891hdm","role":"maachine learning engineer"}
  ]


  ob.concatenate_job_fields(job)
  
  
  ob.recommendation("123")
  print(ob.job_recommendations)
  
if __name__=="__main__":
  main()


