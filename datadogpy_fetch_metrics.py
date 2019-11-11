import boto3, time

# Purpose:
# This script is used to poll metrics from datadog by using datadogpy api.Metric.query
# In this example, we are fetching rabbitmq metrics, example rabbitmq.queue.messages

from datadog import initialize, api

options = {
    'api_key':'xxx',
    'app_key':'xxx'
}

initialize(**options)

# Use Datadog REST API client

def get_avg_queue_count(now):
    queue_count = 0
    counter = 0
    query = 'avg:rabbitmq.queue.messages{rabbitmq_queue:queuename,rabbitmqinstance:instancename}'
    result = api.Metric.query(start=now - 600, end=now, query=query)
    for output1 in result['series']:
        for output2 in output1['pointlist']:
            for output3 in output2[1::2]:
                if output3 > 0:
                    counter = counter + 1
                    queue_count = queue_count + output3
                    print output3
    avg_queue_count = queue_count / counter
    return avg_queue_count

avg_queue_count=get_avg_queue_count(int(time.time()))
print "Average Queue Count:", avg_queue_count
if avg_queue_count >= 5000:
    print "Number of messages in Queue is high"
elif avg_queue_count < 5000:
    print "Relax"
