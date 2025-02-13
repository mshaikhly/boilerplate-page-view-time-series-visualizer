import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data
df = df[df['value'].between(df['value'].quantile(0.025), df['value'].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df['value'], color='red', linewidth=1)

    # Add title and labels
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019", fontsize=14)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Page Views", fontsize=12)
    
    # Format x-axis ticks
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability

    # Add grid
    ax.grid(True, linestyle='--', alpha=0.6)

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.strftime('%b')  # Convert to month name

    # Sort months correctly
    month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September","October", "November", "December"]

    # Group data by year and month
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(12, 6))
    df_bar.plot(kind='bar', ax=ax)

    # Set labels and title
    ax.set_xlabel("Years", fontsize=12)
    ax.set_ylabel("Average Page Views", fontsize=12)
    ax.set_title("Monthly Average Page Views per Year", fontsize=14)

    # Set legend and order months correctly
    ax.legend(title="Months", labels=month_order)

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')

    # 🔹 Ensure 'value' is numeric to prevent Seaborn errors
    df_box["value"] = pd.to_numeric(df_box["value"], errors="coerce")

    # Create subplots
    fig, axes = plt.subplots(1, 2, figsize=(32, 10), dpi=100)

    # Year-wise Box Plot (Trend)
    sns.boxplot(data=df_box, x="year", y="value", ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # Month-wise Box Plot (Seasonality)
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    sns.boxplot(data=df_box, x="month", y="value", order=month_order, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig