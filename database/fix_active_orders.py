from boto3.dynamodb.conditions import Key

import database


response = database.profile_users.query(KeyConditionExpression=Key('id_user').eq(id))
last_item = response['Items'][-1]
num_active = last_item['number-active']
response1 = database.profile_users.update_item(Key={'id_user': id},
                                               UpdateExpression='SET  number-active = :a',
                                               ExpressionAttributeValues={':a': num_active - 1})

