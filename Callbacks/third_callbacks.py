from dash import Input, Output, State, no_update, html
import plotly.graph_objects as go

def register_risk_subgrade_callbacks(app, data_loader):
    """Register callbacks for risk subgrade analysis"""

    @app.callback(
        Output("riskChart-summaryStore", "data"),
        Input("riskChart-dateRange", "start_date"),
        Input("riskChart-dateRange", "end_date"),
        Input("riskChart-gradeDropdown", "value"),
    )
    def update_summary_data(start_date, end_date, selected_grade):
        try:
            df = data_loader.get_filtered_data(start_date, end_date)
            if df.empty:
                return {}

            if "grade" not in df.columns and "sub_grade" in df.columns:
                df["grade"] = df["sub_grade"].str[0]

            summary = (
                df.groupby("grade")["loan_amount"]
                .sum()
                .sort_index()
                .to_dict()
            )

            return summary

        except Exception:
            return {}

    @app.callback(
        Output("riskChart-gradeDropdown", "disabled"),
        Input("riskChart-groupToggle", "on"),
    )
    def toggle_grade_dropdown(toggle_on):
        return not toggle_on

    @app.callback(
        Output("riskChart-gradeDropdown", "value"),
        Input("riskChart-groupToggle", "on"),
    )
    def clear_grade_dropdown(toggle_on):
        return None if not toggle_on else no_update

    @app.callback(
        Output("riskChart-graph", "figure"),
        Output("riskChart-filterStore", "data"),
        Input("riskChart-dateRange", "start_date"),
        Input("riskChart-dateRange", "end_date"),
        Input("riskChart-groupToggle", "on"),
        Input("riskChart-gradeDropdown", "value"),
        State("riskChart-filterStore", "data"),
    )
    def update_risk_chart(
        start_date, end_date, is_subgrade_mode, selected_grade, filter_state
    ):
        filter_state = filter_state or {}
        filter_state.update(
            {
                "start_date": start_date,
                "end_date": end_date,
                "subgrade_mode": is_subgrade_mode,
                "grade": selected_grade if is_subgrade_mode else None,
            }
        )

        fig = generate_risk_chart_figure(
            start_date, end_date, is_subgrade_mode, selected_grade
        )

        return fig, filter_state

    def generate_risk_chart_figure(start_date, end_date, subgrade_mode, grade):
        try:
            df = data_loader.get_filtered_data(start_date, end_date)

            if df.empty:
                return create_empty_figure("No data for selected range")

            df["grade"] = df["sub_grade"].str[0]

            if subgrade_mode and grade:
                df = df[df["grade"] == grade]
                group_col = "sub_grade"
                title = f"Loan Amount by Subgrade ({grade})"
            else:
                group_col = "grade"
                title = "Loan Amount by Grade"

            grouped = df.groupby(group_col)["loan_amount"].sum().reset_index()

            fig = go.Figure(
                go.Bar(
                    x=grouped[group_col],
                    y=grouped["loan_amount"],
                    marker_color="#388E3C",
                    text=[f"{v:,.0f}" for v in grouped["loan_amount"]],
                    textposition="outside",
                )
            )

            fig.update_layout(
                title=dict(text=title, font=dict(color="white")),
                plot_bgcolor="#222",
                paper_bgcolor="#222",
                xaxis=dict(tickfont=dict(color="#aaa")),
                yaxis=dict(tickfont=dict(color="white")),
                height=400,
            )

            return fig

        except Exception as error:
            return create_error_figure(str(error))

    def create_empty_figure(message):
        fig = go.Figure()
        fig.update_layout(
            title=dict(text=message, font=dict(color="white")),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            plot_bgcolor="#222",
            paper_bgcolor="#222",
            height=400,
        )
        return fig

    def create_error_figure(error_message):
        fig = go.Figure()
        fig.update_layout(
            title=dict(text="Error", font=dict(color="white")),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            plot_bgcolor="#222",
            paper_bgcolor="#222",
            annotations=[
                dict(
                    text=error_message,
                    x=0.5,
                    y=0.5,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(color="#ff6b6b"),
                )
            ],
            height=400,
        )
        return fig

