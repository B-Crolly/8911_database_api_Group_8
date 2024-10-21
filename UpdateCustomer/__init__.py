import logging
import json
import azure.functions as func
from azure.cosmos import CosmosClient, exceptions
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing PUT request to update a customer entry.')

    try:
        item_id = req.route_params.get('id')
        if not item_id:
            return func.HttpResponse("Item ID is required.", status_code=400)

        req_body = req.get_json()
        if not req_body:
            return func.HttpResponse("Invalid request body", status_code=400)

        # Initialize the Cosmos client
        cosmos_db_connection_string = os.environ['CosmosDBConnectionString']
        client = CosmosClient.from_connection_string(cosmos_db_connection_string)

        # Set database and container
        database_name = 'Clients'
        container_name = 'Customers'
        database = client.get_database_client(database_name)
        container = database.get_container_client(container_name)

        # Read the existing customer
        item = container.read_item(item=item_id, partition_key=item_id)

        # Update the customer entry
        for key in req_body:
            item[key] = req_body[key]

        container.upsert_item(body=item)

        return func.HttpResponse(
            body=json.dumps(item, default=str),
            status_code=200,
            mimetype='application/json'
        )

    except exceptions.CosmosResourceNotFoundError:
        return func.HttpResponse('Customer not found', status_code=404)
    except ValueError:
        return func.HttpResponse('Invalid JSON', status_code=400)
    except Exception as e:
        logging.error(f'Error: {e}')
        return func.HttpResponse('Internal server error', status_code=500)