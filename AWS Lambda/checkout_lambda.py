import boto3
import time

def lambda_handler(event, context):
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('shopping_cart')
	response = table.scan()
	result = list()
	# create a temp to store unpaid items
	temp_list = list()
	for item in response["Items"]:
	    if item["user_id"]==event["request"]:
	    	temp_list.append(item['item'])
		# use timestamp as key, store current shopping record to history purchashing table
	    	temp_time = item["timestamp"]
		# set the status of these items to paid
	    	response = table.update_item(
	            Key={
	                'timestamp':temp_time
	            },
	            UpdateExpression="set payment = :p",
	            ExpressionAttributeValues={
                    ':p': "paid"
                },
                ReturnValues="UPDATED_NEW"
	       )
	table = dynamodb.Table('shopping_history')
	response = table.put_item(
		Item={
			'shopping_index': str(time.time()),
			'item':temp_list
        }
	)
	return {
        'statusCode': 200,
        'body': "Successfully Check Out"
    }
