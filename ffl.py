import pandas as pd #(version 0.24.2)
import dash         #(version 1.0.0)
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import dash_extensions as de 
import plotly       #(version 4.4.1)
import plotly.express as px
import plotly.io as pio
#pio.templates.default = "plotly"

BS = "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
app = dash.Dash(__name__,external_stylesheets=[BS])
server = app.server

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
df=pd.read_excel("ffl_data.xlsx", engine='openpyxl', sheet_name="Sheet_all").reset_index()
df.groupby(['Country','Year','Budget'],as_index=False).sum().reset_index()
app.layout = html.Div([
html.Div([
     dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="20px")),
                    dbc.Col(dbc.NavbarBrand("Dashboard - Jatin Mahour", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
        )
    ],
    color="#fbfdfb",
    dark=False,
),
            dbc.Row(
                [
                    dbc.Col(html.Img(src=app.get_asset_url('logo.png'), height="150px",width="200px"),style={'padding':20},width=2.5),
                    dbc.Col(html.H5("Fondation Follereau Luxembourg (FFL), a Luxembourg-based NGO is committed to the prevention and promotion of the quality of life of the most vulnerable African communities. Since 1966, the foundation has evolved with the times by developing its activities beyond its initial fight against social exclusion in the leprosy communities. The foundation supports the 17 Sustainable Development Goals (SDG). ",style={"font-family":"Times New Roman",'color':'#f4f424','marginTop': 20} ,className="ml-2"),style={'padding':20}),
                ]),
             
            
    ],style={'backgroundColor':'#3f92ad'}
), 
html.Div([
     dbc.Row([
            dbc.Col([
        dbc.Label('Country',style={'font-weight': 'bold','marginLeft':90,"font-family":"Times New Roman"}),
    dcc.Dropdown(
                id="country",
                options=[{'label': s, 'value': s} for s in sorted(df.Country.unique())]
                ,value='Benin',
            multi=False,
            clearable=False,
            style={"width": "80%",'padding':5,"font-family":"Times New Roman","font-size":"90%"}
                )]),
    dbc.Col([
        dbc.Label('Year',style={'font-weight': 'bold','marginLeft':100,"font-family":"Times New Roman"}),
        dcc.Dropdown(id="year",
                options=[{'label': s, 'value': s} for s in sorted(df.Year.unique())]
                ,value=[2018],
            multi=True,
            clearable=False,
            style={"width": "80%",'padding':5,"font-family":"Times New Roman","font-size":"90%"})
    ]),  
           
    dbc.Col(
    html.Div(id="content")
    ,style={'padding':10})
 ],style={'padding':20})
],style={'backgroundColor':'#c4d6dc'}),
#------------------------------------------------------------------------------------------------------------
html.Div([
 dbc.Row([
 dbc.Col(dcc.Graph(id="graph2")),
 dbc.Col(dcc.Graph(id="graph3"))
 ])
]),
#------------------------------------------------------------------------------------------------------------
html.Div([ 
     dbc.Row([
         dbc.Card([
            dbc.Col([
            dbc.Label('Projects',style={'font-weight': 'bold','padding':10,"font-family":"Times New Roman"}),
            dcc.Dropdown(
                id="project",
                options=[],
                value=['Project title:CIPSA-EH Socio-educative center'],
                multi=True,
                clearable=False,
                style={"width": "80%",'padding':5,"font-family":"Times New Roman","font-size":"90%",'padding':10}),
            html.Div(dcc.Graph(id="graph"))
                    ])
         ]),
      dbc.Col([
     dbc.Card([               
            html.Div([
            html.Section(id="slideshow", children=[
            html.Div(id="slideshow-container", children=[
            html.Div(id="image"),
            dcc.Interval(id='interval', interval=3000)
                     ])
                     ])
                     ])
     ]),
            dbc.Label('Project Achievements',style={'font-weight': 'bold',"font-family":"Times New Roman",'padding':10}),
            html.Div(id="content2"),
            ])
            
            ],style={'padding':10})
],style={'padding':10,'backgroundColor':'#c4d6dc'})
])   

@app.callback(Output('image', 'children'),
              [Input('interval', 'n_intervals')])
