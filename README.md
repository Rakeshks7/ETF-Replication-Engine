# Vector Index Rebalancer 

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Vectorized-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Prototype-orange?style=for-the-badge)]()

> A real-time ETF management system that replicates index performance by minimizing tracking error through automated drift detection and rebalancing.

##  Overview

The **Vector Index Rebalancer** is a simulation of the core infrastructure used by passive asset managers (like Vanguard or BlackRock). It addresses the "Passive Investing" problem: *How do you ensure a fund's holdings perfectly match an index that changes price every millisecond?*

This engine subscribes to a live data feed, maintains an internal accounting ledger (NAV), and executes "trim" or "fill" orders when asset weights drift beyond a specified threshold (e.g., 5 basis points).

##  Key Features

* **Live NAV Calculation:** Real-time computation of Net Asset Value based on mark-to-market prices.
* **Vectorized Logic:** Utilizes `pandas` vectorization for high-speed arithmetic, avoiding slow iterative loops.
* **Smart Drift Detection:** Monitors tracking error and only triggers rebalancing when the "Drift" exceeds a configurable threshold (minimizing transaction costs).
* **Audit-Grade Logging:** Detailed transaction logs for every NAV update and order execution, suitable for fund accounting reconciliation.
* **Modular Architecture:** Decoupled strategy, execution, and data layers for production scalability.

##  Tech Stack

* **Core Logic:** Python 3.10+
* **Data Processing:** Pandas, NumPy
* **Market Simulation:** Geometric Brownian Motion (Random Walk) for price feeds
* **Logging:** Python Standard Logging (StreamHandler)

##   Logic Flow
1. Ingest: Engine receives tick data for Nifty 50 constituents.
2. Mark-to-Market: Portfolio calculates current NAV ($Price \times Quantity$).
3. Drift Check:
$$Drift_i = Weight_{Target, i} - \frac{Value_{Holding, i}}{NAV_{Total}}$$
4. Signal: If $|Drift| > 0.05\%$, generate BUY/SELL order.
5. Execute: Order fills and the internal ledger is updated.

##  Disclaimer
For Educational Purposes Only. This software is a simulation designed to demonstrate algorithmic trading and portfolio management concepts. It is not financial advice, and the "Execution" module currently mocks trade fills. Do not use this code with real capital without implementing proper risk management, API connections, and error handling.