from dash import Input, Output, State
import plotly.graph_objects as go

def register_second_chart_callbacks(app, data_loader):
    """Register callbacks for US map chart"""

    @app.callback(
        Output("secondChart-graph", "figure"),
        Output("secondChart-filterStore", "data"),
        Input("secondChart-dateRange", "start_date"),
        Input("secondChart-dateRange", "end_date"),
        State("secondChart-filterStore", "data"),
    )
    def update_second_chart(start_date, end_date, filter_state):

        filter_state = filter_state or {}
        filter_state.update(
            {
                "start_date": start_date,
                "end_date": end_date,
            }
        )

        figure = generate_us_map_figure(start_date, end_date)

        return figure, filter_state

    def generate_us_map_figure(start_date, end_date):
        try:
            state_df = data_loader.get_state_loan_data(start_date, end_date)

            if state_df.empty:
                return create_empty_figure(
                    "No Data", "No data for selected date range"
                )

            hover_texts = [
                (
                    f"State: {row.state}<br>"
                    f"Total Loans: {row.loan_count:,}<br>"
                    f"Total Amount: ${row.total_loan_amount:,.0f}<br>"
                    f"Bad Loans: {row.bad_loan_count:,}<br>"
                    f"Bad Amount: ${row.bad_loan_amount:,.0f}<br>"
                    f"Bad Loan %: {row.bad_loan_pct:.2f}%<br>"
                    f"Avg Income: ${row.avg_income:,.0f}"
                )
                for _, row in state_df.iterrows()
            ]

            fig = go.Figure(
                go.Choropleth(
                    locations=state_df["state"],
                    z=state_df["total_loan_amount"].astype(float),
                    locationmode="USA-states",
                    colorscale=[
                        [0.0, "#E8F5E9"],
                        [0.2, "#C8E6C9"],
                        [0.4, "#A5D6A7"],
                        [0.6, "#81C784"],
                        [0.8, "#66BB6A"],
                        [1.0, "#1B5E20"],
                    ],
                    marker_line_color="white",
                    marker_line_width=0.5,
                    hovertext=hover_texts,
                    hovertemplate="%{hovertext}<extra></extra>",
                    colorbar=dict(
                        title=dict(text="Loan Amount", font=dict(color="white")),
                        tickfont=dict(color="white"),
                    ),
                )
            )

            fig.update_layout(
                title=dict(
                    text="Loan Portfolio Map",
                    font=dict(color="white", size=20),
                    x=0.5,
                    xanchor="center",
                ),
                geo=dict(
                    scope="usa",
                    projection=dict(type="albers usa"),
                    showland=True,
                    landcolor="#222",
                    bgcolor="rgba(0,0,0,0)",
                ),
                paper_bgcolor="#111",
                plot_bgcolor="#1a1a1a",
                height=500,
                margin=dict(l=0, r=0, t=80, b=0),
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
            paper_bgcolor="#111",
            plot_bgcolor="#1a1a1a",
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
            paper_bgcolor="#111",
            plot_bgcolor="#1a1a1a",
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

