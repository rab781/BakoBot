"""Data visualization module for price arbitrage."""

import os
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns

from config.settings import PROJECT_ROOT
from config.constants import DAERAH_LIST
from src.utils.logger import logger

def generate_price_chart(komoditas: str, data: list[dict[str, Any]]) -> str | None:
    """
    Generate horizontal bar chart for a commodity across regions.
    
    Args:
        komoditas: Name of the commodity
        data: List of dicts with 'kode_daerah' and 'harga_int'
        
    Returns:
        Path to the generated image file, or None if failed
    """
    if not data:
        return None
        
    try:
        # Prepare data
        regions = []
        prices = []
        
        # Sort data highest to lowest so the cheapest is at the bottom (or top) of horizontal bar
        # In matplotlib barh, the first item is at the bottom. 
        # We want cheapest at the top, so we sort lowest to highest, then matplotlib plots bottom-up.
        data_sorted = sorted(data, key=lambda x: x["harga_int"], reverse=True)
        
        for item in data_sorted:
            # Get full region name from constants, fallback to kode_daerah
            full_name = DAERAH_LIST.get(item["kode_daerah"], item["kode_daerah"]).replace("Kab. ", "").replace("Kota ", "")
            regions.append(full_name)
            prices.append(item["harga_int"])
            
        # Create figure
        # Height depends on number of regions (max 38)
        fig_height = max(8, len(regions) * 0.3)
        plt.figure(figsize=(10, fig_height))
        
        # Set style
        sns.set_theme(style="whitegrid")
        
        # Determine colors: cheapest is green, most expensive is red, rest is blue
        colors = []
        min_price = min(prices)
        max_price = max(prices)
        
        for p in prices:
            if p == min_price:
                colors.append('#2ecc71')  # Emerald green
            elif p == max_price:
                colors.append('#e74c3c')  # Alizarin red
            else:
                colors.append('#3498db')  # Peter river blue
                
        # Create horizontal bar chart
        ax = sns.barplot(x=prices, y=regions, palette=colors)
        
        # Customize chart
        plt.title(f"Peta Harga Lintas Daerah\\n{komoditas.upper()}", fontsize=16, pad=20, fontweight='bold')
        plt.xlabel("Harga (Rp)", fontsize=12)
        plt.ylabel("Daerah", fontsize=12)
        
        # Add value labels to bars
        for i, p in enumerate(prices):
            ax.text(p + (max_price * 0.01), i, f"Rp {p:,}".replace(',', '.'), 
                    va='center', fontsize=9)
            
        # Add padding to x-axis to fit the labels
        plt.xlim(0, max_price * 1.15)
        
        plt.tight_layout()
        
        # Save figure
        temp_dir = PROJECT_ROOT / "data" / "temp"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = temp_dir / f"chart_{komoditas.replace(' ', '_').lower()}.png"
        plt.savefig(file_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info("Successfully generated chart for %s at %s", komoditas, file_path)
        return str(file_path)
        
    except Exception as e:
        logger.error("Failed to generate price chart: %s", e)
        return None
