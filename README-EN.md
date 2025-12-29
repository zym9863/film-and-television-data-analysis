[中文](README.md) | **English**

# Film and Television Data Analysis System

A comprehensive analysis system based on the TMDB 5000 movie dataset, offering ROI analysis, box-office prediction models, and interactive data visualizations.

## Project Overview

This project performs in-depth analysis on the TMDB 5000 movie dataset, leveraging various data analysis techniques and machine learning models to explore investment return patterns, genre distribution characteristics, temporal trends, and box-office prediction models.

### Main Features

- 📊 **ROI Analysis** - Analyze returns by genre and budget ranges
- 📈 **Time Trend Analysis** - Annual production, budget, and box-office trends, plus monthly release patterns
- 🎬 **Genre Analysis** - Box-office distribution and ROI per genre
- 🎭 **Directors / Actors Analysis** - Top directors and actors box-office performance
- 🏢 **Production Company Analysis** - Market share of major production companies
- 🤖 **Box-Office Prediction Models** - Machine learning-based box-office prediction
- 📉 **Interactive Visualizations** - D3.js charts for various analysis results

## Tech Stack

| Layer | Technology | Notes |
|------|-----------|------|
| Backend | Python 3.12 + FastAPI | RESTful API service |
| Data Analysis | Pandas, NumPy | Data processing and statistics |
| Machine Learning | Scikit-learn | Box-office prediction models |
| Front-end Framework | Svelte 5 + TypeScript | Reactive UI |
| Visualization | D3.js | Interactive charts |
| Build Tools | Vite + pnpm | Modern build |
| Package Management | uv (Python), pnpm (Node) | Dependency management |

## Project Structure

```
film and television data analysis/
├── analysis/              # Data analysis modules
│   ├── data_loader.py    # Data loading and preprocessing
│   ├── analyzer.py       # Data analysis logic
│   └── predictor.py      # Box-office prediction models
├── api/                   # FastAPI backend
│   └── app.py            # API route definitions
├── visualization/         # Svelte front-end
│   ├── src/
│   │   ├── pages/        # Page components
│   │   ├── lib/
│   │   │   ├── charts/   # D3.js chart components
│   │   │   ├── components/ # UI components
│   │   │   └── api/      # API wrappers
│   │   └── utils/        # Utility functions
│   └── package.json
├── data/                  # Data files
│   └── raw/              # TMDB datasets
│       ├── tmdb_5000_movies.csv
│       └── tmdb_5000_credits.csv
├── docs/                  # Documentation
│   ├── Step1-数据源说明.md
│   └── Step2-影视数据分析报告.md
├── main.py               # Backend service entry
└── pyproject.toml        # Python project configuration
```

## Quick Start

### Requirements

- Python >= 3.12
- Node.js >= 18
- pnpm >= 8
- uv (Python package manager)

### Install Dependencies

**Backend:**
```bash
uv sync
```

**Frontend:**
```bash
cd visualization
pnpm install
```

### Run the Project

**Start backend service:**
```bash
uv run python main.py
```
The service runs at http://localhost:8000

**Start front-end dev server:**
```bash
cd visualization
pnpm dev
```
The front-end is available at http://localhost:5173

### API Documentation

After starting the backend service, visit http://localhost:8000/docs to view the Swagger API documentation.

## API Endpoints

| Endpoint | Method | Description |
|---------|--------|-------------|
| `/` | GET | Root endpoint |
| `/api/overview` | GET | Dataset overview |
| `/api/roi` | GET | ROI analysis results |
| `/api/genres` | GET | Genre analysis |
| `/api/trends` | GET | Time trend analysis |
| `/api/directors` | GET | Director analysis |
| `/api/actors` | GET | Actor analysis |
| `/api/companies` | GET | Production company analysis |
| `/api/correlations` | GET | Correlation analysis |
| `/api/scatter` | GET | Scatter plot data |
| `/api/prediction/train` | GET | Train prediction model |
| `/api/prediction/insights` | GET | Prediction model insights |
| `/api/prediction/predict` | POST | Predict box-office |

## License

MIT License