def display_image(n):
    if n == None or n % 6 == 1:
        img = html.Img(src=app.get_asset_url('1.png'), height="300px",width="560px")
    elif n % 6 == 2:
        img = html.Img(src=app.get_asset_url('2.png'), height="300px",width="560px")
    elif n % 6 == 3:
        img = html.Img(src=app.get_asset_url('3.png'), height="300px",width="560px")
    elif n % 6 == 4:
        img = html.Img(src=app.get_asset_url('4.png'), height="300px",width="560px") 
    elif n % 6 == 5:
        img = html.Img(src=app.get_asset_url('5.png'), height="300px",width="560px")
    elif n % 6 == 6:
        img = html.Img(src=app.get_asset_url('6.png'), height="300px",width="560px")
    elif n % 6 == 0:
        img = html.Img(src=app.get_asset_url('5.png'), height="300px",width="560px")
    else:
        img = "None"
    return img
#--------------------------------------------------------------------
@app.callback(Output('content2', 'children'),
               Input("country", "value"),             
               Input("project", "value"),             
               Input("year", "value"))                
def render_content(path,path2,path3):  
    dff = df[(df.Country==path) & (df.Project_title.isin(path2)) & (df.Year.isin(path3))]

    return html.Div([
             dbc.Row(
                 (dbc.Card(dff.Results.unique(),style={'padding':5,'backgroundColor':'#3f92ad'})
                 )) 
       ],style={'padding':10}) 
#--------------------------------------------------------------------     
@app.callback(Output('content', 'children'),
              Input('country', 'value'),
              Input('year', 'value'))

def render_content(content,year):
    dff = df[(df.Country==content) & (df.Year.isin(year))]

    return html.Div([
             dbc.Row([
                 dbc.Col(dbc.Card(dff.country_budget.unique(),style={'padding':10,'backgroundColor':'#3f92ad'}),style={'padding':10}),
                 dbc.Col(dbc.Card(dff.country_budget_per.unique(),style={'padding':10,'backgroundColor':'#3f92ad'}),style={'padding':10})
    ]) 
    ])             
#-------------------------------------------------------------------------                                           
                                 
@app.callback(
    Output('project', 'options'),
    Input('country', 'value')
)
def set_projects_options(chosen_country):
    dff=df[df.Country==chosen_country]
    return [{'label': c, 'value': c} for c in sorted(dff.Project_title.unique())
    ]
@app.callback(
    Output('project', 'value'),
    Input('project', 'options')
)   
def set_projects_value(available_options):
    return [x[0]['value'] for x in available_options
            ] 

@app.callback(
   Output("graph", "figure"),
    Input("country", "value"),
    Input("project", "value"),
    Input("year", "value"))

def update_graph(path,path2,path3):

   dff = df[(df.Country==path) & (df.Project_title.isin(path2)) & (df.Year.isin(path3))]
   fig = px.treemap(dff,width=650,height=400 , path=['Local partner', 'Project_title','Axis of intervention','Direct beneficiaries','Indirect beneficiaries','Region','Voted project budget €','Project share % out of all budget','Project financing (as per the 2016-2020 cooperation agreement)'])
   fig.update_layout(treemapcolorway = ["#acd5d9"])
   fig.update_traces(
   hovertemplate=None,
   hoverinfo='skip'
)

   return(fig) 

@app.callback(
   Output("graph2", "figure"),
    Input("country", "value"))
def render_content(content):
    dff = df[(df.Country==content)]  
    fig = px.bar(dff, x="Year", y="Budget",height=400, log_y=True,width=600,hover_data=["Year","Budget","Country"])
    fig.update_xaxes(type='category')
    fig.update_layout(showlegend=False)
    fig.update_layout(
    title={
        'text': "Country's budget for the year 2018, 2019 & 2020.",
        'y':0.94,
        'x':0.5,
     #   'font-weight': 'bold',
        'xanchor': 'center',
        'yanchor': 'top'})
    return fig

@app.callback(
   Output("graph3", "figure"),
    Input("year", "value"))
def render_content(content):
    dff = df[(df.Year.isin(content))]  
    fig = px.bar(dff, y="Country", x="Budget",height=400,color='Country',log_x=True,width=600,hover_data=["Budget","budget%","Year"])        
    fig.update_layout(showlegend=False)
    fig.update_layout(
    title={
        'text': "Yearly budget for each country.",
        'y':0.94,
        'x':0.55,
        'xanchor': 'center',
        'yanchor': 'top'})
    return fig
if __name__ == '__main__':
    app.run_server(debug=True)