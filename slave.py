import socket
import pickle

# Fonction pour calculer les bénéfices nets
def calculate_net_profit(sales, expenses):
    total_sales = sum(sales)
    total_expenses = expenses['rent'] + expenses['salaries'] + expenses['utilities']
    net_profit = total_sales - total_expenses
    return net_profit

# Fonction pour évaluer l'efficacité de la promotion
def evaluate_promotion_effectiveness(sales_data, promotion_effectiveness):
    avg_sales = sum(sales_data['last_year_sales']) / len(sales_data['last_year_sales'])
    increase_due_to_promotion = avg_sales * (promotion_effectiveness / 100)
    return increase_due_to_promotion

# Fonction pour traiter les données des ventes
def process_sales_data(store_data):
    # Afficher les données du magasin avant traitement
    print(f"Traitement des données du magasin {store_data['store_id']}...")
    print(f"Ventes mensuelles: {store_data['sales']['monthly_sales']}")
    print(f"Dépenses: {store_data['expenses']}")
    print(f"Efficacité de la promotion: {store_data['promotions']['promotion_effectiveness']}")
   
    total_sales = sum(store_data['sales']['monthly_sales'])  # Calcul des ventes totales
    net_profit = calculate_net_profit(store_data['sales']['monthly_sales'], store_data['expenses'])  # Calcul du bénéfice net
    promotion_effectiveness = evaluate_promotion_effectiveness(store_data['sales'], store_data['promotions']['promotion_effectiveness'])
   
    # Afficher les résultats après traitement
    print(f"Magasin {store_data['store_id']}:")
    print(f"  Ventes totales: {total_sales}")
    print(f"  Bénéfice net: {net_profit}")
    print(f"  Efficacité promotionnelle: {promotion_effectiveness}")
    print(f"  Ventes prévues pour le mois prochain: {store_data['sales']['predicted_sales_next_month']}")
   
    # Retourner les informations calculées
    return {
        'store_id': store_data['store_id'],
        'total_sales': total_sales,
        'net_profit': net_profit,
        'promotion_effectiveness': promotion_effectiveness,
        'predicted_sales_next_month': store_data['sales']['predicted_sales_next_month']
    }

if __name__ == '__main__':
    host = '0.0.0.0'  # Écouter sur toutes les interfaces
    port = 5000  # Port pour écouter

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print("Le slave attend des connexions...")

        while True:
            conn, addr = s.accept()
            with conn:
                print('Connecté à', addr)
                data = conn.recv(1024)  # Recevoir les données de vente
                store_data = pickle.loads(data)
                result = process_sales_data(store_data)  # Traiter les ventes
                conn.sendall(pickle.dumps(result))  # Envoyer le résultat au master





