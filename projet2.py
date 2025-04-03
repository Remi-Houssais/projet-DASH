# ========= Importation des libraries ======= #
import dash
from dash import html, dcc, dash_table
from dash.dependencies import Output, Input
import plotly.graph_objects as go
import dash_bootstrap_components as dbc 
import plotly.express as px
import pandas as pd
import numpy as np

# ======= Initialisation de l'application ======= #
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server 

# Chargement des données
df = pd.read_csv(r'C:\Users\Remih\OneDrive\Bureau\cours M1\python avancé\supermarket_sales.csv')

# ================= Traitement des données ================= #
df['Date'] = pd.to_datetime(df['Date'])  # Conversion de la colonne Date en datetime
df['Total'] = df['Unit price'] * df['Quantity'] # Calcul du montant total
df['Invoice ID'] = df['Invoice ID'].astype(str)

# Fonction pour calculer le montant total des achats
def montant_total_achats(data):
    return f"{data['Total'].sum():,.2f} €"

# Fonction pour calculer le nombre total d'achats
def nombre_total_achats(data):
    return f"{data['Invoice ID'].nunique()} achats"

# Fonction pour un unique histogramme des montants des achats par sexe
def histogramme_repartition_achats(data):
    # Création d'une palette de couleurs chaudes
    # Rouge profond pour les hommes et orange-doré pour les femmes
    fig = px.histogram(
        data,
        x="Total",
        color="Gender",
        title="Répartition des montants totaux des achats par sexe",
        labels={"Total": "Montant total des achats", "Gender": "Sexe"},
        color_discrete_map={"Female": "#FF9E4A", "Male": "#DB4325"},
        opacity=0.85   #transparence
    )
    
    # Personnalisation du style
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Fond transparent
        paper_bgcolor='rgba(0,0,0,0)',  # Fond transparent
        title_font=dict(size=22, color="#B33309"),  # Titre en rouge chaleureux
        legend_title_font=dict(size=14),
        font=dict(family="Arial", size=12, color="#555555")
    )
    
    
    
    return fig



#  Fonction pour diagramme circulaire de la répartition des catégories de produit
def diagramme_circulaire_produits(data):
    df_produits = data.groupby("Product line").agg({"Total": "sum"}).reset_index()
    
    # Création du diagramme avec une palette de couleurs chaudes
    fig = px.pie(
        df_produits,
        names="Product line",
        values="Total",
        title="Répartition des ventes par catégorie de produit",
        color_discrete_sequence=["#DB4325", "#FF9E4A", "#FFC75F", "#E67E22", "#B33309", "#FF5733", "#CD6155"]
    )
    
    # Personnalisation du style
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Fond transparent
        paper_bgcolor='rgba(0,0,0,0)',
        title_font=dict(size=22, color="#B33309"),  # Titre 
        legend_title_font=dict(size=14)
    )
    
    # Personnalisation des tracés
    fig.update_traces(
        textfont=dict(size=12, color='white'),  # Texte blanc 
        marker=dict(line=dict(color='#FFFFFF', width=1))  # Bordure blanche entre segments   
    )
    return fig

def evolution_ventes_par_semaine(data):
    # Création de la colonne semaine
    data['Week'] = data['Date'].dt.strftime('%U')
    df_semaine = data.groupby("Week").agg({"Total": "sum"}).reset_index()
    
    # Création du graph
    fig = px.line(
        df_semaine,
        x="Week",
        y="Total",
        title="Évolution du montant total des achats par semaine",
        labels={"Week": "Semaine", "Total": "Montant total des achats"},
        markers=True,
        line_shape="spline", 
    )
    
    # Application du style cohérent avec les graphiques précédents
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)',
        title_font=dict(size=22, color="#B33309"),  
        font=dict(family="Arial", size=12, color="#555555")
    )
    
    # Personnalisation de la ligne et des marqueurs
    fig.update_traces(
        line_color="#DB4325",  # Rouge chaleureux pour la ligne
        line_width=3,  # Épaisseur de ligne
        marker=dict(
            size=8,
            color="#FF9E4A"
        )
    )

    # changement des axes de fond
    fig.update_xaxes(
        showgrid=True,
        gridwidth=0.5,
        gridcolor='rgba(211,211,211,0.3)'
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=0.5,
        gridcolor='rgba(211,211,211,0.3)'
    )
    
    return fig

