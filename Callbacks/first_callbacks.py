from dash import Input, Output, State
import plotly.graph_objects as go

def register_loan_chart_callbacks(app, data_loader):
    """Register loan chart callbacks"""

    @app.callback(
        Output("loanChart-graph", "figure"),
        Output("loanChart-filterStore", "data"),
        Input("loanChart-gradeDropdown", "value"),
        Input("loanChart-dateRange", "start_date"),
        Input("loanChart-dateRange", "end_date"),
        State("loanChart-filterStore", "data"),
    )
    def update_loan_chart(
        selected_grades, start_date, end_date, filter_state
    ):

        if not selected_grades:
            all_grades = data_loader.get_unique_grades()
            selected_grades = [g for g in all_grades if g in ["A", "B", "C", "D", "E"]]

        filter_state = filter_state or {}
        filter_state.update(
            {
                "grades": selected_grades,
                "start_date": start_date,
                "end_date": end_date,
            }
        )

        figure = generate_loan_chart_figure(
            selected_grades, start_date, end_date
        )

        return figure, filter_state

    def generate_loan_chart_figure(selected_grades, start_date, end_date):
        if not selected_grades:
            return create_empty_figure(
                "No grades selected",
                "Please select at least one grade",
            )

        try:
            pivot_df = data_loader.get_monthly_data(
                start_date, end_date, selected_grades
            )

            if pivot_df.empty:
                return create_empty_figure(
                    "No data for selected filters",
                    "Adjust filters or try different dates/grades",
                )

            fig = go.Figure()

            grade_colors = {
                "A": "#1B5E20",
                "B": "#4CAF50",
                "C": "#FBC02D",
                "D": "#FB8C00",
                "E": "#E53935",
                "F": "#8E24AA",
                "G": "#546E7A",
            }

            for grade in selected_grades:
                if grade in pivot_df.columns:
                    fig.add_trace(
                        go.Scatter(
                            x=pivot_df.index,
                            y=pivot_df[grade],
                            mode="lines+markers",
                            name=f"Grade {grade}",
                            line=dict(
                                color=grade_colors.get(grade, "#636efa"),
                                width=2.5,
                            ),
                            marker=dict(size=8),
                            hovertemplate=(
                                f"<b>Grade {grade}</b><br>"
                                "Month: %{x|%Y-%m}<br>"
                                "Loan Amount: %{y:,.0f}<br>"
                                "<extra></extra>"
                            ),
                        )
                    )

            fig.update_layout(
                title=dict(
                    text="Monthly Loan Amount by Grade",
                    font=dict(color="white", size=18),
                    x=0.5,
                    xanchor="center",
                ),
                xaxis=dict(
                    tickformat="%Y-%m",
                    tickfont=dict(color="#aaa"),
                    showgrid=False,
                ),
                yaxis=dict(
                    tickfont=dict(color="white"),
                    gridcolor="gray",
                ),
                hovermode="closest",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                legend=dict(
                    orientation="h",
                    x=0.5,
                    xanchor="center",
                    y=0.93,
                    font=dict(color="white"),
                    bgcolor="rgba(0,0,0,0)",
                ),
                height=500,
            )

            return fig

        except Exception as error:
            return create_error_figure(str(error))

    def create_empty_figure(title, message):
        fig = go.Figure()
        fig.update_layout(
            title=dict(text=title, font=dict(color="white")),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            annotations=[
                dict(
                    text=message,
                    x=0.5,
                    y=0.5,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(color="#aaa", size=14),
                )
            ],
            height=500,
        )
        return fig

    def create_error_figure(error_message):
        fig = go.Figure()
        fig.update_layout(
            title=dict(text="Error", font=dict(color="white")),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            annotations=[
                dict(
                    text=error_message,
                    x=0.5,
                    y=0.5,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(color="#ff6b6b", size=12),
                )
            ],
            height=500,
        )
        return fig

