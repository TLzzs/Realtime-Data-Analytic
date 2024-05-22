import warnings
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ---------------------
# Plot Map
# ---------------------

map_titles = {
    'crime':'Top 10 Suburbs with Highest Crimes (VIC)',
    'temp':'Top 10 Suburbs with Highest Annual Temperature (VIC)',
    'precip':'Top 10 Suburbs with Highest Annual Precipitation (VIC)'
}

gdf = gpd.read_file("../data/georef-australia-local-government-area@public.geojson")

map_titles = {
    'crime':'Top 10 Suburbs with Highest Crimes in Victoria',
    'temp':'Top 10 Suburbs with Highest Annual Temperature (VIC)',
    'precip':'Top 10 Suburbs with Highest Annual Precipitation (VIC)'
}

def plot_map(map_type,highlight_suburbs):
    map_title = map_titles[map_type]
    # Suppress the warning
    warnings.filterwarnings("ignore", message="Geometry is in a geographic CRS")
    warnings.filterwarnings("ignore", message="Legend does not support handles for PatchCollection instances.")
    gdf['lga_name'] = gdf['lga_name'].apply(lambda x: ', '.join(x))

    # Group the GeoDataFrame by 'lga_name'
    grouped = gdf.groupby('lga_name')

    # Plot all polygons on a single map with different colors for each group
    _, ax = plt.subplots(figsize=(10, 8))

    for i, (name, group) in enumerate(grouped):
        if name in highlight_suburbs:
            group.plot(ax=ax, label=name, color='orange')
            centroid = group['geometry'].centroid.iloc[0]
            ax.annotate(name, (centroid.x, centroid.y), fontsize=8, ha='center',color='gray')
        else:
            group.plot(ax=ax, label=name, color='#F8F8F8',edgecolor='lightgrey')

    # Plot with title
    plt.axis('off')
    plt.suptitle(map_title, y=0.82, fontsize=10, fontweight='bold')
    plt.tight_layout()
    plt.legend()
    plt.show()

# ---------------------
# Plot Scatterplot
# ---------------------

scatter_annotations = {
    'title': {
        'average_temp':'Temperature vs. Crime in High-Crime Victoria Suburbs',
        'average_rain':'Precipitation vs. Crime in High-Crime Victoria Suburbs'
    },
    'xlabel': {
        'average_temp':'Annual Average Temperature (°C)',
        'average_rain':'Annual Average Preciptation (cm)'
    }
}

def plot_scatter_chart(scatter_type,data):
    # Extracting data
    feature_data = [entry[scatter_type] for entry in data]
    count_data = [entry['total_offences'] for entry in data]
    suburbs = [entry['suburb_name'] for entry in data]

    # Create Scatter Plot
    plt.figure(figsize=(10, 5))
    plt.scatter(feature_data, count_data, color='orange')

    # Add Trend Line
    sns.regplot(x=feature_data, y=count_data, scatter=False, color='orange')

    # Add annotations for each suburb
    for i, suburb in enumerate(suburbs):
        plt.text(feature_data[i], count_data[i], suburb, ha='center', va='bottom', size='small')

    # Plot with title, xlabel, and ylabel
    plt.title(scatter_annotations['title'][scatter_type], fontweight='bold', fontsize=10)
    plt.xlabel(scatter_annotations['xlabel'][scatter_type], fontweight='bold')
    plt.ylabel('Number of Crimes', fontweight='bold')

    # Dynamically adjust limits
    x_range = max(feature_data) - min(feature_data)
    y_range = max(count_data) - min(count_data)
    x_padding = 0.1 * x_range
    y_padding = 0.1 * y_range

    plt.xlim(min(feature_data) - x_padding, max(feature_data) + x_padding)
    plt.ylim(min(count_data) - y_padding, max(count_data) + y_padding)
    plt.show()

# ---------------------
# Plot Bar Chart
# ---------------------

bar_annotations = {
    'title': {
        'average_temp':'Temperature',
        'average_rain':'Preciptation'
    },
    'ylabel': {
        'average_temp':'Annual Average Temperature (°C)',
        'average_rain':'Annual Average Preciptation (cm)'
    }
}

def plot_bar_chart(bar_type, data):
    # Extracting data
    suburbs = [entry['suburb_name'] for entry in data]
    total_a_offences = [entry['total_a_offences'] for entry in data]
    total_b_offences = [entry['total_b_offences'] for entry in data]
    feature_data = [entry[bar_type] for entry in data] # temperature or rain

    # Set up the data for plotting
    x = np.arange(len(suburbs))
    bar_width = 0.35

    # Increase the figure width
    plt.figure(figsize=(12, 6))

    # Subplot for Type A Crime
    plt.subplot(1, 2, 1)
    plt.bar(x, total_a_offences, bar_width, label='Type A Crime', color='#ADD8E6', edgecolor='grey')
    plt.xlabel('Suburbs',fontweight='bold')
    plt.ylabel('Number of Type A Crimes',fontweight='bold')
    plt.title("Type A Crime (Crimes Against the Person)", fontsize=10, fontweight='bold')
    plt.xticks(x, suburbs, rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(loc='upper left')

    # Temperature/Precipitation line plot for Type A Crime
    ax2 = plt.gca().twinx()
    ax2.plot(x, feature_data, color='orange', marker='o', label=bar_annotations['title'][bar_type])
    ax2.set_ylabel(bar_annotations['ylabel'][bar_type],fontweight='bold')
    ax2.legend(loc='upper right')

    # Subplot for Type B Crime
    plt.subplot(1, 2, 2)
    plt.bar(x, total_b_offences, bar_width, label='Type B Crime', color='#F08080', edgecolor='grey')
    plt.xlabel('Suburbs',fontweight='bold')
    plt.ylabel('Number of Type B Crimes',fontweight='bold')
    plt.title("Type B Crime (Property and Deception Offences)", fontsize=10, fontweight='bold')
    plt.xticks(x, suburbs, rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(loc='upper left')

    # Temperature/Precipitation line plot for Type B Crime
    ax2 = plt.gca().twinx()
    ax2.plot(x, feature_data, color='orange', marker='o', label=bar_annotations['title'][bar_type])
    ax2.set_ylabel(bar_annotations['ylabel'][bar_type],fontweight='bold')
    ax2.legend(loc='upper right')

    suptitle = f"Different Types of Crimes vs. {bar_annotations['title'][bar_type]} in High-Crime Victoria Suburbs"
    plt.suptitle(suptitle,fontweight='bold',fontsize=12)
    plt.tight_layout()
    plt.show()

# ---------------------
# Plot Pie Chart
# ---------------------

sentiments = ['Negative','Neutral','Positive']
colors = ['#F08080','#90EE90','#ADD8E6']

def plot_pie_chart(data):
    plt.figure(figsize=(8, 4))
    for i, year_data in enumerate(data):
        plt.subplot(1, len(data), i + 1)
        plt.pie(year_data['sentiment_counts'].values(),labels=sentiments,autopct='%1.1f%%',startangle=90, colors=colors)
        plt.gca().set_aspect('equal')
        plt.title(f"Year {year_data['year']}",fontweight='semibold',fontsize=10)
        plt.xlabel(f"Number of Crimes = {year_data['total_crimes']}",fontweight='semibold',fontsize=10)

    plt.suptitle('Sentiment Percentage vs. Crime in Victoria', fontweight='bold', fontsize=10)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()
