import json
import socket
import pickle
import random
from concurrent.futures import ThreadPoolExecutor

# Fonction pour charger les données des magasins à partir d'un fichier JSON
def load_stores_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Fonction pour envoyer les données de vente à un slave
def send_sales_data_to_slave(store_data, host, port, retries=3):
    attempt = 0
    while attempt < retries:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                s.sendall(pickle.dumps(store_data))
                result = s.recv(4096)  # Augmenter la taille si nécessaire
                return pickle.loads(result)
        except Exception as e:
            print(f"Erreur de connexion avec le slave {host} (tentative {attempt+1}/{retries}): {e}")
            attempt += 1
            if attempt == retries:
                return None

# Fonction pour répartir les magasins de manière aléatoire entre les slaves
def distribute_stores_randomly(num_stores, slaves):
    store_ids = list(range(1, num_stores + 1))  # Liste des IDs des magasins
    random.shuffle(store_ids)  # Mélanger les IDs aléatoirement
    
    # Répartition aléatoire des magasins entre les slaves
    distributed_stores = []
    for i, slave in enumerate(slaves):
        num_stores_per_slave = len(store_ids) // len(slaves)
        if i == len(slaves) - 1:  # Dernier slave prend le reste des magasins
            assigned_stores = store_ids[i * num_stores_per_slave :]
        else:
            assigned_stores = store_ids[i * num_stores_per_slave : (i + 1) * num_stores_per_slave]
        distributed_stores.append({'id': set(assigned_stores), 'ip': slave['ip']})
    return distributed_stores

if __name__ == '__main__':
    stores_data = load_stores_data('stores1.json')
    slaves_info = [
        {'ip': '10.26.12.180'},
        {'ip': '10.26.14.210'},
        {'ip': '10.26.15.75'},
    ]
    port = 5000
    total_sales_sum = 0
    total_net_profit = 0
    results = []

    # Répartition aléatoire des magasins entre les slaves
    store_slaves = distribute_stores_randomly(len(stores_data), slaves_info)

    # Impression pour indiquer la répartition des magasins
    print("Répartition aléatoire des magasins pour chaque slave:")
    for store in store_slaves:
        print(f"Slave IP: {store['ip']} gère les magasins: {store['id']}")

    with ThreadPoolExecutor(max_workers=len(store_slaves)) as executor:
        futures = {}
        for store in store_slaves:
            for store_id in store['id']:
                # Impression avant d'envoyer les données au slave
                print(f"Envoi des données du magasin {store_id} au slave {store['ip']}")
                futures[executor.submit(send_sales_data_to_slave, stores_data[store_id - 1], store['ip'], port)] = store_id

        for future in futures:
            store_id = futures[future]
            try:
                result = future.result()
                if result:
                    print(f"Résultat du magasin {store_id}: {result}")
                    results.append(result)
                    total_sales_sum += result['total_sales']
                    total_net_profit += result['net_profit']
                else:
                    print(f"Aucun résultat reçu du magasin {store_id}")
            except Exception as e:
                print(f"Erreur lors de la réception des résultats du magasin {store_id}: {e}")

    print(f"Total des ventes: {total_sales_sum}")
    print(f"Bénéfice net total: {total_net_profit}")

    max_sales_store = None
    max_sales_value = 0

    for result in results:
        if result['total_sales'] > max_sales_value:
            max_sales_value = result['total_sales']
            max_sales_store = result['store_id']

    print(f"Le magasin avec le plus grand chiffre d'affaires est {max_sales_store} avec {max_sales_value}.")
