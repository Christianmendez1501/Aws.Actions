import json
import boto3
import dash
from dash import dcc, html, dash_table
import random
import datetime

# Creamos una aplicación Dash
app = dash.Dash(__name__)

# Configuramos la conexión a la tabla de DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='eu-west-3') #colocar la region que corresponde
tabla_usuarios = dynamodb.Table('formulario') #colocar nopmbre que le hayas puesto a la tabla

# Función para obtener los datos de la tabla de DynamoDB
def obtener_datos_dynamodb():
    response = tabla_usuarios.scan()
    items = response['Items']
    return items

# Definimos el estilo CSS para la página
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Definimos el diseño general de la aplicación
app.layout = html.Div(style={'backgroundColor': 'white', 'padding': '20px', 'text-align': 'center'}, children=[
    html.Div([
        html.H1('Cloud App', style={'color': 'black'}),
    ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'margin-bottom': '20px'}),

    # Menú de navegación
    html.Div([
        dcc.Link(html.Button('Formulario de Usuarios', id='btn-formulario', n_clicks=0,
                             style={'background-color': 'black', 'color': 'white', 'border': 'none', 'margin': '10px', 'box-shadow': '2px 2px 5px 0px #000000'}),
                 href='/formulario'),
        dcc.Link(html.Button('Tabla de Usuarios', id='btn-tabla-usuarios', n_clicks=0,
                             style={'background-color': 'black', 'color': 'white', 'border': 'none', 'margin': '10px', 'box-shadow': '2px 2px 5px 0px #000000'}),
                 href='/tabla_usuarios'),
    ], style={'display': 'flex', 'justify-content': 'center'}),

    # Aquí se mostrará el contenido
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])

# Callback para cargar el contenido de las páginas
@app.callback(
    dash.dependencies.Output('page-content', 'children'),
    [dash.Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/formulario':
        # Si el usuario navega al formulario, muestra el contenido del formulario
        return html.Div([
            html.H1('Formulario de Usuarios', style={'color': 'black'}),
            dcc.Input(id='nombre', type='text', placeholder='Nombre', value='', style={'margin-bottom': '10px'}),
            dcc.Input(id='email', type='email', placeholder='Email', value='', style={'margin-bottom': '10px'}),
            html.Button('Enviar', id='submit-button', n_clicks=0,
                        style={'background-color': 'black', 'color': 'white', 'border': 'none', 'box-shadow': '2px 2px 5px 0px #000000'}),
            html.Div(id='output-container-button', children='', style={'margin-top': '10px', 'color': 'black'})
        ])
    elif pathname == '/tabla_usuarios':
        # Si el usuario navega a la tabla de usuarios, muestra el contenido de la tabla
        data = obtener_datos_dynamodb()
        return html.Div([
            html.H1('Usuarios registrados', style={'color': 'black'}),
            dash_table.DataTable(
                columns=[{'name': key, 'id': key} for key in data[0].keys()],
                data=data,
                style_table={'overflowX': 'auto', 'border': '1px solid black', 'backgroundColor': 'white'},
                style_header={'backgroundColor': 'black', 'color': 'white', 'fontWeight': 'bold'},
                style_cell={'textAlign': 'left', 'border': '1px solid black'},
                style_data={'border': '1px solid black'},
                style_as_list_view=True
            )
        ])
# Ruta para manejar la subida de datos del formulario
@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.Input('submit-button', 'n_clicks'),
     dash.State('nombre', 'value'),
     dash.State('email', 'value')]
)
def submit_form(n_clicks, nombre, email):
    # Obtenemos los datos del formulario
    usuario = {
        'ID': random.randint(100000, 999999),
        'Nombre': nombre,
        'Correo electrónico': email,
        'Fecha de registro': datetime.date.today().strftime('%Y-%m-%d')
    }
    tabla_usuarios.put_item(Item=usuario)
    return f'Se ha enviado el formulario: {nombre}, {email}'

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True)