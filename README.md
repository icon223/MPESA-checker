# 💸 MPESA Checker — Expense Tracker & Refund Monitor

A lightweight web dashboard for tracking M-PESA transactions, recurring subscriptions, and pending refunds. Paste in raw M-PESA SMS/email alerts and it parses them into structured transaction records automatically.

[![Alpine.js](https://img.shields.io/badge/Alpine.js-8BC0D0?logo=alpine.js&logoColor=black)](https://alpinejs.dev)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-38B2AC?logo=tailwind-css&logoColor=white)](https://tailwindcss.com)
[![GitHub Pages](https://img.shields.io/badge/Hosted%20on-GitHub%20Pages-222?logo=github)](https://pages.github.com)

---

## Table of Contents

- [About](#about)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Usage](#usage)
- [License](#license)

---

## About

MPESA Checker gives you a single dashboard for your M-PESA money movement — debits, credits, active subscriptions, and refunds you're chasing — without needing to dig through SMS alerts one by one. Paste an alert in and it's parsed and logged; the dashboard keeps a running summary of your balances and upcoming subscription charges.

This is the frontend, a static single-page app served via GitHub Pages (`gh-pages` branch). It talks to a backend API for auth, parsing, and data storage.

## Key Features

- 🔐 **Authentication** — username/password login and registration, plus Google Sign-In.
- 📊 **Summary Dashboard** — total transactions, debits, credits, pending refunds, and a 30-day subscription runway at a glance.
- 📄 **Transaction Log** — searchable, filterable table (by merchant/reference, direction, and status).
- 🔁 **Subscription Tracking** — add recurring charges with amount, currency, billing day, and FX rate to KES; see what's due in the next 30 days.
- 💰 **Refund Watchlist** — track pending refunds and their expected settlement dates.
- 🧾 **Alert Parsing** — paste a raw M-PESA SMS/email alert to preview how it parses, or ingest it directly into the transaction log.

## Tech Stack

- **Alpine.js** — lightweight reactive UI
- **Tailwind CSS** (via CDN) — styling
- **Lucide Icons** — iconography
- **Google Identity Services** — Google Sign-In
- Static frontend hosted on **GitHub Pages**; backend API (auth, parsing, storage) required separately

## Getting Started

This repo is the frontend only — it's a single static `index.html` with no build step.

### Run locally

```sh
git clone https://github.com/icon223/MPESA-checker.git
cd MPESA-checker
# then just open index.html in a browser, or serve it:
npx serve .
```

### Backend

The dashboard expects a backend API for auth, transaction storage, and alert parsing. By default it points at:

```js
API_URL: 'http://127.0.0.1:8000'
```

Update `API_URL` in `index.html` to point at your deployed backend before using this outside of local development.

## Configuration

| Setting | Where | Notes |
|---|---|---|
| `API_URL` | `index.html` (top of the `appState()` script) | Base URL of the backend API |
| Google Sign-In client | `index.html` `<head>` | Requires a Google OAuth client ID for the Google Sign-In button to work |

## Usage

1. Sign in (or use the demo account, if enabled on your backend) or sign up.
2. **Transactions** — browse and filter your parsed transaction history.
3. **Subscriptions** — add recurring charges to track upcoming billing and runway.
4. **Refunds** — monitor refunds you're waiting on.
5. **Parse Alert** — paste an M-PESA alert to preview the parsed fields before saving.
6. **Ingest Alert** — paste an alert to parse and save it directly to your transaction log.

## License

Add your chosen license here (e.g. MIT) and include a `LICENSE` file in the repo root.
