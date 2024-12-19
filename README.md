# Dataset Information

The following large files are required but not included in the repository due to size limitations:

- `creditcard.csv` (143.84 MB)
- `creditcardfraud.zip` (65.95 MB)
- `data/Real_Estate_Sales_2001-2022_GL.csv` (119.35 MB)

## How to obtain the data
[Add instructions here for where to download these files from (e.g., Kaggle, official sources, etc.)]

## Setup instructions
1. Download the required files from the sources above
2. Place them in their respective locations in the project directory
3. Your directory structure should look like:
   ```
   project/
   ├── creditcard.csv
   ├── creditcardfraud.zip
   └── data/
       └── Real_Estate_Sales_2001-2022_GL.csv
   ```

## Ruff check
```
ruff check .
```

## Ruff format
```
ruff format .
```

uv run ruff check eda.py
uv run ruff format eda.py   