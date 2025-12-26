from dash import Input, Output, State
import plotly.graph_objects as go

def register_sunburst_chart_callbacks(app, data_loader):

    @app.callback(
        Output("sunburstChart-graph", "figure"),
        Output("sunburstChart-filterStore", "data"),
        Input("sunburstChart-dateRange", "start_date"),
        Input("sunburstChart-dateRange", "end_date"),
        State("sunburstChart-filterStore", "data"),
    )
    def update_sunburst_chart(start_date, end_date, filter_state):

        filter_state = filter_state or {}
        filter_state.update(
            {"start_date": start_date, "end_date": end_date}
        )

        fig = generate_sunburst_chart_figure(start_date, end_date)

        return fig, filter_state

    def generate_sunburst_chart_figure(start_date, end_date):
        try:
            sunburst_df = data_loader.get_sunburst_data(start_date, end_date)

            if sunburst_df.empty:
                return create_empty_figure(
                    "No Data", "No data for selected date range"
                )

            grade_colors = {
                "A": "#1E88E5",
                "B": "#43A047",
                "C": "#FDD835",
                "D": "#FB8C00",
                "E": "#E53935",
                "F": "#8E24AA",
                "G": "#546E7A",
            }

            colors = []
            for _, row in sunburst_df.iterrows():
                parent = row["parent"]
                label = row["label"]
                colors.append(
                    grade_colors.get(label if parent == "" else parent, "#1B5E20")
                )

            fig = go.Figure(
                go.Sunburst(
                    ids=sunburst_df["id"],
                    labels=sunburst_df["label"],
                    parents=sunburst_df["parent"],
                    values=sunburst_df["value"],
                    branchvalues="total",
                    marker=dict(
                        colors=colors,
                        line=dict(color="#111", width=1),
                    ),
                    hovertemplate=(
                        "<b>%{label}</b><br>"
                        "Loan Amount: %{value:,.0f}<br>"
                        "<extra></extra>"
                    ),
                    customdata=sunburst_df["loan_count"],
                    maxdepth=2,
                )
            )

            fig.update_layout(
                title=dict(
                    text="Loan Amount by Grade and Subgrade",
                    font=dict(color="white", size=18),
                    x=0.5,
                    xanchor="center",
                ),
                paper_bgcolor="#0a0a0a",
                plot_bgcolor="#0a0a0a",
                margin=dict(l=0, r=0, t=60, b=0),
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
            paper_bgcolor="#0a0a0a",
            plot_bgcolor="#0a0a0a",
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
            paper_bgcolor="#0a0a0a",
            plot_bgcolor="#0a0a0a",
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

