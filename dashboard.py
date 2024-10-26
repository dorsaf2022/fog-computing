import json
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Charger les données à partir du fichier JSON
with open('stores1.json') as f:
    data = json.load(f)

# Préparation des données pour le DataFrame
results = []
for store in data:
    total_sales = sum(store['sales']['monthly_sales'])
    net_profit = total_sales - sum(store['expenses'].values())
    
    results.append({
        "store_id": store['store_id'],
        "store_name": store['store_name'],
        "total_sales": total_sales,
        "net_profit": net_profit,
        "promotion_effectiveness": store['promotions']['promotion_effectiveness'],
        "predicted_sales_next_month": store['sales']['predicted_sales_next_month']
    })

# Créer un DataFrame pour faciliter les visualisations avec Plotly
df = pd.DataFrame(results)

# Initialiser l'application Dash
app = dash.Dash(__name__)

# Créer des graphiques interactifs avec Plotly
sales_fig = px.bar(df, x='store_name', y='total_sales', title='Total Sales per Store',
                   labels={'store_name': 'Store Name', 'total_sales': 'Total Sales'})

profit_fig = px.bar(df, x='store_name', y='net_profit', title='Net Profit per Store',
                    labels={'store_name': 'Store Name', 'net_profit': 'Net Profit'})

promotion_fig = px.scatter(df, x='store_name', y='promotion_effectiveness', size='promotion_effectiveness',
                           title='Promotion Effectiveness per Store',
                           labels={'store_name': 'Store Name', 'promotion_effectiveness': 'Promotion Effectiveness (%)'})

predicted_sales_fig = px.line(df, x='store_name', y='predicted_sales_next_month', title='Predicted Sales Next Month',
                              labels={'store_name': 'Store Name', 'predicted_sales_next_month': 'Predicted Sales'})

# Disposition du tableau de bord
app.layout = html.Div(children=[
    html.H1(children='Business Intelligence Dashboard'),

    html.Div(children='''
        Aperçu des performances des magasins.
    '''),

    dcc.Graph(
        id='sales-graph',
        figure=sales_fig
    ),

    dcc.Graph(
        id='profit-graph',
        figure=profit_fig
    ),

    dcc.Graph(
        id='promotion-graph',
        figure=promotion_fig
    ),

    dcc.Graph(
        id='predicted-sales-graph',
        figure=predicted_sales_fig
    )
])

# Lancer l'application Dash
if __name__ == '__main__':
    app.run_server(debug=True)
