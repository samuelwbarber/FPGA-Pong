import boto3
from boto3.dynamodb.conditions import Key

def query_position(GameID, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')

    table = dynamodb.Table('SaveGame')
    response = table.query(
        KeyConditionExpression=Key('GameID').eq(GameID)
    )
    return response['Items']

if __name__ == '__main__':
    query_ID = 10000
    print(f"Positions from {query_ID}")
    positions = query_position(query_ID)
    for position in positions:
        print("GameID: ", position['GameID'], " IndexVal: ", position['IndexVal'])
        positions_data = position['Positions']
        # extract each position
        print("PosBallX:", positions_data['PosBallX'])
        print("PosBallY:", positions_data['PosBallY'])
        print("PosPaddle0:", positions_data['PosPaddle0'])
        print("PosPaddle1:", positions_data['PosPaddle1'])
        