import redis
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sentence_transformers import SentenceTransformer

class content_based_recommendation:
  def __init__(self,k):
    self.r=redis.Redis(host="redis-18193.c301.ap-south-1-1.ec2.cloud.redislabs.com",port=18193,password="BupHh5wCElXHWdseCGcqt55lDfqSwEcd",ssl=False,decode_responses=False)
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
            for idx,element in value:
              s=s+element+","
          else:
            s=s+value+","
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
  ob=content_based_recommendation(2)
  job=[{"title":
  "software development engineer, amazon ads",
  "id":"23045",
  "company":
  "amazon.com",
  "location":
  "new york, ny, us",
  "job_type":
  "fulltime",
  "interval":
  "yearly",
  "is_remote":
  "false",
  "company_industry":
  "Internet And Software",
  "company_addresses":
  "440 Terry Ave N, Seattle, WA, United States, Washington",

  "skills":
  #Array (3)
  [(0,
  "JavaScript"),
  (1,
  "React"),
  (2,
  "Node.js")],
  "experience_range":
  "null",
  "work_from_home_type":
  "null",
  "search_term":
  "software engineer",
  "country":
  "USA",
  "location_query":
  "New York, NY",
  "degree_required":
  "Bachelor's degree",
  "employment_type":
  "full-time",
  "experience_years":
  "5",

  "languages":
  #Array (1)
  [(0,
  "English")],
  "remote_type":
  "hybrid",
  "salary_max":
  "120000",
  "salary_min":
  "80000",
  "seniority":
  "mid"},{"name":"google","id":"345","role":"machine learning and natural language processing engineer","skills":[(0,"pytorch"),(1,"natural language processing"),(2,"reinforcement learning"),(3,"deep learning"),(4,"machine learning"),(5,"text summarization and keyword extraction"),(6,"graph algorithms and graph neural network")]}]
  ob.concatenate_job_fields(job)
  
  
  ob.recommendation("123")
  print(ob.job_recommendations)
if __name__=="__main__":
  main()

