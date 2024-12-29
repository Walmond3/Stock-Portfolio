# Define or import the generate_pdf_report function here

from fpdf import FPDF
import pandas as pd
from io import BytesIO


def generate_pdf_report(optimal_weights_df, portfolio_return_value, portfolio_risk_value, portfolio_excess_return, sharpe_ratio, sortino_ratio, max_drawdown):
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
        pdf.cell(200, 10, txt=f"{row['Stock']}: {row['Optimal Weights']}", ln=True)
    pdf.ln(10)

    pdf.cell(200, 10, txt=f"Portfolio Return: {portfolio_return_value:.4f}", ln=True)
    pdf.cell(200, 10, txt=f"Portfolio Risk: {portfolio_risk_value:.4f}", ln=True)
    pdf.cell(200, 10, txt=f"Portfolio Excess Return: {portfolio_excess_return:.4f}", ln=True)
    pdf.cell(200, 10, txt=f"Sharpe Ratio: {sharpe_ratio:.4f}", ln=True)
    pdf.cell(200, 10, txt=f"Sortino Ratio: {sortino_ratio:.4f}", ln=True)
    pdf.cell(200, 10, txt=f"Maximum Drawdown: {max_drawdown:.4f}", ln=True)

    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    return pdf_output.getvalue()

if __name__ == "__main__":
    # Dummy data for testing
    test_weights_df = pd.DataFrame({'Stock': ['AAPL', 'GOOGL'], 'Optimal Weights': [0.6, 0.4]})
    test_return = 0.08
    test_risk = 0.15
    test_excess_return = 0.05
    test_sharpe = 0.67
    test_sortino = 0.95
    test_drawdown = 0.1

    # Test PDF generation
    pdf_data = generate_pdf_report(
        test_weights_df, test_return, test_risk, test_excess_return, test_sharpe, test_sortino, test_drawdown
    )

    with open("test_report.pdf", "wb") as f:
        f.write(pdf_data)

    print("PDF generated and saved as test_report.pdf")
