import boto3, time
from datadog import initialize

# Purpose: 
# This script can be used to pull count of EC2s
#           group by instanceType like m4.xlarge, t2.medium, etc.
#           group by aws account Id
#           group by tags like project, stack, etc.
#           group by instance state like running, stopped, etc.
# Then post the results to DataDog metrics using DataDog REST API Client api.Metric.send

# Your datadop api key here:
options = {
    'api_key':'xxx'
}

initialize(**options)

# Use Datadog REST API client
from datadog import api

# Your AWS Keys here
keys=['xxx',
      'xxx',
      'xxx',
      'xxx']
secrets=['xxx+xxx/xxx',
         'xxx+xxx/F/xxx',
         'xxx',
         'xxx/xxx']

regions=['us-east-1',
         'us-east-2',
         'us-west-1',
         'us-west-2',
         'eu-central-1',
         'eu-north-1',
         'eu-west-3',
         'eu-west-2',
         'eu-west-1',
         'ap-south-1',
         'ap-northeast-2',
         'ap-northeast-1',
         'ap-southeast-1',
         'ap-southeast-2',
         'sa-east-1',
         'ca-central-1'
]

for region in regions:
    for (key,secret) in zip(keys,secrets):
        ec2 = boto3.resource('ec2', aws_access_key_id=key,
                             aws_secret_access_key=secret, region_name=region)
        client = boto3.client("sts", aws_access_key_id=key,
                              aws_secret_access_key=secret,
                              region_name=region)
        account_id = client.get_caller_identity()["Account"]
        ids = []
        state = []
        instance_type = []
        stack = []
        project = []
        response = ec2.instances.all()
        for i in response:
            ids.append(i.id)
            state.append(i.state['Name'])
            instance_type.append(i.instance_type)
            for t in i.tags:
              key=t['Key']
              value=t['Value']
              if key.lower() == "stack":
                stack.append(value)
              if key.lower() == "project":
                project.append(value)

        # State = All
        tag={}
        tag.update({'aws_account':account_id,'region':region,'state':'all'})
        point=len(ids)
        api.Metric.send(metric='count_of_ec2', points=point, tags=tag)

        # Group by State
        result = dict((i, state.count(i)) for i in state)
        tag={}
        for key, val in result.items():
                tag.update({'aws_account':account_id,'region':region,'state':key})
                point=val
                api.Metric.send(metric='count_of_ec2', points=point, tags=tag)

        # Group by Instance Type
        result = dict((i, instance_type.count(i)) for i in instance_type)
        tag={}
        for key, val in result.items():
          tag.update({'aws_account':account_id,'region':region,'instanceType':key})
          point=val
          api.Metric.send(metric='count_of_ec2', points=point, tags=tag)

        # Group by Stack type, example dev, prod, test, qa
        result = dict((i, stack.count(i)) for i in stack)
        tag={}
        for key, val in result.items():
          tag.update({'aws_account':account_id,'region':region,'Stack':key})
          point=val
          api.Metric.send(metric='count_of_ec2', points=point, tags=tag)

        # Group by Project type like, api, gateway, db, etc
        result = dict((i, project.count(i)) for i in project)
        tag={}
        for key, val in result.items():
          tag.update({'aws_account':account_id,'region':region,'Project':key})
          point=val
          api.Metric.send(metric='count_of_ec2', points=point, tags=tag)

