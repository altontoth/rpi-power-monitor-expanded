import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from datetime import datetime


# This package is imported by power-monitor.py
# plot_data will be called when power-monitor.py is started in debug mode. See the documentation for more information about debug mode.

webroot = '/var/www/html'


def plot_data(samples, title, *args, **kwargs):
    # Plots the raw sample data from the individual CT channels and the AC voltage channel.
    
    # Check to see if the sample rate was included in the parameters passed in.
    if kwargs:
        if 'sample_rate' in kwargs.keys():
            sample_rate = kwargs['sample_rate']
    
    else:
        sample_rate = None

    if args:    # Make plot for a single CT channel
        ct_selection = args[0]
        ct = samples['ct']
        voltage = samples['original_v']
        x = [x for x in range(1, len(ct))]
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=x, y=ct, mode='lines', name=ct_selection.upper()), secondary_y=False)
        fig.add_trace(go.Scatter(x=x, y=voltage, mode='lines', name='Original Voltage Wave'), secondary_y=True)

        # Get the phase shifted voltage wave
        fig.add_trace(go.Scatter(x=x, y=samples['new_v'], mode='lines', name=f'Phase corrected voltage wave ({ct_selection})'), secondary_y=True)    

    else:       # Make plot for all CT channels
        ct0 = samples['ct0']
        ct1 = samples['ct1']
        ct2 = samples['ct2']
        ct3 = samples['ct3']
        ct4 = samples['ct4']
        ct5 = samples['ct5']
        ct6 = samples['ct6']
        ct7 = samples['ct7']
        ct8 = samples['ct8']
        ct9 = samples['ct9']
        ct10 = samples['ct10']
        ct11 = samples['ct11']
        ct12 = samples['ct12']
        ct13 = samples['ct13']
        voltage = samples['voltage']
        x = [x for x in range(1, len(ct0))]

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=x, y=ct0, mode='lines', name='CT0'), secondary_y=False)
        fig.add_trace(go.Scatter(x=x, y=ct1, mode='lines', name='CT1'), secondary_y=False)
        fig.add_trace(go.Scatter(x=x, y=ct2, mode='lines', name='CT2'), secondary_y=False)
        fig.add_trace(go.Scatter(x=x, y=ct3, mode='lines', name='CT3'), secondary_y=False)
        fig.add_trace(go.Scatter(x=x, y=ct4, mode='lines', name='CT4'), secondary_y=False)
        fig.add_trace(go.Scatter(x=x, y=ct5, mode='lines', name='CT5'), secondary_y=False)
        fig.add_trace(go.Scatter(x=x, y=ct5, mode='lines', name='CT6'), secondary_y=False)
        fig.add_trace(go.Scatter(x=x, y=ct5, mode='lines', name='CT7'), secondary_y=False)
        fig.add_trace(go.Scatter(x=x, y=ct5, mode='lines', name='CT8'), secondary_y=False)
        fig.add_trace(go.Scatter(x=x, y=ct5, mode='lines', name='CT9'), secondary_y=False)
        fig.add_trace(go.Scatter(x=x, y=ct5, mode='lines', name='CT10'), secondary_y=False)
        fig.add_trace(go.Scatter(x=x, y=ct5, mode='lines', name='CT11'), secondary_y=False)
        fig.add_trace(go.Scatter(x=x, y=ct5, mode='lines', name='CT12'), secondary_y=False)
        fig.add_trace(go.Scatter(x=x, y=ct5, mode='lines', name='CT13'), secondary_y=False)
        fig.add_trace(go.Scatter(x=x, y=voltage, mode='lines', name='AC Voltage'), secondary_y=True)

        if 'vWave_ct0' in samples.keys():
            fig.add_trace(go.Scatter(x=x, y=samples['vWave_ct0'], mode='lines', name='New V wave (ct0)'), secondary_y=True)
            fig.add_trace(go.Scatter(x=x, y=samples['vWave_ct1'], mode='lines', name='New V wave (ct1)'), secondary_y=True)
            fig.add_trace(go.Scatter(x=x, y=samples['vWave_ct2'], mode='lines', name='New V wave (ct2)'), secondary_y=True)
            fig.add_trace(go.Scatter(x=x, y=samples['vWave_ct3'], mode='lines', name='New V wave (ct3)'), secondary_y=True)
            fig.add_trace(go.Scatter(x=x, y=samples['vWave_ct4'], mode='lines', name='New V wave (ct4)'), secondary_y=True)
            fig.add_trace(go.Scatter(x=x, y=samples['vWave_ct5'], mode='lines', name='New V wave (ct5)'), secondary_y=True)
            fig.add_trace(go.Scatter(x=x, y=samples['vWave_ct5'], mode='lines', name='New V wave (ct6)'), secondary_y=True)
            fig.add_trace(go.Scatter(x=x, y=samples['vWave_ct5'], mode='lines', name='New V wave (ct7)'), secondary_y=True)
            fig.add_trace(go.Scatter(x=x, y=samples['vWave_ct5'], mode='lines', name='New V wave (ct8)'), secondary_y=True)
            fig.add_trace(go.Scatter(x=x, y=samples['vWave_ct5'], mode='lines', name='New V wave (ct9)'), secondary_y=True)
            fig.add_trace(go.Scatter(x=x, y=samples['vWave_ct5'], mode='lines', name='New V wave (ct10)'), secondary_y=True)
            fig.add_trace(go.Scatter(x=x, y=samples['vWave_ct5'], mode='lines', name='New V wave (ct11)'), secondary_y=True)
            fig.add_trace(go.Scatter(x=x, y=samples['vWave_ct5'], mode='lines', name='New V wave (ct12)'), secondary_y=True)
            fig.add_trace(go.Scatter(x=x, y=samples['vWave_ct5'], mode='lines', name='New V wave (ct13)'), secondary_y=True)


    fig.update_layout(
        title=title,
        xaxis_title='Sample Number',
        yaxis_title='ADC Value (CTs)',
        yaxis2_title="ADC Value (Voltage)",
    )

    div = plotly.offline.plot(fig, show_link=False, output_type='div', include_plotlyjs='cdn')
    home_link = '<a href="/">Back to Index</a>'
    div = home_link + div
    if sample_rate:
        sample_rate = f'<p>Sample Rate: {sample_rate} KSPS</p>'
        div += sample_rate
    

    with open(f"{webroot}/{title.replace(' ', '_')}.html", 'w') as f:
        f.write(div)
