import dash_bootstrap_components as dbc
from dash import dcc, html
import dash_daq as daq

def build_risk_subgrade_layout(data_loader):
    """Build layout for risk subgrade analysis"""

    unique_grades = data_loader.get_unique_grades() if data_loader else []
    min_date, max_date = data_loader.get_date_range() if data_loader else (None, None)

    return html.Div(
        className="riskChart-layout",
        children=[
            # ── Controls ─────────────────────────────
            html.Div(
                className="riskChart-controlsRow",
                children=[
                    html.Div(
                        className="riskChart-controlGroup",
                        children=[
                            dcc.DatePickerRange(
                                id="riskChart-dateRange",
                                min_date_allowed=min_date,
                                max_date_allowed=max_date,
                                start_date=min_date,
                                end_date=max_date,
                                display_format="YYYY-MM-DD",
                                className="riskChart-datePicker",
                            )
                        ],
                    ),
                    html.Div(
                        className="riskChart-controlGroup riskChart-toggleGroup",
                        children=[
                            daq.BooleanSwitch(
                                id="riskChart-groupToggle",
                                on=False,
                                label="Subgrade Mode",
                                labelPosition="right",
                                color="#1B5E20",
                                className="riskChart-toggle",
                            )
                        ],
                    ),
                    html.Div(
                        className="riskChart-controlGroup",
                        children=[
                            dcc.Dropdown(
                                id="riskChart-gradeDropdown",
                                options=[
                                    {"label": g, "value": g}
                                    for g in unique_grades
                                ],
                                placeholder="All grades",
                                className="riskChart-gradeDropdown",
                            )
                        ],
                    ),
                ],
            ),

            # ── Chart ────────────────────────────────
            html.Div(
                className="riskChart-graphContainer",
                children=[
                    dcc.Graph(
                        id="riskChart-graph",
                        className="riskChart-graph",
                        config={
                            "displayModeBar": True,
                            "displaylogo": False,
                            "modeBarButtonsToRemove": ["select2d", "lasso2d"],
                            "toImageButtonOptions": {
                                "format": "png",
                                "filename": "risk_subgrade_chart",
                                "height": 500,
                                "width": 800,
                                "scale": 2,
                            },
                        },
                    ),
                    dcc.Store(id="riskChart-filterStore", data={}),
                    dcc.Store(id="riskChart-summaryStore", data={}),
                ],
            ),
        ],
    )

