import backend

def main():
    """runs the program and repeats unless user cancels the prompt"""
    flag = True
    while flag:
        orgs = backend.get_orgs()
        x = 1
        y = 1
        z = 1
        for i in orgs:
            print(f"{x}. {i['name']}")
            x = x + 1
        org_num = int(input("Select an organization by its number: "))
        org = orgs[org_num - 1]
        org_id = org['id']

        network = backend.get_networks(org_id)
        for i in network:
            print(f"{y}. {i['name']}")
            y = y + 1
        net_num = int(input("Select a network by its number: "))
        net = network[net_num - 1]
        net_id = net['id']

        product_types = backend.get_network_product_types(net_id)
        for productType in product_types:
            print(f"{z}. {productType}")
            z = z + 1
        product_number = int(input("Select product type by its number: "))
        product_type = product_types[product_number -1]
        if product_type == 'sensor':
            print("Product type cannot be sensor, please run the script again.")
            break

        backend.get_event_logs(net_id, product_type)

        repeat = input("Would you like to run the script again? Y to continue N to exit: ")
        if repeat.lower() == 'y':
            flag = True
        else:
            flag = False


if __name__ == '__main__':
    main()
