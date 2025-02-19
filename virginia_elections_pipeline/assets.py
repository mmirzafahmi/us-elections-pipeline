import os
import time
import glob
import dagster as dg
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup, SoupStrainer
from sqlalchemy import create_engine, text
from datetime import datetime
from selenium.webdriver.chrome.options import Options


BASE_URL = os.getenv('URL')
FULL_URL = BASE_URL + os.getenv('END_POINT')
USER_AGENT = os.getenv('USER_AGENT')
DOWNLOAD_DIR = os.getcwd() + '\\data'


@dg.asset(
        group_name='extraction', 
        automation_condition=dg.AutomationCondition.eager()
)
def get_data() -> dg.MaterializeResult:

    def get_browser():

        user_agent = USER_AGENT
        default_dir = DOWNLOAD_DIR + '\\new'
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument(f'user-agent={user_agent}')
        options.add_experimental_option("prefs", {
            "download.default_directory": default_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        browser = webdriver.Chrome(options=options)
        return browser

    def getLinks(browser, url):

        browser.get(url)
        html_page = browser.page_source
        links = []

        for link in BeautifulSoup(html_page, "html.parser", parse_only=SoupStrainer('a')):
            if link.has_attr('href') and '2025' in link.get('href'):
                links.append(BASE_URL + link.get('href'))
        return links


    browser = get_browser()
    anchors = getLinks(
        browser=browser, 
        url=FULL_URL
    )
    downloadables = DOWNLOAD_DIR + '\\new'

    for anchor in anchors:
        
        browser = get_browser()
        browser.get(anchor)
        html_page = browser.page_source
        date = anchor.split('/')[-2]

        for link in BeautifulSoup(html_page, "html.parser", parse_only=SoupStrainer('a')):

            if link.has_attr('href') and 'ScheduleA.csv' in link.get('href'):
                download_link = f"{BASE_URL}{link.get('href')}"
                browser.get(download_link)

        old = downloadables + '\\ScheduleA.csv'
        new = downloadables + f'\\{date}_ScheduleA.csv'

        seconds = 0
        while seconds < 30:

            if os.path.exists(old):
                
                os.rename(old, new)
                print("Download Complete.")
                break

            else:
                time.sleep(1)
                seconds += 1
    
    df = pd.concat(
        [pd.read_csv(csv, encoding = "ISO-8859-1") for csv in glob.glob(downloadables + '\\*.csv')]
    )

    return dg.MaterializeResult(
        metadata={
                "row_count": dg.MetadataValue.int(len(df)),
                "preview": dg.MetadataValue.md(df.to_markdown(index=False)),
            }
        )


@dg.asset(
        deps=[get_data], 
        group_name='ingestion',
        automation_condition=dg.AutomationCondition.eager()
)
def ingest_to_dwh() -> dg.MaterializeResult:
    
    dwh = create_engine(os.getenv('CONN_STRING'))

    csvs = glob.glob(DOWNLOAD_DIR + '\\new\\*.csv')
    archived = DOWNLOAD_DIR + '\\archived\\'
    for csv in csvs:
        
        file_name = csv.split('\\')[-1]
        df = pd.read_csv(csv, encoding = "ISO-8859-1")
        
        df['CommitteeContactId'] = df['CommitteeContactId'].astype('Int64')
        df['TransactionDate'] = df['TransactionDate'].apply(lambda r: datetime.strptime(r, '%m/%d/%Y'))

        df.to_sql(name='schedule_a', con=dwh, index=False, if_exists='append')

        if not os.path.exists(archived + file_name):
            os.rename(csv, archived + file_name)
        else:
            os.remove(csv)
    
    with dwh.connect() as conn:
        row_count = conn.execute(
            text(
                """
                SELECT COUNT(*)
                FROM default.schedule_a
                """
            )
        ).fetchall()
        
        count = row_count[0][0] if row_count else 0

        return dg.MaterializeResult(
            metadata={
                "row_count": dg.MetadataValue.int(count)
            }
        )


