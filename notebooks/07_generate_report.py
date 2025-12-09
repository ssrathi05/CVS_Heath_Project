"""
Generate PDF Report from Analysis Notebook Results

This script creates a comprehensive PDF report from the analysis notebook.
It includes key findings, visualizations, and recommendations.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.patches as mpatches
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style for professional-looking plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def create_pdf_report(df, output_path='CVS_Health_Analysis_Report.pdf'):
    """
    Create a comprehensive PDF report from the analysis results.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The analysis dataset with all computed metrics
    output_path : str
        Path where the PDF will be saved
    """
    
    # Ensure required columns exist
    if 'health_burden_score' not in df.columns:
        health_vars = ['stroke', 'physical_inactivity', 'self_care_disability', 'social_isolation']
        available_vars = [var for var in health_vars if var in df.columns]
        if available_vars:
            df['health_burden_score'] = df[available_vars].mean(axis=1)
    
    if 'population' not in df.columns:
        print("Warning: Population data not found. Some metrics may be unavailable.")
        df['population'] = 100000  # Default
    
    if 'clinics_per_100k' not in df.columns and 'population' in df.columns:
        df['clinics_per_100k'] = (df['clinic_count'] / df['population']) * 100000
        df['clinics_per_100k'] = df['clinics_per_100k'].replace([np.inf, -np.inf], 0)
    
    if 'health_need' not in df.columns and 'health_burden_score' in df.columns:
        df['health_need'] = (
            (df['health_burden_score'] - df['health_burden_score'].min()) /
            (df['health_burden_score'].max() - df['health_burden_score'].min())
        )
    
    if 'pop_adjusted_gap' not in df.columns and 'health_need' in df.columns:
        df['pop_adjusted_gap'] = df['health_need'] * df['population']
    
    # Create PDF
    with PdfPages(output_path) as pdf:
        
        # ========== COVER PAGE ==========
        fig = plt.figure(figsize=(11, 8.5))
        fig.text(0.5, 0.7, 'CVS Health Community Access Analysis', 
                ha='center', va='center', fontsize=28, fontweight='bold')
        fig.text(0.5, 0.6, 'County-Level Health Needs & Clinic Distribution Report', 
                ha='center', va='center', fontsize=18)
        fig.text(0.5, 0.4, f'Generated: {datetime.now().strftime("%B %d, %Y")}', 
                ha='center', va='center', fontsize=14)
        fig.text(0.5, 0.3, f'Total Counties Analyzed: {len(df):,}', 
                ha='center', va='center', fontsize=14)
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
        
        # ========== EXECUTIVE SUMMARY ==========
        fig, ax = plt.subplots(figsize=(11, 8.5))
        ax.axis('off')
        
        summary_text = f"""
EXECUTIVE SUMMARY

Key Findings:

1. COVERAGE GAP
   • {((df['clinic_count'] == 0).sum() / len(df) * 100):.1f}% of U.S. counties have zero CVS MinuteClinic locations
   • Only {((df['clinic_count'] > 0).sum()):,} counties ({((df['clinic_count'] > 0).sum() / len(df) * 100):.1f}%) have at least one clinic
   • Total clinics across all counties: {df['clinic_count'].sum():.0f}

2. SOCIOECONOMIC INEQUITY
   • Counties without clinics have higher SVI scores: {df[df['clinic_count']==0]['svi_overall'].mean():.3f} vs {df[df['clinic_count']>0]['svi_overall'].mean():.3f}
   • Socioeconomic vulnerability: {df[df['clinic_count']==0]['svi_socioeconomic'].mean():.3f} (no clinics) vs {df[df['clinic_count']>0]['svi_socioeconomic'].mean():.3f} (with clinics)

3. HEALTH NEED MISMATCH
   • Counties without clinics have higher health burden: {df[df['clinic_count']==0]['health_burden_score'].mean():.2f} vs {df[df['clinic_count']>0]['health_burden_score'].mean():.2f}
   • This indicates sicker populations have less access to CVS services

4. TOP UNDERSERVED REGIONS
   • Mississippi Delta region
   • Rural South (Alabama, Georgia Black Belt)
   • South Texas border region
   • Native American communities in Southwest

