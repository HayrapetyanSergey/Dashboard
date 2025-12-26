from dash import dcc, html

def build_sunburst_chart_layout(data_loader):
    """Build sunburst chart layout for risk groups and subgrades"""

    min_date, max_date = data_loader.get_date_range() if data_loader else (None, None)

    return html.Div(
        className="sunburstChart-layout",
        children=[
            # ── Filters ───────────────────────────────
            html.Div(
                className="sunburstChart-filterSection",
                children=[
                    html.Div(
                        className="sunburstChart-filterRow",
                        children=[
                            html.Div(
                                className="sunburstChart-filterItem",
                                children=[
                                    dcc.DatePickerRange(
                                        id="sunburstChart-dateRange",
                                        min_date_allowed=min_date,
                                        max_date_allowed=max_date,
                                        start_date=min_date,
                                        end_date=max_date,
                                        display_format="YYYY-MM-DD",
                                        className="sunburstChart-dateRange",
                                    )
                                ],
                            )
                        ],
                    )
                ],
            ),

            # ── Chart ─────────────────────────────────
            html.Div(
                className="sunburstChart-chartContainer",
                children=[
                    dcc.Graph(
                        id="sunburstChart-graph",
                        className="sunburstChart-graph",
                        config={
                            "displayModeBar": True,
                            "displaylogo": False,
                            "modeBarButtonsToRemove": ["select2d", "lasso2d"],
                            "toImageButtonOptions": {
                                "format": "png",
                                "filename": "risk_sunburst_chart",
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
                id="sunburstChart-filterStore",
                data={
                    "start_date": str(min_date) if min_date else None,
                    "end_date": str(max_date) if max_date else None,
                },
            ),
        ],
    )

