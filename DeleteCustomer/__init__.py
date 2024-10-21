import logging
import azure.functions as func
from azure.cosmos import CosmosClient, exceptions
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing DELETE request to delete a customer')

    try:
        item_id = req.route_params.get('id')
        if not item_id:
            return func.HttpResponse("Customer ID is required.", status_code=400)

        # Initialize the Cosmos client
        cosmos_db_connection_string = os.environ['CosmosDBConnectionString']
        client = CosmosClient.from_connection_string(cosmos_db_connection_string)

        # Set database and container
        database_name = 'Clients'
        container_name = 'Customers'
        database = client.get_database_client(database_name)
        container = database.get_container_client(container_name)

        # Delete the customer
        container.delete_item(item=item_id, partition_key=item_id)

        return func.HttpResponse(status_code=204)

    except exceptions.CosmosResourceNotFoundError:
        return func.HttpResponse('Customer not found', status_code=404)
    except Exception as e:
        logging.error(f'Error: {e}')
        return func.HttpResponse('Internal server error', status_code=500)