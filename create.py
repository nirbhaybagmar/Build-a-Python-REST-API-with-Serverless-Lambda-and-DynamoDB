import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.create_table(
	TableName='responseTable',
	KeySchema=[
		{
			'AttributeName': 'formId', 
			'KeyType': 'HASH'
		},
		
	], 
	AttributeDefinitions=[
		{
			'AttributeName': 'formId', 
			'AttributeType': 'S'
		}
		
	], 
	ProvisionedThroughput={
		'ReadCapacityUnits': 5, 
		'WriteCapacityUnits': 5
	}
)

