import boto3
import datetime
from boto3.dynamodb.conditions import Key

def get_data(timestamp, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url='dynamodb.us-east-1.amazonaws.com')

    table = dynamodb.Table('hb_temp_data')

    response = table.query(KeyConditionExpression=Key('timestamp').ge(timestamp))
    return response['Items']


if __name__ == '__main__':
   now  = datetime.datetime.now()
   print(now)
   query_timestamp = now.timestamp()
   print('timestamp =', query_timestamp)
   data = get_data(query_timestamp)
   for q_data in data:
      print(data['temperature'], ":", data['heartbeats'])
