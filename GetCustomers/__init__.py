import logging
import json
import azure.functions as func
from azure.cosmos import CosmosClient, exceptions
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing GET request for all customers.')

    try:
        # Initialize the Cosmos client
        cosmos_db_connection_string = os.environ['CosmosDBConnectionString']
        client = CosmosClient.from_connection_string(cosmos_db_connection_string)

        # Set database and container
        database_name = 'Clients'
        container_name = 'Customers'
        database = client.get_database_client(database_name)
        container = database.get_container_client(container_name)

        # Query all customers
        query = 'SELECT * FROM c'
        items = list(container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))

        # Return the list of customers
        return func.HttpResponse(
            body=json.dumps(items, default=str),
            status_code=200,
            mimetype='application/json'
        )

    except Exception as e:
        logging.error(f'Error: {e}')
        return func.HttpResponse('Internal server error', status_code=500)