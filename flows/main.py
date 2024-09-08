from prefect import flow
from tasks.fetch_html import fetch_html_page, parse_html
from tasks.parse_seloger import create_object, insert_new
from config.database import connect_to_database

seloger_url = "https://www.seloger.com/immobilier/achat/immo-caen-14/bien-maison/?projects=2&types=2&places=[{%22inseeCodes%22:[140118]}]&sort=d_dt_crea&mandatorycommodities=0&enterprise=0&qsVersion=1.0&m=search_refine-redirection-search_results"


@flow(retries=3, retry_delay_seconds=5, log_prints=True)
def parse_seloger_flow():
    table_name = 'houses'
    source_name = 'seloger.com'
    engine = connect_to_database('eruditio')
    page = fetch_html_page(seloger_url)
    contents = parse_html(
        page,  'div', {'data-testid': 'sl.explore.card-container'})
    houses = create_object(contents)
    rows = insert_new(engine, houses)
    print(f"Found {len(contents)} houses from \"{source_name}\".")
    print(f"{rows} new rows in {table_name}.")


if __name__ == "__main__":
    parse_seloger_flow.serve(
        name="parse-seloger-deployment",
        cron="0 */2 * * *",
        tags=["parse", "db"],
        description="Parsing seloger.com and load data in database.",
        version="eruditio/deployments",
    )
