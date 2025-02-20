import boto3

def create_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')

    table = dynamodb.create_table(
        TableName='SaveGame',
        KeySchema=[
            {
                'AttributeName': 'GameID',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'IndexVal',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'GameID',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'IndexVal',
                'AttributeType': 'N'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table



if __name__ == '__main__':
    savegame = create_table()
    print("Table status:", savegame.table_status)
