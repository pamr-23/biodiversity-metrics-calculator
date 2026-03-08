"""
Biodiversity Metrics Calculator
Author: Paula Murcia
Description: Calculate ecological biodiversity metrics from species data
"""

import pandas as pd
import numpy as np
from typing import Dict

class BiodiversityMetrics:
    """
    Calculate biodiversity metrics from species detection data.
    
    Input data should have columns: 'species' and 'count'
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize with species detection data.
        
        Args:
            data: DataFrame with columns 'species' and 'count'
        """
        self.data = data
        self._validate_data()
    
    def _validate_data(self):
        """Check that data has required columns."""
        required = ['species', 'count']
        if not all(col in self.data.columns for col in required):
            raise ValueError(f"Data must have columns: {required}")
        
        if self.data['count'].isna().any():
            raise ValueError("Count column has missing values")
    
    def species_richness(self) -> int:
        """
        Calculate species richness (total unique species).
        
        Returns:
            Number of unique species
        """
        return self.data['species'].nunique()
    
    def relative_abundance(self) -> pd.DataFrame:
        """
        Calculate relative abundance for each species.
        
        Formula: (count_i / total_count) * 100
        
        Returns:
            DataFrame with species and their relative abundance (%)
        """
        total = self.data['count'].sum()
        result = self.data.copy()
        result['relative_abundance'] = (result['count'] / total) * 100
        return result.sort_values('relative_abundance', ascending=False)
    
    def shannon_index(self) -> float:
        """
        Calculate Shannon Diversity Index.
        
        Formula: H' = -Σ(p_i * ln(p_i))
        where p_i is proportion of species i
        
        Returns:
            Shannon index value
        """
        total = self.data['count'].sum()
        proportions = self.data['count'] / total
        proportions = proportions[proportions > 0]  # Remove zeros
        return float(-np.sum(proportions * np.log(proportions)))
    
    def simpson_index(self) -> float:
        """
        Calculate Simpson's Diversity Index.
        
        Formula: D = 1 - Σ(n_i * (n_i - 1)) / (N * (N - 1))
        
        Returns:
            Simpson index (0-1, higher = more diverse)
        """
        total = self.data['count'].sum()
        sum_n = np.sum(self.data['count'] * (self.data['count'] - 1))
        return float(1 - (sum_n / (total * (total - 1))))
    
    def dominant_species(self, top_n: int = 5) -> pd.DataFrame:
        """
        Get most abundant species.
        
        Args:
            top_n: Number of top species to return
            
        Returns:
            DataFrame with top N species
        """
        abundance = self.relative_abundance()
        return abundance.head(top_n)[['species', 'count', 'relative_abundance']]
    
    def calculate_all(self) -> Dict:
        """
        Calculate all metrics at once.
        
        Returns:
            Dictionary with all metrics
        """
        return {
            'species_richness': self.species_richness(),
            'shannon_index': round(self.shannon_index(), 3),
            'simpson_index': round(self.simpson_index(), 3),
            'total_observations': int(self.data['count'].sum()),
            'dominant_species': self.dominant_species().to_dict('records')
        }
    
    def summary_report(self) -> str:
        """
        Generate text summary of metrics.
        
        Returns:
            Formatted string with results
        """
        metrics = self.calculate_all()
        top_species = metrics['dominant_species'][0]
        
        report = f"""
BIODIVERSITY ASSESSMENT SUMMARY
================================

Species Richness: {metrics['species_richness']} unique species
Total Observations: {metrics['total_observations']}

Diversity Indices:
- Shannon Index: {metrics['shannon_index']} 
  (Range: 0-5, typical 1.5-3.5, higher = more diverse)
- Simpson Index: {metrics['simpson_index']} 
  (Range: 0-1, higher = more diverse)

Most Abundant Species:
{top_species['species']}: {top_species['count']} observations 
({top_species['relative_abundance']:.1f}% of total)

Interpretation:
- Shannon > 3: High diversity
- Shannon 1-3: Moderate diversity  
- Shannon < 1: Low diversity
        """
        return report
