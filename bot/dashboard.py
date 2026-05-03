import streamlit as st
import pandas as pd
from database import get_all_trades, get_statistics
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="AAPL Trading Bot", layout="wide", initial_sidebar_state="expanded")

st.title("🤖 AAPL Trading Bot Dashboard")
st.markdown("---")

# ESTADÍSTICAS PRINCIPALES
col1, col2, col3, col4, col5 = st.columns(5)

stats = get_statistics()

with col1:
    st.metric("Total Trades", stats['total_trades'])
with col2:
    st.metric("Ganadores", stats['winning_trades'])
with col3:
    st.metric("Win Rate", f"{stats['win_rate']:.1f}%")
with col4:
    st.metric("Total Return", f"{stats['total_return']:+.2f}%", 
              delta=f"{stats['avg_return']:+.2f}% avg")
with col5:
    st.metric("Última actualización", datetime.now().strftime("%H:%M:%S"))

st.markdown("---")

# TABLA DE TRADES
st.subheader("📊 Historial de Trades")

trades = get_all_trades()

if trades:
    columns = ['ID', 'Symbol', 'Entry Time', 'Entry Price', 'Exit Time', 'Exit Price', 'PnL', 'Return %', 'Status', 'Rolling STD']
    df_trades = pd.DataFrame(trades, columns=columns + ['Created'])
    df_trades = df_trades[columns]  # Mostrar solo columnas importantes
    
    # Colorear por status
    def color_status(status):
        if status == 'CLOSED':
            return '✅ CLOSED'
        return '🟢 OPEN'
    
    df_trades['Status'] = df_trades['Status'].apply(color_status)
    
    st.dataframe(df_trades, width='stretch')
    
    # GRÁFICO DE P&L
    closed_trades = [t for t in trades if t[8] == 'CLOSED']  # Index 8 es status
    
    if closed_trades:
        st.subheader("📈 Análisis de Ganancias/Pérdidas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de returns por trade
            returns = [t[7] for t in closed_trades]  # Index 7 es return_pct
            trade_ids = [f"Trade #{t[0]}" for t in closed_trades]
            
            fig = go.Figure()
            colors = ['green' if r > 0 else 'red' for r in returns]
            fig.add_trace(go.Bar(x=trade_ids, y=returns, marker=dict(color=colors)))
            fig.update_layout(title="Return por Trade (%)", xaxis_title="Trade", yaxis_title="Return %")
            st.plotly_chart(fig, width='stretch')
        
        with col2:
            # Distribución de returns
            fig = px.histogram(x=returns, nbins=10, labels={'x': 'Return %', 'count': 'Frequency'})
            fig.update_layout(title="Distribución de Returns")
            st.plotly_chart(fig, width='stretch')
        
        # Equity curve
        st.subheader("💰 Equity Curve")
        
        equity = [100]  # Inicial
        for ret in returns:
            equity.append(equity[-1] * (1 + ret/100))
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=equity, mode='lines', name='Equity', 
                                 fill='tozeroy', line=dict(color='blue', width=2)))
        fig.update_layout(title="Equity Curve", xaxis_title="Trade #", yaxis_title="Equity ($)")
        st.plotly_chart(fig, width='stretch')

else:
    st.warning("No hay trades aún. Ejecuta el bot para generar datos.")

st.markdown("---")
st.caption("🚀 AAPL Trading Bot | Desarrollado con Python + Streamlit")