5. URBAN OPPORTUNITIES
   • Large metropolitan areas show high population-adjusted gaps
   • Major cities with millions of residents have unmet demand
        """
        
        ax.text(0.1, 0.95, summary_text, transform=ax.transAxes, 
                fontsize=11, verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
        
        # ========== KEY STATISTICS ==========
        fig, axes = plt.subplots(2, 2, figsize=(11, 8.5))
        fig.suptitle('Key Statistics Overview', fontsize=16, fontweight='bold')
        
        # Clinic count distribution
        axes[0, 0].hist(df['clinic_count'], bins=50, edgecolor='black', alpha=0.7, color='steelblue')
        axes[0, 0].set_title('Distribution of Clinic Counts', fontweight='bold')
        axes[0, 0].set_xlabel('Number of Clinics')
        axes[0, 0].set_ylabel('Number of Counties')
        axes[0, 0].axvline(df['clinic_count'].median(), color='red', linestyle='--', 
                          label=f'Median: {df["clinic_count"].median():.1f}')
        axes[0, 0].legend()
        axes[0, 0].grid(alpha=0.3)
        
        # Health burden distribution
        axes[0, 1].hist(df['health_burden_score'], bins=50, edgecolor='black', alpha=0.7, color='purple')
        axes[0, 1].set_title('Distribution of Health Burden Scores', fontweight='bold')
        axes[0, 1].set_xlabel('Health Burden Score')
        axes[0, 1].set_ylabel('Number of Counties')
        axes[0, 1].axvline(df['health_burden_score'].mean(), color='red', linestyle='--',
                           label=f'Mean: {df["health_burden_score"].mean():.2f}')
        axes[0, 1].legend()
        axes[0, 1].grid(alpha=0.3)
        
        # SVI distribution
        axes[1, 0].hist(df['svi_overall'], bins=50, edgecolor='black', alpha=0.7, color='teal')
        axes[1, 0].set_title('Distribution of Social Vulnerability Index', fontweight='bold')
        axes[1, 0].set_xlabel('SVI Score')
        axes[1, 0].set_ylabel('Number of Counties')
        axes[1, 0].axvline(df['svi_overall'].mean(), color='red', linestyle='--',
                           label=f'Mean: {df["svi_overall"].mean():.3f}')
        axes[1, 0].legend()
        axes[1, 0].grid(alpha=0.3)
        
        # Clinic presence comparison
        clinic_presence = df['clinic_count'].apply(lambda x: 'No Clinics' if x == 0 else ('1-2 Clinics' if x <= 2 else '3+ Clinics'))
        comparison_data = df.groupby(clinic_presence)['health_burden_score'].mean()
        axes[1, 1].bar(comparison_data.index, comparison_data.values, color=['#d62728', '#ff7f0e', '#2ca02c'])
        axes[1, 1].set_title('Health Burden by Clinic Presence', fontweight='bold')
        axes[1, 1].set_xlabel('Clinic Presence Category')
        axes[1, 1].set_ylabel('Average Health Burden Score')
        axes[1, 1].tick_params(axis='x', rotation=45)
        axes[1, 1].grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
        
        # ========== BOX PLOTS ==========
        fig, axes = plt.subplots(1, 2, figsize=(11, 8.5))
        fig.suptitle('Comparative Analysis: Clinic Distribution by Vulnerability', fontsize=16, fontweight='bold')
        
        # SVI Quartiles
        df['svi_quartile'] = pd.qcut(df['svi_overall'], q=4, labels=['Low SVI (Q1)', 'Medium-Low SVI (Q2)', 
                                                                      'Medium-High SVI (Q3)', 'High SVI (Q4)'])
        sns.boxplot(data=df, x='svi_quartile', y='clinic_count', ax=axes[0], palette='viridis')
        axes[0].set_title('Clinic Count by SVI Quartiles', fontweight='bold')
        axes[0].set_xlabel('SVI Quartile')
        axes[0].set_ylabel('Number of Clinics')
        axes[0].tick_params(axis='x', rotation=45)
        axes[0].grid(axis='y', alpha=0.3)
        
        # Clinic Presence
        sns.boxplot(data=df, x=clinic_presence, y='health_burden_score', ax=axes[1], 
                   palette='Set2', order=['No Clinics', '1-2 Clinics', '3+ Clinics'])
        axes[1].set_title('Health Burden by Clinic Presence', fontweight='bold')
        axes[1].set_xlabel('Clinic Presence Category')
        axes[1].set_ylabel('Health Burden Score')
        axes[1].tick_params(axis='x', rotation=45)
        axes[1].grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
        
        # ========== TOP UNDERSERVED COUNTIES ==========
        if 'pop_adjusted_gap' in df.columns:
            top_underserved = df.nlargest(20, 'pop_adjusted_gap')[
                ['county_full', 'state_full', 'pop_adjusted_gap', 'health_burden_score', 
                 'clinic_count', 'population']]
            
            fig, ax = plt.subplots(figsize=(11, 8.5))
            colors = ['#d62728' if x == 0 else '#ff7f0e' if x <= 2 else '#2ca02c' 
                     for x in top_underserved['clinic_count']]
            bars = ax.barh(range(len(top_underserved)), top_underserved['pop_adjusted_gap'], color=colors)
            ax.set_yticks(range(len(top_underserved)))
            ax.set_yticklabels([f"{row['county_full']}, {row['state_full']}" 
                               for _, row in top_underserved.iterrows()])
            ax.set_xlabel('Population-Adjusted Gap Score', fontsize=12, fontweight='bold')
            ax.set_title('Top 20 Most Underserved Counties (High Need × Population)', 
                        fontsize=14, fontweight='bold')
            ax.invert_yaxis()
            ax.grid(axis='x', alpha=0.3)
            
            legend_elements = [mpatches.Patch(facecolor='#d62728', label='0 Clinics'),
                             mpatches.Patch(facecolor='#ff7f0e', label='1-2 Clinics'),
                             mpatches.Patch(facecolor='#2ca02c', label='3+ Clinics')]
            ax.legend(handles=legend_elements, loc='lower right')
            
            plt.tight_layout()
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()
        
        # ========== STATE-LEVEL SUMMARY ==========
        state_stats = df.groupby('state_full').agg({
            'clinic_count': 'sum',
            'population': 'sum',
            'health_burden_score': 'mean',
            'svi_overall': 'mean'
        }).reset_index()
        
        if 'population' in state_stats.columns:
            state_stats['clinics_per_100k'] = (state_stats['clinic_count'] / state_stats['population']) * 100000
            top_states = state_stats.sort_values('clinics_per_100k', ascending=False).head(15)
            
            fig, ax = plt.subplots(figsize=(11, 8.5))
            bars = ax.barh(range(len(top_states)), top_states['clinics_per_100k'], color='steelblue')
            ax.set_yticks(range(len(top_states)))
            ax.set_yticklabels(top_states['state_full'])
            ax.set_xlabel('Clinics per 100,000 Population', fontsize=12, fontweight='bold')
            ax.set_title('Top 15 States by CVS Clinic Density', fontsize=14, fontweight='bold')
            ax.invert_yaxis()
            ax.grid(axis='x', alpha=0.3)
            
            for i, (idx, row) in enumerate(top_states.iterrows()):
                ax.text(row['clinics_per_100k'] + 0.1, i, f"{row['clinics_per_100k']:.2f}", 
                       va='center', fontsize=10)
            
            plt.tight_layout()
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()
        
        # ========== RECOMMENDATIONS ==========
        fig, ax = plt.subplots(figsize=(11, 8.5))
        ax.axis('off')
        
        recommendations = """
