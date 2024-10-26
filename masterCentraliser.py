import json
import random

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
    total_sales = sum(store_data['sales']['monthly_sales'])
    net_profit = calculate_net_profit(store_data['sales']['monthly_sales'], store_data['expenses'])
    promotion_effectiveness = evaluate_promotion_effectiveness(store_data['sales'], store_data['promotions']['promotion_effectiveness'])
    
    return {
        'store_id': store_data['store_id'],
        'total_sales': total_sales,
        'net_profit': net_profit,
        'promotion_effectiveness': promotion_effectiveness,
        'predicted_sales_next_month': store_data['sales']['predicted_sales_next_month']
    }

# Fonction pour charger les données des magasins à partir d'un fichier JSON
def load_stores_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

if __name__ == '__main__':
    stores_data = load_stores_data('stores1.json')
    total_sales_sum = 0
    total_net_profit = 0
    results = []

    # Traitement des données pour chaque magasin
    for store_data in stores_data:
        result = process_sales_data(store_data)
        results.append(result)
        total_sales_sum += result['total_sales']
        total_net_profit += result['net_profit']
        
        # Affichage des résultats pour chaque magasin
        print(f"Magasin {result['store_id']}:")
        print(f"  Ventes totales: {result['total_sales']}")
        print(f"  Bénéfice net: {result['net_profit']}")
        print(f"  Efficacité promotionnelle: {result['promotion_effectiveness']}")
        print(f"  Ventes prévues pour le mois prochain: {result['predicted_sales_next_month']}")
        print("-" * 30)
    
    # Affichage des résultats globaux
    print(f"Total des ventes pour tous les magasins: {total_sales_sum}")
    print(f"Bénéfice net total pour tous les magasins: {total_net_profit}")
    
    # Identifier le magasin avec le plus grand chiffre d'affaires
    max_sales_store = max(results, key=lambda x: x['total_sales'])
    print(f"Le magasin avec le plus grand chiffre d'affaires est {max_sales_store['store_id']} avec {max_sales_store['total_sales']}.")
