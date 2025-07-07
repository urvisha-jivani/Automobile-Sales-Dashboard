import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Automobile Statistics Dashboard"



# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
# List of years 
year_list = [i for i in range(1980, 2024)]



# Create the layout of the app
app.layout = html.Div([

    #Add title to the dashboard
    html.H1("Automobile Sales Statistics Dashboard",
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': '28px'}),
    
    #Add two dropdown menus
    html.Div([
        # html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value=None,
            placeholder='Select a report type',
            style={'textAlign': 'center', 'width': '80%', 'padding': '3px', 'font-size': '20px', 'margin-bottom': '20px'}
        )
    ], style={'textAlign': 'center'}),

    html.Div([
        dcc.Dropdown(
            id='select-year',
            options=[{'label': str(i), 'value': i} for i in year_list],
            value=None,
            placeholder='Select Year',
            style={'textAlign': 'center', 'width': '80%', 'padding': '3px', 'font-size': '20px'}
        )
    ], style={'textAlign': 'center', 'margin-bottom': '30px'}),
    
    #Add a division for output display
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'center'})
    ])
])

#Creating Callbacks

# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True

#Callback for plotting
@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'),
     Input('select-year', 'value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]

        #Create and display graphs for Recession Report Statistics

        #Plot 1 Automobile sales fluctuate over Recession Period (year wise)
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec,
                           x='Year',
                           y='Automobile_Sales',
                           title="Average Automobile Sales fluctuation over Recession Period")
        )

        #Plot 2 Calculate the average number of vehicles sold by vehicle type       
        average_sales = recession_data.groupby(['Year', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(average_sales,
                          x='Year',
                          y='Automobile_Sales',
                          color='Vehicle_Type',
                          title='Average Automobile Sales by Vehicle Type over Recession Period')
        )

        # Plot 3 Pie chart for total expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec,
                          values='Advertising_Expenditure',
                          names='Vehicle_Type',
                          title='Total Advertising Expenditure Share by Vehicle Type during Recessions')
        )

        # Plot 4 Develop a Bar chart for the effect of unemployment rate on vehicle type and sales
        unemp_data = recession_data.groupby('Vehicle_Type')[['unemployment_rate', 'Automobile_Sales']].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemp_data,
                          x='Vehicle_Type',
                          y='Automobile_Sales',
                          color='unemployment_rate',
                          labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
                          title='Effect of Unemployment Rate on Vehicle Type and Sales')
        )

        return [
            html.Div(className='chart-item', children=[R_chart1, R_chart2], style={'display': 'flex', 'flex': '1', 'gap': '20px'}),
            html.Div(className='chart-item', children=[R_chart3, R_chart4], style={'display': 'flex', 'flex': '1', 'gap': '20px'})
        ]

    #Create and display graphs for Yearly Report Statistics
    elif selected_statistics == 'Yearly Statistics' and input_year:
        yearly_data = data[data['Year'] == input_year]

        # Plot 1 :Yearly Automobile sales using line chart for the whole period.
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yas,
                           x='Year',
                           y='Automobile_Sales',
                           title="Yearly Automobile Sales")
        )

        # Plot 2 :Total Monthly Automobile sales using line chart.
        mon_sales = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(mon_sales,
                           x='Month',
                           y='Automobile_Sales',
                           title=f'Total Monthly Automobile Sales in {input_year}')
        )

        # Plot 3: Plot bar chart for average number of vehicles sold during the given year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(avr_vdata,
                          x='Vehicle_Type',
                          y='Automobile_Sales',
                          color='Vehicle_Type',
                          title=f'Average Vehicles Sold by Vehicle Type in the year {input_year}')
        )

        # Plot 4: Total Advertisement Expenditure for each vehicle using pie chart
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(exp_data,
                          values='Advertising_Expenditure',
                          names='Vehicle_Type',
                          title=f'Total Advertisement Expenditure for each Vehicle Type in the year {input_year}')
        )

        return [
            html.Div(className='chart-item', children=[Y_chart1, Y_chart2], style={'display': 'flex', 'flex': '1', 'gap': '20px'}),
            html.Div(className='chart-item', children=[Y_chart3, Y_chart4], style={'display': 'flex', 'flex': '1', 'gap': '20px'})
        ]

    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)
