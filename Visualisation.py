import pandas as pd
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib as mpl

#colours for plotting
mpl.rcParams["text.color"] = "#7552cc"
mpl.rcParams["axes.labelcolor"] = "#ffffff"
mpl.rcParams["axes.titlecolor"] = "#7552cc"
mpl.rcParams["xtick.color"] = "#000000"
mpl.rcParams["ytick.color"] = "#000000"
mpl.rcParams["legend.labelcolor"] = "#000000"
mpl.rcParams["axes.edgecolor"] = "#000000"

#loading year
yearly_path = r'C:\\Users\\faadh\\Downloads\\CenturyPly_PnL.csv'
df = pd.read_csv(yearly_path)

df.columns = df.columns.astype(str).str.strip()
df["Narration"] = df["Narration"].astype(str).str.strip()
df = df.set_index("Narration")

years = [c for c in df.columns if c.isdigit()]
for c in years:
    df[c] = df[c].astype(str).str.replace(",", "", regex=False)
    df[c] = pd.to_numeric(df[c], errors="coerce")

sales      = df.loc["Sales", years]
expenses   = df.loc["Expenses", years]
op_profit  = df.loc["Operating Profit", years]
net_profit = df.loc["Net profit", years]
eps        = df.loc["EPS", years]
price      = df.loc["Price", years]

#trend data from PnL (could not access linearly for some reason)
trend_labels = ["10 Years", "7 Years", "5 Years", "3 Years", "Recent"]

sales_growth_trend = [11.94, 12.19, 14.34, 14.36, 16.52]
opm_trend          = [14.57, 13.95, 14.28, 13.19, 11.58]
pe_trend           = [41.59, 45.02, 52.11, 56.22, 68.76]

#quarterly loading
quarterly_path = r"C:\\Users\\faadh\\Downloads\\CenturyPly_Quarters.csv"
qdf = pd.read_csv(quarterly_path)

qdf.columns = qdf.columns.astype(str).str.strip()
qdf["Narration"] = qdf["Narration"].astype(str).str.strip()
qdf = qdf.set_index("Narration")

quarters = list(qdf.columns)
for c in quarters:
    qdf[c] = (
        qdf[c].astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("%", "", regex=False)
    )
    qdf[c] = pd.to_numeric(qdf[c], errors="coerce")

q_data = {
    "Sales": qdf.loc["Sales", quarters],
    "Expenses": qdf.loc["Expenses", quarters],
    "Operating Profit": qdf.loc["Operating Profit", quarters],
    "Other Income": qdf.loc["Other Income", quarters],
    "Depreciation": qdf.loc["Depreciation", quarters],
    "Interest": qdf.loc["Interest", quarters],
    "Profit Before Tax": qdf.loc["Profit before tax", quarters],
    "Tax": qdf.loc["Tax", quarters],
    "Net Profit": qdf.loc["Net profit", quarters],
    "OPM (%)": qdf.loc["OPM", quarters],
}

#canvas ui
root = tk.Tk()
root.title("Century Plyboards – Financial Dashboard")
root.geometry("1000x700")

charts = [
    "Sales Trend (Yearly)",
    "Expenses Trend (Yearly)",
    "Operating Profit Trend (Yearly)",
    "Net Profit Trend (Yearly)",
    "EPS Trend (Yearly)",
    "Price Trend (Yearly)",
    "Sales vs Expenses (Yearly)",
    "Sales Growth (Trends)",
    "OPM (Trends)",
    "Price to Earnings (Trends)",
    "Quarterly Dashboard (Jun-23 onwards)",
]

selected_chart = tk.StringVar(value=charts[0])

dropdown = ttk.Combobox(
    root,
    values=charts,
    textvariable=selected_chart,
    state="readonly",
    font=("Arial", 11),
)
dropdown.pack(pady=10)

content_frame = tk.Frame(root)
content_frame.pack(fill=tk.BOTH, expand=True)

def clear_frame():
    for widget in content_frame.winfo_children():
        widget.destroy()

#singular line chart
def show_line_chart(title, x, y):
    clear_frame()
    fig = Figure(figsize=(8.5, 5))
    ax = fig.add_subplot(111)
    ax.plot(x, y, marker="o", color="#7552cc")
    ax.set_title(title)
    ax.set_xlabel("Year")
    ax.set_ylabel("Value")
    ax.grid(alpha=0.3)

    canvas = FigureCanvasTkAgg(fig, master=content_frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()
#singular bar chart
def show_bar_chart(title, labels, values, ylabel):
    clear_frame()
    fig = Figure(figsize=(8.5, 5))
    ax = fig.add_subplot(111)
    ax.bar(labels, values)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", alpha=0.3)

    canvas = FigureCanvasTkAgg(fig, master=content_frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()

#quarterly dashboard
def show_quarterly_dashboard():
    clear_frame()

    canvas = tk.Canvas(content_frame)
    scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas)

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for title, series in q_data.items():
        fig = Figure(figsize=(8.5, 3))
        ax = fig.add_subplot(111)
        ax.plot(quarters, series, marker="o", color="#7552cc")
        ax.set_title(f"{title} – Quarterly")
        ax.set_xlabel("Quarter")
        ax.set_ylabel("Value")
        ax.grid(alpha=0.3)

        chart_canvas = FigureCanvasTkAgg(fig, master=scroll_frame)
        chart_canvas.get_tk_widget().pack(pady=10)
        chart_canvas.draw()

#dropdwon
def update_view(event=None):
    choice = selected_chart.get()

    if choice == "Sales Trend (Yearly)":
        show_line_chart("Sales Trend", years, sales)

    elif choice == "Expenses Trend (Yearly)":
        show_line_chart("Expenses Trend", years, expenses)

    elif choice == "Operating Profit Trend (Yearly)":
        show_line_chart("Operating Profit Trend", years, op_profit)

    elif choice == "Net Profit Trend (Yearly)":
        show_line_chart("Net Profit Trend", years, net_profit)

    elif choice == "EPS Trend (Yearly)":
        show_line_chart("EPS Trend", years, eps)

    elif choice == "Price Trend (Yearly)":
        show_line_chart("Price Trend", years, price)

    elif choice == "Sales vs Expenses (Yearly)":
        clear_frame()
        fig = Figure(figsize=(8.5, 5))
        ax = fig.add_subplot(111)
        ax.plot(years, sales, label="Sales", marker="o", color="#7552cc")
        ax.plot(years, expenses, label="Expenses", marker="o")
        ax.set_title("Sales vs Expenses (Yearly)")
        ax.legend()
        ax.grid(alpha=0.3)

        canvas = FigureCanvasTkAgg(fig, master=content_frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        canvas.draw()

    elif choice == "Sales Growth (Trends)":
        show_bar_chart("Sales Growth (%) – Trends", trend_labels, sales_growth_trend, "Percentage")

    elif choice == "OPM (Trends)":
        show_bar_chart("Operating Profit Margin (%) – Trends", trend_labels, opm_trend, "Percentage")

    elif choice == "Price to Earnings (Trends)":
        show_bar_chart("Price to Earnings Ratio – Trends", trend_labels, pe_trend, "P/E Ratio")

    elif choice == "Quarterly Dashboard (Jun-23 onwards)":
        show_quarterly_dashboard()

dropdown.bind("<<ComboboxSelected>>", update_view)
update_view()

root.mainloop()
