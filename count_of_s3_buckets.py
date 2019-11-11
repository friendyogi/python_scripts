import boto3

# Purpose: 
# This script can be used to pull count of S3 buckets
#           group by aws account Id
# Then post the results to DataDog metrics using DataDog REST API Client api.Metric.send

from datadog import initialize
#from collections import Counter

options = {
    'api_key':'xxx'
}

initialize(**options)

# Use Datadog REST API client
from datadog import api

# EU, DS, Dev, PROD
keys=['xxx',
      'xxx',
      'xxx',
      'xxx']
secrets=['xxx+xxx/xxx',
         'xxx+xxx/F/xxx',
         'xxx',
         'xxx/xxx']

for (key,secret) in zip(keys,secrets):
	s3 = boto3.resource('s3', aws_access_key_id=key,
                             aws_secret_access_key=secret)
	client = boto3.client("sts", aws_access_key_id=key,
                              aws_secret_access_key=secret)
        account_id = client.get_caller_identity()["Account"]
	count = 0
	for bucket in s3.buckets.all():
        	count = count +1
	tag={}
	tag.update({'aws_account':account_id})
	point=count
	api.Metric.send(metric='count_of_s3_bucket', points=point, tags=tag)