STRATEGIC RECOMMENDATIONS

Priority 1: High-Impact Urban Expansion
• Focus on large metropolitan counties with high health burden and moderate-to-low clinic density
• Target: Los Angeles County, Harris County (Houston), Dallas County, Maricopa County (Phoenix)
• Rationale: Maximum population impact with existing infrastructure

Priority 2: Rural High-Need Markets
• Target rural counties with high health burden scores and zero clinics
• Focus on Mississippi Delta, rural South, and Native American communities
• Consider mobile clinics or partnerships with existing healthcare facilities

Priority 3: Vulnerable Community Access
• Prioritize counties with high SVI scores and zero clinics
• Address socioeconomic barriers to healthcare access
• Consider sliding scale pricing or community health partnerships

Priority 4: Cluster-Based Expansion
• Use K-means clustering results to identify similar counties
• Develop standardized expansion strategies for each cluster type
• Leverage successful clinic models from similar county types

NEXT STEPS

1. Validate Findings: Cross-reference identified underserved counties with local healthcare 
   infrastructure and competitor presence
2. Market Research: Conduct feasibility studies for top-priority expansion targets
3. Partnership Opportunities: Explore partnerships with local health systems in underserved areas
4. Pilot Programs: Launch pilot clinics in 2-3 high-priority counties to test expansion model
5. Monitor Impact: Track health outcomes and utilization rates in new clinic locations
6. Iterate Strategy: Use clustering results to refine expansion criteria and identify new 
   opportunities
        """
        
        ax.text(0.1, 0.95, recommendations, transform=ax.transAxes, 
                fontsize=11, verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
        
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
        
    print(f"✓ PDF report generated successfully: {output_path}")
    return output_path


if __name__ == "__main__":
    # Load the data
    data_path = r"C:\Users\14122\OneDrive\Desktop\cvs_heath_project\data\processed\CVS_FINAL_DATASET.csv"
    df = pd.read_csv(data_path)
    
    # Clean data
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col], errors='ignore')
        except:
            pass
    
    # Generate report
    output_file = r"C:\Users\14122\OneDrive\Desktop\cvs_heath_project\CVS_Health_Analysis_Report.pdf"
    create_pdf_report(df, output_file)
    print(f"\nReport saved to: {output_file}")

