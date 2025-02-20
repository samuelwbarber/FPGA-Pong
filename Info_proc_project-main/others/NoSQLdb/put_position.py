from pprint import pprint
import boto3

# put position of ball and paddles into the table
def put_position(GameID, IndexVal, PosBallX, PosBallY, PosPaddle0, PosPaddle1, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')

    table = dynamodb.Table('SaveGame')
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
    return response

if __name__ == '__main__':
    position_resp = put_position(10000, 2, 0, 0, 0, 1)
    print("Put position succeeded:")
    pprint(position_resp, sort_dicts=False)

# use for-loop to store each position into the table?
