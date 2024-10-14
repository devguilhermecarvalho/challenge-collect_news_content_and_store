from src.datasources.the_guardian_scraper import TheGuardianScraper

class ScraperFactory:

    # Method that returns a scraper with the font name.
    def get_scraper(self, source_name):
        if source_name == "the_guardian":
            return TheGuardianScraper()
        
        raise ValueError(f"Scraper for {source_name} not found")