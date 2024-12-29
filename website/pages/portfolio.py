import streamlit as st
from scipy.optimize import minimize
import pandas as pd
import numpy as np
from sklearn.covariance import EmpiricalCovariance
from io import BytesIO
from fpdf import FPDF

def app():

    def portfolio(df, selected_stock, expected_returns, risk_free_rate_input=0.0312, benchmark=False):
        # Filter data
        filtered_df = df[df['Stock'].isin(selected_stocks)]

        monthly_returns = pd.DataFrame()
        grouped_data = filtered_df.groupby('Stock')
        for stock, data in grouped_data:
            monthly_returns[stock] = data['Future_Return'].values

        # Covariance matrix
        cov_estimator = EmpiricalCovariance().fit(monthly_returns)
        Sigma = cov_estimator.covariance_
      
        # User-provided expected returns
        mu = np.array([expected_returns[stock] for stock in selected_stocks])
      
        n_assets = len(mu)
        risk_free_rate = risk_free_rate_input / 3
      
        if benchmark:
            optimal_weights = np.ones(n_assets) / n_assets
            optimal_weights_df = pd.DataFrame({
                'Stock': selected_stocks,
                'Optimal Weights': optimal_weights
            })
      
        else:
            max_weight = 1 / n_assets + 0.2
      
            def weight_sum_constraint(w):
                return np.sum(w) - 1
      
            def long_only_constraint(w):
                return w
      
            def max_weight_constraint(w, max_weight):
                return max_weight - w
      
            def negative_sharpe_ratio(w, mu, Sigma, risk_free_rate):
                portfolio_return = np.dot(mu, w)
                portfolio_volatility = np.sqrt(np.dot(w.T, np.dot(Sigma, w)))
                excess_return = portfolio_return - risk_free_rate
                return -excess_return / portfolio_volatility
      
            initial_guess = np.ones(n_assets)/ n_assets
      
            constraints = [
                {'type': 'eq', 'fun': weight_sum_constraint},
                {'type': 'ineq', 'fun': long_only_constraint},
                {'type': 'ineq', 'fun': lambda w: max_weight - w}
            ]
      
            result = minimize(
                negative_sharpe_ratio,
                initial_guess,
                args = (mu, Sigma, risk_free_rate),
                method='SLSQP',
                constraints=constraints,
                bounds=[(0,1) for _ in range(n_assets)],
                options={'disp': True}
            )
      
            optimal_weights = result.x
            optimal_weights = np.round(optimal_weights, 2)
            rounding_error = 1- np.sum(optimal_weights)
            adjustment_index = np.argmax(optimal_weights)
            optimal_weights[adjustment_index] += rounding_error
            optimal_weights_df = pd.DataFrame({
                'Stock': selected_stocks,
                'Optimal Weights': optimal_weights
            })
      
        portfolio_return_value = np.dot(mu, optimal_weights)
        portfolio_risk_value = np.sqrt(np.dot(optimal_weights.T, np.dot(Sigma, optimal_weights)))
        portfolio_excess_return = portfolio_return_value - risk_free_rate
      
        sharpe_ratio = portfolio_excess_return / portfolio_risk_value
      
        portfolio_returns = np.dot(monthly_returns, optimal_weights)
        negative_returns = portfolio_returns[portfolio_returns < 0]
        downside_risk = np.std(negative_returns)
        sortino_ratio = portfolio_excess_return / downside_risk
      
        cumulative_returns = np.cumsum(portfolio_returns)
        peaks = np.maximum.accumulate(cumulative_returns)
        drawdowns = (peaks - cumulative_returns) / peaks
        max_drawdown = np.max(drawdowns)

        return optimal_weights_df, np.round(portfolio_return_value, 4), np.round(portfolio_risk_value, 4), np.round(portfolio_excess_return, 4), np.round(sharpe_ratio, 4), np.round(sortino_ratio, 4), np.round(max_drawdown, 4)

    def generate_pdf_report(optimal_weights_df, portfolio_return_value, portfolio_risk_value, portfolio_excess_return, sharpe_ratio, sortino_ratio, max_drawdown):
        try:
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="Portfolio Optimization Report", ln=True, align="C")
            pdf.ln(10)

            pdf.set_font("Arial", size=12)
            pdf.cell(100, 10, txt="Portfolio Performance Metrics", ln=True)
            pdf.ln(5)

            pdf.cell(200, 10, txt="Optimal Weights:", ln=True)
            pdf.ln(5)
            for index, row in optimal_weights_df.iterrows():
                pdf.cell(200, 10, txt=f"{row['Stock']}: {row['Optimal Weights']:.2f}", ln=True)
            pdf.ln(10)

            pdf.cell(200, 10, txt=f"Portfolio Return: {portfolio_return_value:.4f}", ln=True)
            pdf.cell(200, 10, txt=f"Portfolio Risk: {portfolio_risk_value:.4f}", ln=True)
            pdf.cell(200, 10, txt=f"Portfolio Excess Return: {portfolio_excess_return:.4f}", ln=True)
            pdf.cell(200, 10, txt=f"Sharpe Ratio: {sharpe_ratio:.4f}", ln=True)
            pdf.cell(200, 10, txt=f"Sortino Ratio: {sortino_ratio:.4f}", ln=True)
            pdf.cell(200, 10, txt=f"Maximum Drawdown: {max_drawdown:.4f}", ln=True)

            # Save PDF to BytesIO object
            pdf_output = BytesIO()
            pdf.output(pdf_output)
            pdf_output.seek(0)

            return pdf_output.getvalue()

        except Exception as e:
            st.error(f"Error in PDF generation: {e}")
            return None

    st.header('Portfolio Optimization')

    # Upload file
    uploaded_stock_file = st.file_uploader("Upload Stock Data CSV", type=["csv"])

    if uploaded_stock_file is not None:
        df = pd.read_csv(uploaded_stock_file)

        # Ensure user selects stocks from the df
        stocks = df['Stock'].unique()
        selected_stocks = st.multiselect('Select Stocks (3 to 5)', options=stocks, default=stocks[:5])

        # Validation: Ensure user selects 3 to 5 stocks
        if len(selected_stocks) < 3:
            st.warning("Please select at least 3 stocks.")
        elif len(selected_stocks) > 5:
            st.warning("Please select no more than 5 stocks.")

        if len(selected_stocks) >= 3 and len(selected_stocks) <= 5:
            # Input expected return
            expected_returns = {}
            for stock in selected_stocks:
                user_return = st.number_input(f"Enter expected return for {stock}", min_value=-1.0, max_value=1.0, value=None, format="%.6f")
                if user_return is not None:
                    expected_returns[stock] = user_return
                else:
                    default_return = 0.05
                    expected_returns[stock] = default_return
      
            # Risk-free rate input
            risk_free_rate_input = st.number_input("Enter risk-free rate (%)", min_value=0.0, max_value=10.0, value=3.12, format="%.6f") / 100
      
            # Option to use benchmark (equal weights)
            benchmark = st.checkbox("Use benchmark (Equal Weights)")
      
            # Run optimization
            if st.button('Optimize'):
                optimal_weights_df, portfolio_return_value, portfolio_risk_value, portfolio_excess_return, sharpe_ratio, sortino_ratio, max_drawdown = portfolio(
                        df, selected_stocks, expected_returns, risk_free_rate_input, benchmark
                    )

                # Store the results in session state to persist them across interactions
                st.session_state.optimized_weights = optimal_weights_df
                st.session_state.portfolio_return = portfolio_return_value
                st.session_state.portfolio_risk = portfolio_risk_value
                st.session_state.portfolio_excess_return = portfolio_excess_return
                st.session_state.sharpe_ratio = sharpe_ratio
                st.session_state.sortino_ratio = sortino_ratio
                st.session_state.max_drawdown = max_drawdown

                # Display results
                st.write("Optimal Weights:", optimal_weights_df)
                st.write(f"Portfolio Return: {portfolio_return_value:.4f}")
                st.write(f"Portfolio Risk: {portfolio_risk_value:.4f}")
                st.write(f"Portfolio Excess Return: {portfolio_excess_return:.4f}")
                st.write(f"Sharpe Ratio: {sharpe_ratio:.4f}")
                st.write(f"Sortino Ratio: {sortino_ratio:.4f}")
                st.write(f"Maximum Drawdown: {max_drawdown:.4f}")

                # Generate PDF report
                pdf_data = generate_pdf_report(
                    st.session_state.optimized_weights,
                    st.session_state.portfolio_return,
                    st.session_state.portfolio_risk,
                    st.session_state.portfolio_excess_return,
                    st.session_state.sharpe_ratio,
                    st.session_state.sortino_ratio,
                    st.session_state.max_drawdown
                )

                # Store the PDF data in session state
                st.session_state.pdf_report = pdf_data

            # Display the download button only once the PDF is generated
            if 'pdf_report' in st.session_state:
                st.download_button(
                    label="Download PDF Report",
                    data=st.session_state.pdf_report,
                    file_name="portfolio_report.pdf",
                    mime="application/pdf"
                )

if __name__ == "__main__":
    app()
