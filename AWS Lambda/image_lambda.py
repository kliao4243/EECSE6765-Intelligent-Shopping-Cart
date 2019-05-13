import json
import boto3
import time

price_dict = {
	"Banana": "59.99",
	"Apple": "108.99",
	"Orange": "79.99"
}

# call Rekognition API to get tags of uploaded image
def detect_labels(bucket, key):
	rekognition = boto3.client('rekognition')
	response = rekognition.detect_labels(
		Image={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		},
		MaxLabels=20,
		MinConfidence=90
	)
	print(response['Labels'])
	return response['Labels']
# update database based on tag, weight change, and items currently in Database
def writeDatabase(info):
	dynamodb = boto3.resource('dynamodb')
	table_name = 'shopping_cart'
	userId = info["userId"]
	item = info["item"]
	unit = info["unit"]
	amount = info["amount"]
	price = info["price"]
	table = dynamodb.Table('shopping_cart')
	response = table.scan()
	key_id = ""
	current_item = None
	for entry in response["Items"]:
		if (entry["user_id"]==userId) and (entry["item"]==item) and (entry["payment"]=="unpaid"):
			key_id = entry["timestamp"]
			current_item = entry
	if (key_id == "") and (int(amount)>0):
		response = table.put_item(
			Item={
                'timestamp': str(time.time()),
                'user_id': userId,
                'amount': amount,
                'price': price,
                'item': item,
                'payment':"unpaid"
            }
		)
	elif(key_id != ""):
		if float(current_item["amount"])+float(amount) < 50/1000: #to be modified
			response = table.delete_item(
		        Key={
		            'timestamp': key_id
		        }
		    )
		else:
			response = table.update_item(
	            Key={
	                'timestamp':key_id
	            },
	            UpdateExpression="set amount = :a",
	            ExpressionAttributeValues={
                    ':a': str(float(current_item["amount"])+float(amount))
                },
                ReturnValues="UPDATED_NEW"
	       )

	#print(response)

# after being processed by Rekognition, delete item from S3
def delete_from_S3(BUCKET, OBJECT):
	s3 = boto3.resource('s3')
	s3.Object(BUCKET, OBJECT).delete()

def lambda_handler(event, context):
	possible_item = ["Apple", "Banana", "Orange"]
	BUCKET = event["Records"][0]["s3"]["bucket"]["name"]
	OBJECT = event["Records"][0]["s3"]["object"]["key"]
	print(BUCKET, OBJECT)
	results = detect_labels(BUCKET, OBJECT)
	item = ""
	for result in results:
		if (result['Name'] == 'Grapefruit') or (result['Name']=='Citrus Fruit'):
			item = 'Orange'
		if result['Name'] in possible_item:
			item = result['Name']
	userId, amount = OBJECT.strip('.jpg').split('_')
	print(userId, item)
	info = {
		"userId": userId,
		"item": item,
		"amount": amount,
		"unit": "kg",
		"price": price_dict[item]
	}
	writeDatabase(info)
	delete_from_S3(BUCKET, OBJECT)
	return {
	    'statusCode': 200,
	    'body': json.dumps("llha")
	}
