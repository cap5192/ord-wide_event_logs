import os
from dotenv import load_dotenv
import pandas as pd
import meraki

# load all environment variables
load_dotenv()

def get_orgs():
    """Gets the list of all orgs (name and id) that admin has access to"""
    orgs = []
    dict = {"id": "", "name": ""}
    dashboard = meraki.DashboardAPI(api_key=os.environ['MERAKI_API_TOKEN'], output_log=False, print_console=False)
    response = dashboard.organizations.getOrganizations()

    for i in response:
        dict["id"] = i["id"]
        dict["name"] = i["name"]
        orgs.append(dict)
        dict = {"id": "", "name": ""}

    return orgs

def get_networks(org_id):
    """Get a list of networks and returns dict with net IDs and names"""
    nets = []
    dict = {"id": "", "name": ""}
    # collect network names
    dashboard = meraki.DashboardAPI(api_key=os.environ['MERAKI_API_TOKEN'], output_log=False, print_console=False)
    response = dashboard.organizations.getOrganizationNetworks(
        org_id, total_pages='all'
    )
    for i in response:
        dict["id"] = i["id"]
        dict["name"] = i["name"]
        nets.append(dict)
        dict = {"id": "", "name": ""}

    return nets

def get_network_product_types(net_id):
    dashboard = meraki.DashboardAPI(api_key=os.environ['MERAKI_API_TOKEN'], output_log=False, print_console=False)
    response = dashboard.networks.getNetwork(
        net_id
    )
    return response['productTypes']

def net_id_name_conversion(net_id):
    dashboard = meraki.DashboardAPI(api_key=os.environ['MERAKI_API_TOKEN'], output_log=False, print_console=False)
    response = dashboard.networks.getNetwork(
        net_id
    )
    return response['name']

def get_event_logs(net_id, product_type):
    dashboard = meraki.DashboardAPI(api_key=os.environ['MERAKI_API_TOKEN'], output_log=False, print_console=True)
    print(f"exporting logs for network {net_id_name_conversion(net_id)} {product_type} logs")
    response = dashboard.networks.getNetworkEvents(
        net_id,
        total_pages='all',
        productType=product_type,
        perPage=1000
    )
    network_name = net_id_name_conversion(net_id)
    event_logs_df = pd.DataFrame(response)
    event_logs_df.to_csv(f"{network_name}_{product_type}.csv")

