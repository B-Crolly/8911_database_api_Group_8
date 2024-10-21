import logging
import json
import azure.functions as func
from azure.cosmos import CosmosClient
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing POST request to create a customer.')

    try:
        # Parse request body
        req_body = req.get_json()
        if not req_body:
            return func.HttpResponse(
                "Invalid request body",
                status_code=400
            )

        # Initialize the Cosmos client
        cosmos_db_connection_string = os.environ['CosmosDBConnectionString']
        client = CosmosClient.from_connection_string(cosmos_db_connection_string)

        # Set database and container
        database_name = 'Clients'
        container_name = 'Customers'
        database = client.get_database_client(database_name)
        container = database.get_container_client(container_name)

        # Create a new Customer
        container.create_item(body=req_body)

        # Return the created Customer
        return func.HttpResponse(
            body=json.dumps(req_body, default=str),
            status_code=201,
            mimetype='application/json'
        )

    except ValueError:
        return func.HttpResponse('Invalid JSON', status_code=400)
    except Exception as e:
        logging.error(f'Error: {e}')
        return func.HttpResponse('Internal server error', status_code=500)