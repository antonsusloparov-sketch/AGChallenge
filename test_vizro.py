import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import vizro
from vizro import Vizro
import vizro.models as vm
from vizro.models.types import capture
import vizro.plotly.express as px

@capture("graph")
def financial_candlestick_chart(data_frame):
    """
    Create a candlestick chart with volume bars for financial data.
    
    Args:
        data_frame: DataFrame with columns: datetime, open, high, low, close, volume
        
    Returns:
        plotly.graph_objects.Figure: The candlestick chart with volume
    """
    # Convert datetime column to proper format
    data_frame['datetime'] = pd.to_datetime(data_frame['datetime'], format='%d.%m.%Y %H:%M')
    
    # Create subplots: one for candlesticks, one for volume
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=('Price (OHLC)', 'Volume'),
        row_width=[0.2, 0.8]
    )
    
    # Add candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=data_frame['datetime'],
            open=data_frame['open'],
            high=data_frame['high'],
            low=data_frame['low'],
            close=data_frame['close'],
            name='OHLC',
            increasing_line_color='#26A69A',
            decreasing_line_color='#EF5350'
        ),
        row=1, col=1
    )
    
    # Add volume bars
    colors = ['#26A69A' if close >= open else '#EF5350' 
              for close, open in zip(data_frame['close'], data_frame['open'])]
    
    fig.add_trace(
        go.Bar(
            x=data_frame['datetime'],
            y=data_frame['volume'],
            name='Volume',
            marker_color=colors,
            opacity=0.7
        ),
        row=2, col=1
    )
    
    # Update layout
    fig.update_layout(
        title='FUT.AFH5_D1 Financial Data - Candlestick Chart with Volume',
        xaxis_rangeslider_visible=False,
        height=600,
        showlegend=False
    )
    
    # Update y-axis labels
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    
    return fig

# Create the Vizro page with the custom chart
model = vm.Dashboard(
    pages=[
        vm.Page(
            title="Financial Data Analysis",
            components=[
                vm.Graph(
                    id='candlestick_chart',
                    type='graph',
                    figure=financial_candlestick_chart(
                    data_frame=pd.read_csv('Data/TQBR.LKOH_M60.txt', sep='\t'))
                )
            ]
        )
    ]
)

# Create and run the Vizro app
app = Vizro()
app.build(model)
app.run()
