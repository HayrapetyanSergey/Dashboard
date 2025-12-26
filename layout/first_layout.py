from dash import dcc, html

def build_loan_chart_layout(data_loader):
    """Build loan chart layout with grade and date filters"""

    min_date, max_date = data_loader.get_date_range() if data_loader else (None, None)
    all_grades = data_loader.get_unique_grades() if data_loader else []
    default_grades = [g for g in all_grades if g in ["A", "B", "C", "D", "E"]]

    return html.Div(
        className="loanChart-layout",
        children=[
            # ── Filters ───────────────────────────────
            html.Div(
                className="loanChart-filterSection",
                children=[
                    html.Div(
                        className="loanChart-filterRow",
                        children=[
                            html.Div(
                                className="loanChart-filterItem",
                                children=[
                                    dcc.Dropdown(
                                        id="loanChart-gradeDropdown",
                                        options=[{"label": g, "value": g} for g in all_grades],
                                        value=default_grades,
                                        multi=True,
                                        placeholder="Select grades...",
                                        className="loanChart-gradeDropdown",
                                    )
                                ],
                            ),
                            html.Div(
                                className="loanChart-filterItem",
                                children=[
                                    dcc.DatePickerRange(
                                        id="loanChart-dateRange",
                                        min_date_allowed=min_date,
                                        max_date_allowed=max_date,
                                        start_date=min_date,
                                        end_date=max_date,
                                        display_format="YYYY-MM-DD",
                                        className="loanChart-dateRange",
                                    )
                                ],
                            ),
                        ],
                    )
                ],
            ),

            # ── Chart ─────────────────────────────────
            html.Div(
                className="loanChart-chartContainer",
                children=[
                    dcc.Graph(
                        id="loanChart-graph",
                        className="loanChart-graph",
                        config={
                            "displayModeBar": True,
                            "displaylogo": False,
                            "modeBarButtonsToRemove": ["select2d", "lasso2d"],
                            "toImageButtonOptions": {
                                "format": "png",
                                "filename": "loan_chart",
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
                id="loanChart-filterStore",
                data={
                    "grades": default_grades,
                    "start_date": str(min_date) if min_date else None,
                    "end_date": str(max_date) if max_date else None,
                },
            ),
        ],
    )

