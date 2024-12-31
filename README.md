# Dataset Information

The following large files are required but not included in the repository due to size limitations:

- `creditcard.csv` (143.84 MB)
- `creditcardfraud.zip` (65.95 MB)
- `data/Real_Estate_Sales_2001-2022_GL.csv` (119.35 MB)

## How to obtain the data
[Add instructions here for where to download these files from (e.g., Kaggle, official sources, etc.)]

## How to add dependencies
```
uv add python-dotenv
uv add requests-toolbelt
uv add requests
uv add gql
uv add wordcloud
uv add matplotlib
uv add pandas
uv add scikit-learn
uv add notebook
uv add jupyter
uv add seaborn
```
### How to run the analysis python file
```
uv run analysis.py
```

### How to run the eda python file
```
uv run eda.py
```

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