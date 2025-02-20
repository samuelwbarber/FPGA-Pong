import boto3
from boto3.dynamodb.conditions import Key

def put_position(GameID, IndexVal, PosBallX, PosBallY, PosPaddle0, PosPaddle1, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')

    table = dynamodb.Table('SaveGame')
    try:
        response = table.put_item(
            Item={
                'GameID': GameID,
                'IndexVal': IndexVal,
                'Positions': {
                    'PosBallX': PosBallX,
                    'PosBallY': PosBallY,
                    'PosPaddle0': PosPaddle0,
                    'PosPaddle1': PosPaddle1
                }
            }
        )
    except Exception as e:
        print(f"Error putting position: {e}")
    
    else:
        return response

def query_position(GameID, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')

    table = dynamodb.Table('SaveGame')
    try:
        response = table.query(
            KeyConditionExpression=Key('GameID').eq(GameID)
        )
    except Exception as e:
        print(f"Error querying position: {e}")
    
    else:
        return response['Items']

# example of putting positions into DynamoDB
put_position(10000, 5, 0, 0, 0, 0)
put_position(10000, 6, 0, 0, 0, 0)
put_position(10000, 7, 0, 0, 0, 0)

# example of querying positions from DynamoDB
positions = query_position(10000)
for position in positions:
    print("GameID: ", position['GameID'], " IndexVal: ", position['IndexVal'])
    positions_data = position['Positions']
    # extract each position
    print("PosBallX:", positions_data['PosBallX'])
    print("PosBallY:", positions_data['PosBallY'])
    print("PosPaddle0:", positions_data['PosPaddle0'])
    print("PosPaddle1:", positions_data['PosPaddle1'])
