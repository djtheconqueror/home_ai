# BioSentinel v1

BioSentinel is an early-stage machine learning project for biosignal risk classification and explainable threat scoring.

## Overview

This project uses synthetic signal features to train a Random Forest classifier that estimates whether a given biosignal profile should be treated as a potential threat.

## Features

The current model uses five normalized signal variables:

- persistence
- volatility
- detection_confidence
- toxicity_index
- anomaly_score

## Current Capabilities

- Synthetic biosignal dataset generation
- Random Forest classification model
- Threat probability scoring
- Risk level categorization
- AI-style explanation outputs
- Scenario testing
- Feature importance visualization
- ROC-AUC evaluation
- Executive summary reporting

## Current Files

- `BioSentinel_v1.ipynb` — main Colab notebook
- `biosentinel_rf.pkl` — saved model artifact, if uploaded
- `biosentinel_scenario_report.csv` — scenario output report, if uploaded

## Next Steps

- Build a Streamlit dashboard
- Add richer synthetic and public datasets
- Add model comparison
- Improve explainability
- Add time-series sensor simulation
- Package as a deployable demo
