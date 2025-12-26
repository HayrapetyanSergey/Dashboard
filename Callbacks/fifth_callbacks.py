from dash import Input, Output, State
import plotly.graph_objects as go

def register_bar_chart_callbacks(app, data_loader):

    @app.callback(
        Output("barChart-graph", "figure"),
        Output("barChart-filterStore", "data"),
        Input("barChart-variableDropdown", "value"),
        Input("barChart-dateRange", "start_date"),
        Input("barChart-dateRange", "end_date"),
        State("barChart-filterStore", "data"),
    )
    def update_bar_chart_figure(selected_variable, start_date, end_date, filter_state):

        filter_state = filter_state or {}
        filter_state.update(
            {
                "variable": selected_variable,
                "start_date": start_date,
                "end_date": end_date,
            }
        )

        figure = generate_bar_chart_figure(
            selected_variable, start_date, end_date
        )

        return figure, filter_state

    def generate_bar_chart_figure(variable, start_date, end_date):
        try:
            grouped_df = data_loader.get_bar_chart_data(
                variable, start_date, end_date, top_n=30
            )

            if grouped_df.empty:
                return create_empty_figure(
                    "No Data", f"No data for {variable} or selected date range"
                )

            grouped_df = grouped_df.drop_duplicates(subset=[variable]).sort_values(
                "total_amount", ascending=True
            )

            y_values = grouped_df[variable].astype(str).tolist()
            x_values = grouped_df["loan_count"].tolist()

            fig = go.Figure(
                go.Bar(
                    y=y_values,
                    x=x_values,
                    orientation="h",
                    marker_color="#4CAF50",
                    text=[f"{x:,}" for x in x_values],
                    textposition="outside",
                    hovertemplate="<b>%{y}</b><br>Count: %{x:,}<extra></extra>",
                )
            )

            variable_labels = {
                "purpose": "Purpose",
                "home_ownership": "Home Ownership",
                "emp_length": "Employment Length",
            }

            fig.update_layout(
                title=dict(
                    text=f"Count by {variable_labels.get(variable, variable)}",
                    font=dict(color="white", size=18),
                    x=0.5,
                    xanchor="center",
                ),
                xaxis=dict(
                    gridcolor="#333",
                    tickfont=dict(color="#aaa"),
                    title_font=dict(color="white"),
                ),
                yaxis=dict(
                    tickfont=dict(color="white"),
                    automargin=True,
                ),
                plot_bgcolor="#0a0a0a",
                paper_bgcolor="#0a0a0a",
                height=500,
                margin=dict(l=10, r=80, t=80, b=50),
                showlegend=False,
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
            plot_bgcolor="#0a0a0a",
            paper_bgcolor="#0a0a0a",
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
            plot_bgcolor="#0a0a0a",
            paper_bgcolor="#0a0a0a",
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

