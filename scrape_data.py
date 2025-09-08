import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_URL = "https://www.payscale.com/research"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
}

JOBS = {
    "Software_Engineer": "Software Engineer",
    "Machine_Learning_Engineer": "AI/ML Engineer",
    "Security_Analyst%2C_Cyber": "Cybersecurity Analyst"
}

COUNTRIES = {
    "US": "United States",
    "DE": "Germany",
    "IN": "India",
    "JP": "Japan",
    "CA": "Canada"
}

def get_payscale_salary(job_slug, country_code):
    url = f"{BASE_URL}/{country_code}/Job={job_slug}/Salary"
    logging.info(f"Scraping URL: {url}")
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')
        salary_element = soup.select_one('div[data-test-id="avg-sal-text"]')
        if salary_element:
            salary_text = salary_element.get_text(strip=True)
            logging.info(f"Found salary text: '{salary_text}' for {job_slug} in {country_code}")
            match = re.search(r'[\d,]+', salary_text)
            if match:
                salary_numeric_str = match.group(0).replace(',', '')
                return float(salary_numeric_str)
        logging.warning(f"Salary element not found for {job_slug} in {country_code}")
        return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed for {url}: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred for {url}: {e}")
        return None

def main():
    all_data = []
    for job_slug, job_title in JOBS.items():
        for country_code, country_name in COUNTRIES.items():
            median_salary = get_payscale_salary(job_slug, country_code)
            if median_salary:
                all_data.append({
                    "Profession": job_title,
                    "Country": country_name,
                    "Average Salary (Local Currency)": median_salary,
                    "Source": "PayScale"
                })
            else:
                logging.warning(f"Could not retrieve data for {job_title} in {country_name}. Skipping.")
            time.sleep(3)
    if not all_data:
        logging.error("No data was collected. Please check the website structure and your selectors.")
        return

    df = pd.DataFrame(all_data)
    output_filename = 'salary_data.csv'
    df.to_csv(output_filename, index=False, encoding='utf-8')
    logging.info(f"Data successfully scraped and saved to {output_filename}")
    print("\n--- Collected Data ---")
    print(df)

if __name__ == "__main__":
    main()