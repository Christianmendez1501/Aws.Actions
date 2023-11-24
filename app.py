'''
import json
import boto3
import dash
from dash import dcc, html, dash_table
import random
import datetime

# Creamos una aplicación Dash
app = dash.Dash(__name__)

# Configuramos la conexión a la tabla de DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='eu-west-3')  # Coloca la región correspondiente
tabla_usuarios = dynamodb.Table('formulario')  # Coloca el nombre que hayas puesto a la tabla

# Función para obtener los datos de la tabla de DynamoDB
def obtener_datos_dynamodb():
    response = tabla_usuarios.scan()
    items = response['Items']
    return items

# Definimos el estilo CSS para la página
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Definimos el diseño general de la aplicación
app.layout = html.Div(style={'backgroundColor': 'black', 'padding': '20px', 'text-align': 'center'}, children=[
    html.Div([
        html.H1('Cloud App', id='title', style={'color': 'white', 'animation': 'bounce 2s infinite'}),
    ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'margin-bottom': '20px'}),

    # Menú de navegación
    html.Div([
        dcc.Link(html.Button('Formulario de Usuarios', id='btn-formulario', n_clicks=0,
                             style={'background-color': 'white', 'color': 'black', 'border': 'none', 'margin': '10px', 'box-shadow': '2px 2px 5px 0px #000000', 'animation': 'falling 2s infinite'}),
                 href='/formulario'),
        dcc.Link(html.Button('Tabla de Usuarios', id='btn-tabla-usuarios', n_clicks=0,
                             style={'background-color': 'white', 'color': 'black', 'border': 'none', 'margin': '10px', 'box-shadow': '2px 2px 5px 0px #000000', 'animation': 'falling 2s infinite'}),
                 href='/tabla_usuarios'),
    ], style={'display': 'flex', 'justify-content': 'center'}),

    # Aquí se mostrará el contenido
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', style={'text-align': 'center'}),
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
            html.H1('Formulario de Usuarios', style={'color': 'white'}),
            dcc.Input(id='nombre', type='text', placeholder='Nombre', value='', style={'margin-bottom': '10px'}),
            dcc.Input(id='email', type='email', placeholder='Email', value='', style={'margin-bottom': '10px'}),
            html.Button('Enviar', id='submit-button', n_clicks=0,
                        style={'background-color': 'white', 'color': 'black', 'border': 'none', 'box-shadow': '2px 2px 5px 0px #000000'}),
            html.Div(id='output-container-button', children='', style={'margin-top': '10px', 'color': 'white'})
        ], style={'background-color': 'black'})
    elif pathname == '/tabla_usuarios':
        # Si el usuario navega a la tabla de usuarios, muestra el contenido de la tabla
        data = obtener_datos_dynamodb()
        return html.Div([
            html.H1('Usuarios registrados', style={'color': 'white'}),
            dash_table.DataTable(
                columns=[{'name': key, 'id': key} for key in data[0].keys()],
                data=data,
                style_table={'overflowX': 'auto', 'border': '1px solid white', 'backgroundColor': 'black'},
                style_header={'backgroundColor': 'white', 'color': 'black', 'fontWeight': 'bold'},
                style_cell={'textAlign': 'left', 'border': '1px solid white'},
                style_data={'border': '1px solid white'},
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
'''

from flask import Flask, render_template, request
import boto3
import random
import datetime

app = Flask(__name__)

# Configura la conexión a la tabla de DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='eu-west-3')  # Coloca la región correspondiente
tabla_usuarios = dynamodb.Table('formulario')  # Coloca el nombre que hayas puesto a la tabla

# Función para obtener los datos de la tabla de DynamoDB
def obtener_datos_dynamodb():
    response = tabla_usuarios.scan()
    items = response['Items']
    return items

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para el formulario de usuarios
@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        # Si se envía el formulario, obtén los datos y guárdalos en DynamoDB
        nombre = request.form['nombre']
        email = request.form['email']
        usuario = {
            'ID': random.randint(100000, 999999),
            'Nombre': nombre,
            'Correo electrónico': email,
            'Fecha de registro': datetime.date.today().strftime('%Y-%m-%d')
        }
        tabla_usuarios.put_item(Item=usuario)
        return f'Se ha enviado el formulario: {nombre}, {email}'

    return render_template('formulario.html')

# Ruta para la tabla de usuarios
@app.route('/tabla_usuarios')
def mostrar_tabla_usuarios():
    data = obtener_datos_dynamodb()
    return render_template('tabla_usuarios.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)





