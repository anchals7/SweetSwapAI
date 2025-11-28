## Scraper outline

1. List target cafe menu URLs inside `scrapers/targets.json`.
2. Use `requests` + `BeautifulSoup` to parse drink names, descriptions, sugar clues.
3. Save CSV output into `data/raw/{source}.csv`.
4. Use a loader script to upsert into the database via SQLAlchemy or API call.
5. Schedule via Windows Task Scheduler weekly.

