from dash import dcc, html
from layout.first_layout import build_loan_chart_layout
from layout.second_layout import build_second_chart_layout
from layout.third_layout import build_risk_subgrade_layout
from layout.fourth_layout import build_sunburst_chart_layout  
from layout.fifth_layout import build_bar_chart_layout  

def create_dashboard_layout(data_loader, extra_sections=None):
    
    risk_subgrade_section = build_risk_subgrade_layout(data_loader)
    sunburst_section = build_sunburst_chart_layout(data_loader) 
    bar_chart_section = build_bar_chart_layout(data_loader)  
    
    layout_children = [
        html.Div(className="dashboard-header", children=[
            html.H1("Loan Portfolio Dashboard", className="dashboard-title"),
        ]),
        
        html.Div(className="charts-grid", children=[
            html.Div(className="chart-card", children=[
                build_loan_chart_layout(data_loader) 
            ]),
            
            html.Div(className="chart-card", children=[
                build_second_chart_layout(data_loader) 
            ]),
        ]),
        
        html.Div(className="extra-section-row", children=[
            html.Div(className="chart-card full-width", children=[
                risk_subgrade_section 
            ])
        ]),
        
        html.Div(className="charts-grid-last", children=[
            html.Div(className="chart-card", children=[
                sunburst_section  
            ]),
            
            html.Div(className="chart-card", children=[
                bar_chart_section 
            ]),
        ]),
        
        dcc.Store(id='app-state', data={}),
        dcc.Interval(id='update-interval', interval=30000, n_intervals=0)
    ]
    
    return html.Div(className="dashboard-layout", children=layout_children)
