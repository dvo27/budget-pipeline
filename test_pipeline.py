from src.ingestion.parsers import chase, discover, wells_fargo
from src.warehouse.loader import Loader
from config import RAW_CHASE, RAW_WELLS_FARGO, RAW_DISCOVER

if __name__ == "__main__":
    # instantiate
    LoaderClass = Loader()
    WF_Parser = wells_fargo.WellsFargoParser()
    ChaseParser = chase.ChaseParser()
    DiscoverParser = discover.DiscoverParser()
    LoaderClass.init_warehouse()
    
    parsed_wf = WF_Parser.parse(RAW_WELLS_FARGO / 'Checking1.csv')
    parsed_chase = ChaseParser.parse(RAW_CHASE / 'Chase4165_Activity20260101_20260317_20260317.CSV')
    parsed_discover = DiscoverParser.parse(RAW_DISCOVER / 'Discover-Last12Months-20260317.csv')
    
    print(parsed_wf.columns.tolist())
    print(len(parsed_wf.columns))
    
    # load each parsed df
    LoaderClass.load_transactions(parsed_wf)
    LoaderClass.load_transactions(parsed_chase)
    LoaderClass.load_transactions(parsed_discover)
    
    LoaderClass.get_connection().sql('SELECT source_bank, COUNT(*) FROM raw.transactions GROUP BY source_bank')
