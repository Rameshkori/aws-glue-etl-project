import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node Amazon S3
AmazonS3_node1776845546085 = glueContext.create_dynamic_frame.from_catalog(database="project1_db", table_name="customers", transformation_ctx="AmazonS3_node1776845546085")

# Script generated for node Drop Fields
DropFields_node1776845558913 = DropFields.apply(frame=AmazonS3_node1776845546085, paths=["phone 2"], transformation_ctx="DropFields_node1776845558913")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=DropFields_node1776845558913, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1776845488922", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1776845794434 = glueContext.write_dynamic_frame.from_options(frame=DropFields_node1776845558913, connection_type="s3", format="glueparquet", connection_options={"path": "s3://glue-toto-bucket1/transformed_zone/", "partitionKeys": []}, format_options={"compression": "snappy"}, transformation_ctx="AmazonS3_node1776845794434")

job.commit()