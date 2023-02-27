# Assignment 2 - Data ETL Pipeline  

### Overview
This utility collects weather data from SEVIR that was recorded by the GOES and NEXRAD satellites. With the help of Airflow and Crontab, a scheduling tool, we can use this tool to collect data from NOAA's AWS S3 bucket and create an extraction-transformation-loading (ETL) process to collect real-time data on daily basis.

### Directory layout
    .
    ├── airflow            # Scheduling tool used to extract real-time data on daily basis
      ├── docker-compose.yaml 
      
    ├── Arch Diag          # Diagram represents the architecture we have used to build this project             
    ├── backend
      ├── awscloud         # All the files related to AWS functionality, which connects with S3 and Cloudwatch
      ├── fast_api         # Built API to extract data 
      ├── test 
      ├── utils            # Utility functions like logger and status checker.
    ├── frontend
      ├── Dockerfile       # Docker-Container
      ├── login.py         # streamlit application to capture login details
      ├── main.py          
    ├── great-expectations
      ├── data             # This dir consists of data related file (SQLlite)
      ├── expectations
    └── README.md

#### Automated tests
Automated tests are usually placed into the `test`.
    .
    ├── ...
    ├── test                           # Test files
    │   ├── test_aws_goes.py           # Test cases related to GOES Dataset
    │   └── test_aws_nextrad.py        # Test cases related to NexRad Dataset
    └── ...

#### Automated tests
Automated tests are usually placed into the `test`.

    .
    ├── ...
    ├── awscloud         
    │   ├── cloudwatch   # Code related to Cloudwatch
    │   └── s3           # Code related to S3
    └── ...


### Workflow
<img src="https://github.com/BigDataIA-Spring2023-Team-05/Assignment-02/blob/main/Arch_Diag/my_ideal_cluster.png"></img>

Codelabs link:
https://codelabs-preview.appspot.com/?file_id=1d7batzqngkFxnNQz9ccwWyiu2uxTIYhbklPmDzcCiM4#0

### ER Diagram

ER Diagram for the SQL database tables - GOES metadata and NEXRAD metadata - which is storing the data for GOES and NEXRAD metadata.

<img src="https://github.com/BigDataIA-Spring2023-Team-05/Assignment-01/blob/main/ERdiagram.drawio.png"></img>

## How to run this project:
1. Clone this repo locally `git clone <repo-url>`

2. Setup the local python enviornment. You can refer this link [How to setup python enviornment?](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/ "How to setup python enviornment?")

3. Install all the dependencies from the requirements.txt file
`pip install -r requirements.txt`

4. Install all local dependencies 
`pip install -e .`
`Upgrade setuptools: pip install --upgrade setuptools`

5. Create `.env` file under awscloud folder

6. Specify these key and values pair in your .env

`AWS_ACCESS_KEY=<value>`

`AWS_ACCESS_KEY_SECRET=<value>`

`TARGET_BUCKET_NAME=<value>` # Target bucket name for GOES in S3 Bucket.

8. Run the streamlit project
`streamlit run ui/main.py`

## Streamlit Application link:
http://ec2-3-223-141-28.compute-1.amazonaws.com:8501


## FastAPI Application link:
http://ec2-3-223-141-28.compute-1.amazonaws.com:8000/docs
