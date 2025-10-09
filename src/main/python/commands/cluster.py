from client.client import Client

from .filter import append_row_to_excel

def get_interfaces(client: Client, args: list):
    cluster_name = args[0]
    interfaces = client.api_call('show-simple-cluster',{'name':cluster_name}).response()['data']['interfaces']['objects']
    for interface in interfaces:
        name = interface['name']
        topology = interface['topology']
        cluster_ip = interface['ipv4-address']
        mask = '' if cluster_ip == '' else interface['ipv4-mask-length']
        ip = f'{cluster_ip}/{mask}'
        comments = interface['comments']
        append_row_to_excel('interface-report.xlsx', cluster_name, [name,topology,ip,comments], headers=['Interface','Topology','IP Address','Comments'])
    return
