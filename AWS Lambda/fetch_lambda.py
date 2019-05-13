import json
import boto3
import time

# add a price dictionary to store all price information
price_dict = {
	"Banana": "59.99",
	"Apple": "108.99",
	"Orange": "79.99",
	"Cookie": "2000.88",
	"Coke": "20",
	"Water": "20"
}

# recommendation algorithm
def get_co_matrix(input_data):
    data = list()
    current_item = {
        'user_id': input_data["user_id"],
        'item_name': input_data["item"]
    }
    data.append(current_item)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('shopping_history')
    # add current shopping record to covariance matrix
    response = table.scan()
    for entry in response["Items"]:
        temp = dict()
        temp["user_id"] = entry['shopping_index']
        print(type(entry['item']))
        temp["item_name"] = list(entry['item'])
        data.append(temp)
    print(data)
    item_to_user = {}
    user_to_index = {}
    unique_user = set()
    user_count = 0
    user_to_count = []
    for entry in data:
        cur_id = entry['user_id']
        cur_items = entry['item_name']

        if cur_id not in unique_user:
            unique_user.add(cur_id)
            user_to_index[cur_id] = user_count
            user_to_count.append(set(cur_items))
            user_count += 1

        for cur_item in cur_items:

            if cur_item in item_to_user.keys():
                item_to_user[cur_item].add(cur_id)
            else:
                item_to_user[cur_item] = set()
                item_to_user[cur_item].add(cur_id)
    # add all previous shopping record into covariance matrix
    temp_co_matrix = [0] * user_count
    co_matrix = list()
    for i in range(0, user_count):
        co_matrix.append(temp_co_matrix)
    for item, user_list in item_to_user.items():
        user_list = list(user_list)
        for i in range(len(user_list)):
            for j in range(i + 1, len(user_list)):
                co_matrix[user_to_index[user_list[i]]][user_to_index[user_list[j]]] += 1
                co_matrix[user_to_index[user_list[j]]][user_to_index[user_list[i]]] += 1
    print(co_matrix)
    return (item_to_user, user_to_index, co_matrix, user_to_count)


def recommend(input_data):
    user_id = input_data["user_id"]
    (item_to_user, user_to_index, co_matrix, user_to_count) = get_co_matrix(input_data)
    target_index = user_to_index[user_id]
    most_similar_index = 0
    max_w = 0
    user_weight = {}
    item_weight = {}
    # calculate weight of each item based on user preference similarities
    for user in user_to_index.keys():
        if user == user_id:
            continue
        cur_index = user_to_index[user]
        w = co_matrix[target_index][cur_index] / (len(user_to_count[target_index] | user_to_count[cur_index]))
        print(user_id, user, w)
        user_weight[cur_index] = w
        if w > max_w:
            max_w = w
            most_similar_index = cur_index
    for item, user_list in item_to_user.items():
        item_weight[item] = 0
        cur_user_set = set(list(map(lambda x: user_to_index[x], user_list)))

        cur_user_set.add(most_similar_index)
        print(item, cur_user_set)
        for user in cur_user_set:
            if user != target_index:
                item_weight[item] += user_weight[user]
    print(item_weight)
    for item in user_to_count[target_index]:
        item_weight.pop(item)
        # for user in user_list:
    print(item_weight)
    what_to_recommend = ''
    max_index = 0
    for key, value in item_weight.items():
        if value>max_index:
            max_index = value
            what_to_recommend = key
    return what_to_recommend


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('shopping_cart')
    response = table.scan()
    result = list()
    current_list = dict()
    current_list['user_id'] = int(time.time())
    current_list['item'] = list()
    # collect all unpaid items associated to this userid
    for item in response["Items"]:
        if (item["user_id"]==event["request"]) and (item["payment"]=="unpaid"):
            temp = dict()
            temp["item"] = item["item"]
            if float(item["amount"]) > 50:
                temp["amount"] = str(float(item["amount"])/1000)
            else:
                temp["amount"] = item["amount"]
            temp["price"] = item["price"]
            print(temp)
            current_list['item'].append(item["item"])
            result.append(temp)
    print(result)
    # make recommendation
    recommend_temp = recommend(current_list)
    print("Recommendation", recommend_temp)
    recommend_item = {
        'item': "Recommendation",
        'amount': recommend_temp,
        'price': price_dict[recommend_temp]
    }
    # send to mobile application through API gateway
    result.append(recommend_item)
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
