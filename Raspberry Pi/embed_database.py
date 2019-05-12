import boto3
import time
import csv
from boto3.dynamodb.conditions import Key, Attr
import aws


price_dict = {
    "Coke": "1.88",
    "Apple": "2.08"
}

def db_operation(userid, item, amount):
    dynamodb = aws.getResource('dynamodb', 'us-east-1')
    DYNAMO_TABLE_NAME = "shopping_cart"
    table_dynamo = dynamodb.Table(DYNAMO_TABLE_NAME)
    response = table_dynamo.scan()
    current_record = None
    for record in response['Items']:
        if (record["user_id"] == userid) and (record["item"] == item) and (record["payment"]=="unpaid"):
            current_record = record
    if (current_record == None) and (amount>0):
        response = table_dynamo.put_item(
            Item={
                'timestamp': str(time.time()),
                'user_id': userid,
                'amount': amount,
                'price': price_dict[item],
                'item': item,
                'payment':"unpaid"
            }
        )
        return
    elif (current_record != None) and (amount<0):
        table_dynamo.delete_item(Key={'timestamp': current_record["timestamp"]})
    elif (current_record != None) and (amount>0):
        response = table_dynamo.update_item(
            Key={
                'timestamp': current_record["timestamp"]
            },
            UpdateExpression="set amount = :a",
            ExpressionAttributeValues={
                ':a': str(float(current_record["amount"]) + float(amount))
            },
            ReturnValues="UPDATED_NEW"
        )


def s3_operation(filename, userid, amount):
    s3 = aws.getResource('s3', 'us-east-1')
    s3.Bucket('iot-bucket-llha').upload_file(filename, userid+'_'+amount+'.jpg')

db_operation("thisisuserid", "Coke")

#s3_operation('thisisuserid_2.jpg','thisisuserid','2.2')