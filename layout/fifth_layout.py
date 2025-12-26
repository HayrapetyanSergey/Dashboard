from dash import dcc, html

def build_bar_chart_layout(data_loader):
    """Build horizontal bar chart layout for categorical analysis"""

    start_date, end_date = data_loader.get_date_range() if data_loader else (None, None)

    bar_variable_options = [
        {"label": "Purpose", "value": "purpose"},
        {"label": "Home Ownership", "value": "home_ownership"},
        {"label": "Employment Length", "value": "emp_length"},
    ]

    return html.Div(
        className="barChart-layout",
        children=[
            html.Div(
                className="barChart-filterSection",
                children=[
                    html.Div(
                        className="barChart-filterRow",
                        children=[
                            html.Div(
                                className="barChart-filterItem",
                                children=[
                                    dcc.Dropdown(
                                        id="barChart-variableDropdown",
                                        options=bar_variable_options,
                                        value="purpose",
                                        clearable=False,
                                        className="barChart-variableDropdown",
                                    )
                                ],
                            ),
                            html.Div(
                                className="barChart-filterItem barChart-dateFilterItem",
                                children=[
                                    dcc.DatePickerRange(
                                        id="barChart-dateRange",
                                        min_date_allowed=start_date,
                                        max_date_allowed=end_date,
                                        start_date=start_date,
                                        end_date=end_date,
                                        display_format="YYYY-MM-DD",
                                        className="barChart-dateRange",
                                    )
                                ],
                            ),
                        ],
                    )
                ],
            ),
            html.Div(
                className="barChart-chartContainer",
                children=[
                    dcc.Graph(
                        id="barChart-graph",
                        className="barChart-graph",
                        config={
                            "displayModeBar": True,
                            "displaylogo": False,
                            "modeBarButtonsToRemove": ["select2d", "lasso2d"],
                            "toImageButtonOptions": {
                                "format": "png",
                                "filename": "bar_chart_analysis",
                                "height": 500,
                                "width": 800,
                                "scale": 2,
                            },
                        },
                    )
                ],
            ),
            dcc.Store(
                id="barChart-filterStore",
                data={
                    "variable": "purpose",
                    "start_date": str(start_date) if start_date else None,
                    "end_date": str(end_date) if end_date else None,
                },
            ),
        ],
    )

