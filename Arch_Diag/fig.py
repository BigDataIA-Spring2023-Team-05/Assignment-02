
from diagrams import Cluster, Edge, Diagram
from diagrams.onprem.client import User, Users
from diagrams.onprem.container import Docker
from diagrams.onprem.workflow import Airflow
from diagrams.aws.storage import SimpleStorageServiceS3 as S3
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import Postgresql as PostgreSQL 
from diagrams.onprem.database import Mysql as Mysql
from diagrams.oci.monitoring import Telemetry



with Diagram("My Ideal Cluster", show=False):
    # Define Nodes
    ingress = Users("User")
    with Cluster("Compute Instance"):
        with Cluster("Applications"):
            userfacing = Docker("Streamlit")
            backend = Docker("FastAPI")
            userfacing - Edge(label = "API calls", color="red", style="dashed") - backend
        
        with Cluster("Database"):
            db = Mysql("IAM")

        with Cluster("Batch Process"):
            airflow = Airflow("Streamlit")
            GE = Telemetry("Data Quality Check")
            hosting = Nginx("Reports")

    backend << Edge(label="Verify Login",color = "red") << db
    devlopers = User("Developers")
    dataset = S3("AWS S3 Open Dataset")

    GE << Edge(label="CSV of metadata",color="blue") << db
    GE >> Edge(label="Host the static html report",color="blue") >> hosting
    airflow >> Edge(label="Run Great Expectation",color="blue") >> GE

    airflow << Edge(label="metadata collection",color="green") << dataset
    airflow >> Edge(label="Update AWS bucket metadata",color="blue") >> db

    ingress >> Edge(label = "Login to Dashboard",color="blue") << userfacing
    devlopers << Edge(label = "View Reports",color="blue") << hosting
    devlopers << Edge(label = "View Dashboard",color="blue") << airflow