# ============ Layout =============== #
app.layout = dbc.Container([

    dbc.Row([
        dbc.Col(html.H1("Tableau de bord des ventes du supermarché", className="text-white", style={"font-size": "25px"}), width=6),
        dbc.Col([
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(
                        id='drop-1',
                        options=[{'label': ville, 'value': ville} for ville in df['City'].dropna().unique()],
                        placeholder="Choisissez une ville",
                        style={"height": "40px", "width": "100%"}
                    ),
                    width=6
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='drop-2',
                        options=[{'label': gender, 'value': gender} for gender in df['Gender'].dropna().unique()],
                        placeholder="Choisissez un sexe",
                        style={"height": "40px", "width": "100%"}
                    ),
                    width=6
                ),
            ]) 
        ], width=6),
    ],  style={"background-color": "#CD6155", "padding": "10px"}),

    # Première ligne avec les indicateurs stylisés

dbc.Row([
    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.H5("Montant total des achats", className="card-title"),
                html.H3(id='montant-total', className="card-text", style={"fontWeight": "bold"})
            ])
        ], className="shadow-sm text-white", style={"backgroundColor": "#DB4325", "padding": "10px", "borderRadius": "10px"})  # Couleur personnalisée
    ], width=6),

    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.H5("Nombre total d'achats", className="card-title"),
                html.H3(id='nombre-achats', className="card-text", style={"fontWeight": "bold"})
            ])
        ], className="shadow-sm text-white", style={"backgroundColor": "#E67E22", "padding": "10px", "borderRadius": "10px"})  # Couleur personnalisée
    ], width=6),
], style={"marginTop": "20px"}),


    # Graphiques (Histogramme + Diagramme circulaire)
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='histogramme-ventes', config={'displayModeBar': False})
        ], width=6),
        
        dbc.Col([
            dcc.Graph(id='diagramme-circulaire', config={'displayModeBar': False})
        ], width=6),
    ], style={"marginTop": "20px"}),

    # Graphique d'évolution des ventes 
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='graphique-evolution', config={'displayModeBar': False})
        ], width=12),
    ], style={"marginTop": "20px"}),

], fluid=True, style={"backgroundColor": "#FFF5EB", "minHeight": "100vh", "padding": "20px"})

# 🔹 Callback pour mettre à jour les graphiques et indicateurs selon les filtres
@app.callback(
    [
        Output('montant-total', 'children'),
        Output('nombre-achats', 'children'),
        Output('histogramme-ventes', 'figure'),
        Output('diagramme-circulaire', 'figure'),
        Output('graphique-evolution', 'figure')
    ],
    [Input('drop-1', 'value'),
     Input('drop-2', 'value')]
)
def update_graphs(selected_city, selected_gender):
    
    # Filtrage des données en fonction des filtres sélectionnés
    filtered_df = df.copy()
    if selected_city:
        filtered_df = filtered_df[filtered_df['City'] == selected_city]
    if selected_gender:
        filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]
    
    # Calcul des indicateurs
    montant_total = montant_total_achats(filtered_df)
    nombre_achats = nombre_total_achats(filtered_df)
    
    # Mise à jour des graphiques
    fig_histogramme = histogramme_repartition_achats(filtered_df)
    fig_pie = diagramme_circulaire_produits(filtered_df)
    fig_evolution = evolution_ventes_par_semaine(filtered_df)

    return montant_total, nombre_achats, fig_histogramme, fig_pie, fig_evolution

# ================= Run server ================== #



if __name__ == '__main__':
    app.run_server(debug=True)
