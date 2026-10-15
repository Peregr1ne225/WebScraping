# Web Scraping and Product Price Comparison

A graduation project that collects product information from **Advice**, **Banana IT**, and **JIB** in Thailand, stores the results in a database, and helps compare products across retailers.

## Features

- Scrapes product listings from three electronics retailers: Advice, Banana IT, and JIB.
- Collects product names, prices, stock status, brands, descriptions, product links, images, and category paths.
- Stores product, retailer, brand, category, and change-log data in a Django database.
- Updates existing products when their price, stock status, or image URL changes.
- Records changes in a log table.
- Uses fuzzy string matching to group similar products across retailers.
- Exposes product and related data through a Django REST Framework API.
- Uses Selenium with Microsoft Edge to load pages that rely on JavaScript.

## Tech stack

- **Python**
- **Django 5** and **Django REST Framework**
- **PostgreSQL** (psycopg2)
- **Selenium** and **Beautiful Soup**
- **Celery** (task-related code is included; see notes below)

## Project structure

```text
.
├── api/                       # Django models, serializers, views, and API routes
├── ScrapScripts/
│   ├── Advice.py               # Advice product scraper
│   ├── Banana.py               # Banana IT product scraper
│   ├── JIB.py                  # JIB product scraper
│   ├── SeleniumScrap.py        # Shared Selenium/browser helpers
│   ├── save_to_DB.py           # Product persistence and comparison matching
│   ├── RunAll.py               # Runs the three retailer scrapers
│   └── StringMatching.py       # Fuzzy matching experiments
├── WebScapping/                # Django project settings and URL configuration
├── manage.py
└── requirements.txt
```

## Requirements

- Python 3.10 or newer (Python 3.12 was used in the repository's compiled artifacts)
- PostgreSQL
- Microsoft Edge browser
- A compatible Microsoft Edge WebDriver available to Selenium
- Network access to the retailer websites

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Peregr1ne225/WebScraping.git
cd WebScraping
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> **Dependency note:** the current scraper code imports thefuzz, but it is not listed in requirements.txt. If installation or startup reports that module as missing, install it with pip install thefuzz. The Selenium scripts also require Microsoft Edge and a compatible Edge WebDriver.

### 4. Configure environment variables

The Django settings read database credentials and the secret key from environment variables using django-environ. Create a .env file in the repository root:

```dotenv
SECRET_KEY=replace-with-a-long-random-secret
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=127.0.0.1
DB_PORT=5432
```

Create the PostgreSQL database and user referenced by these values before continuing. Do not commit real secrets to Git.

### 5. Apply migrations and start Django

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The development server runs at http://127.0.0.1:8000/.

## API endpoints

The project registers the following Django REST Framework resources under the /api/ route:

| Resource | Endpoint |
|---|---|
| Products | /api/product/ |
| Brands | /api/brand/ |
| Categories | /api/category/ |
| Retailers | /api/retail/ |
| Change logs | /api/log/ |
| Obtain an API token | /api/api-token-auth/ |

The product view supports query parameters for filtering by product ID, similar-product group, and retailer:

- /api/product/?id=<product_id>
- /api/product/?group=<group_id>
- /api/product/?retail=<retailer_id>

Product endpoints require token authentication in the current view configuration. The other viewsets currently have no explicit permission class configured, so review and configure permissions before exposing the API publicly.

## Run the scrapers

Make sure PostgreSQL is running, the database is configured, and the browser/WebDriver prerequisites are installed. From the repository root, run an individual retailer scraper:

```bash
python ScrapScripts/Banana.py
python ScrapScripts/Advice.py
python ScrapScripts/JIB.py
```

Or run the combined script:

```bash
python ScrapScripts/RunAll.py
```

The combined script runs Banana IT, Advice, and then JIB. Scraping can take time, and the websites may change their markup or apply bot protection, so successful runs are not guaranteed. Check the generated timing/error text files when investigating a run.

## Data model overview

- **Products** — product name, price, stock, description, product URL, image URL, retailer, brand, category, and similar-product matching fields.
- **Brands** — product brand names.
- **Categories** — hierarchical product categories.
- **Retailers** — retailer information.
- **Logs** — recorded changes to tracked product attributes.

## Notes and limitations

- This is a learning/graduation project, not a production-ready scraping service.
- Retailer websites can change and may restrict automated access. Respect each website's terms and access policies.
- The repository contains a Celery configuration/task module, but the current RunAll.py executes scrapers directly; a working background-worker setup is not documented here.
- The current Django settings use DEBUG = True and an empty ALLOWED_HOSTS; review the Django deployment checklist and configure secure production settings before deployment.
- Generated Python __pycache__ files are present in the repository and generally should not be committed.

## License

No license is currently specified in this repository.
