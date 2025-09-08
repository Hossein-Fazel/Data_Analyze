import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_data(filepath='salary_data.csv'):
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"Error: The file {filepath} was not found. Run the scrape_data.py script first.")
        return

    print("--- Basic Data Info ---")
    print(df.info())
    print("\n--- Data Head ---")
    print(df.head())

    print("\n--- Highest and Lowest Salaries ---")
    highest_salary = df.loc[df['Average Salary (Local Currency)'].idxmax()]
    lowest_salary = df.loc[df['Average Salary (Local Currency)'].idxmin()]
    print("Highest Salary Record:\n", highest_salary)
    print("\nLowest Salary Record:\n", lowest_salary)

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 8))

    sns.barplot(data=df, x='Country', y='Average Salary (Local Currency)', hue='Profession', ax=ax)

    ax.set_title('Average Tech Salaries by Country and Profession', fontsize=16, weight='bold')
    ax.set_xlabel('Country', fontsize=12)
    ax.set_ylabel('Average Salary (Local Currency - Not Normalized)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    output_plot_path = 'salary_comparison_chart.png'
    plt.savefig(output_plot_path)
    print(f"\nChart saved to {output_plot_path}")
    
    plt.show()

if __name__ == "__main__":
    analyze_data()