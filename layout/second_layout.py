from dash import dcc, html

def build_second_chart_layout(data_loader):
    """Build US map chart layout for state distribution"""

    min_date, max_date = data_loader.get_date_range() if data_loader else (None, None)

    return html.Div(
        className="secondChart-layout",
        children=[
            # ── Filters ───────────────────────────────
            html.Div(
                className="secondChart-filterSection",
                children=[
                    html.Div(
                        className="secondChart-filterRow",
                        children=[
                            html.Div(
                                className="secondChart-filterItem",
                                children=[
                                    dcc.DatePickerRange(
                                        id="secondChart-dateRange",
                                        min_date_allowed=min_date,
                                        max_date_allowed=max_date,
                                        start_date=min_date,
                                        end_date=max_date,
                                        display_format="YYYY-MM-DD",
                                        className="secondChart-dateRange",
                                    )
                                ],
                            )
                        ],
                    )
                ],
            ),

            # ── Chart ─────────────────────────────────
            html.Div(
                className="secondChart-chartContainer",
                children=[
                    dcc.Graph(
                        id="secondChart-graph",
                        className="secondChart-graph",
                        config={
                            "displayModeBar": True,
                            "displaylogo": False,
                            "modeBarButtonsToRemove": ["select2d", "lasso2d"],
                            "toImageButtonOptions": {
                                "format": "png",
                                "filename": "state_distribution_map",
                                "height": 500,
                                "width": 800,
                                "scale": 2,
                            },
                        },
                    )
                ],
            ),

            # ── Store ─────────────────────────────────
            dcc.Store(
                id="secondChart-filterStore",
                data={
                    "start_date": str(min_date) if min_date else None,
                    "end_date": str(max_date) if max_date else None,
                },
            ),
        ],
    )

