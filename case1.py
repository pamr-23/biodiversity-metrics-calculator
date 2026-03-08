import pandas as pd
from metrics import BiodiversityMetrics

# Sample data - replace with your own CSV
data = pd.DataFrame({
    'species': [
        'American Robin', 'Song Sparrow', 'Blue Jay', 'Northern Cardinal',
        'Black-capped Chickadee', 'Downy Woodpecker', 'American Crow',
        'Red-winged Blackbird', 'Common Grackle', 'House Finch'
    ],
    'count': [45, 38, 28, 22, 19, 15, 14, 12, 9, 8]
})

# Calculate metrics
metrics = BiodiversityMetrics(data)

# Get all results
results = metrics.calculate_all()
print("Results as dictionary:")
print(results)

print("\n" + "="*50 + "\n")

# Or get formatted report
print(metrics.summary_report())

# Get just relative abundance
print("\nRelative Abundance:")
print(metrics.relative_abundance()[['species', 'relative_abundance']])


## ============================================
## ARCHIVO 5: data/sample_data.csv
## ============================================

species,count
American Robin,45
Song Sparrow,38
Blue Jay,28
Northern Cardinal,22
Black-capped Chickadee,19
Downy Woodpecker,15
American Crow,14
Red-winged Blackbird,12
Common Grackle,9
House Finch,8
White-breasted Nuthatch,7
Tufted Titmouse,6
Cedar Waxwing,5
American Goldfinch,4
Mourning Dove,3


## ============================================
## ARCHIVO 6: .gitignore
## ============================================

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
*.egg-info/

# Jupyter
.ipynb_checkpoints

# OS
.DS_Store
Thumbs.db

# Data
*.csv
!data/sample_data.csv
