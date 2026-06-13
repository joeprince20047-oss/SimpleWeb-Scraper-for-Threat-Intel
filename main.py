# main.py - CLI Scraper Orchestrator (Entry Point)
# Provides flexible command line options supporting complete flow.

import argparse
import sys
import os

import config
import fetcher
import parser
import validator
import storage

def scrape_single_feed(feed_name, output_dir, file_format):
    if feed_name not in config.FEEDS:
        print(f"[!] Error: Specified feed '{feed_name}' is not defined in config FEEDS.")
        return False
        
    url = config.FEEDS[feed_name]
    print(f"[*] Initiating scrape of feed: {feed_name}")
    print(f"[*] Downloading: {url}")
    
    try:
        raw_data = fetcher.fetch_feed(url)
        print(f"[*] Received raw download containing {len(raw_data)} chars.")
        
        # Parse and Extract
        extracted_iocs = parser.extract_iocs(raw_data)
        
        # Validate and Deduplicate
        clean_iocs = validator.validate_iocs(extracted_iocs)
        
        # Write Output
        filename = f"iocs_{feed_name}.{file_format}"
        out_path = os.path.join(output_dir, filename)
        
        if file_format == "json":
            storage.save_json(clean_iocs, feed_name, out_path)
        elif file_format == "csv":
            storage.save_csv(clean_iocs, out_path)
        else:
            storage.save_txt(clean_iocs, out_path)
            
        return True
    except Exception as e:
        print(f"[!] Pipeline Error executing '{feed_name}': {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Simple Threat Intelligence Web Scraper & Collector CLI Console."
    )
    parser.add_argument(
        "--feed",
        default="urlhaus",
        choices=list(config.FEEDS.keys()),
        help="Target threat intelligence feed to scrape."
    )
    parser.add_argument(
        "--format",
        default=config.DEFAULT_FORMAT,
        choices=["json", "csv", "txt"],
        help="Desired serialization format saving output files."
    )
    parser.add_argument(
        "--output",
        default=config.OUTPUT_DIR,
        help="Local subdirectory path where output files are written."
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Runs scrape sequence covering ALL configured feeds sequentially."
    )
    
    args = parser.parse_args()
    
    if args.all:
        print("[*] Initiating scraping cycle across ALL configured sources:")
        success_count = 0
        for name in config.FEEDS.keys():
            if scrape_single_feed(name, args.output, args.format):
                success_count += 1
        print(f"[*] Cycle finished. Scraped {success_count}/{len(config.FEEDS)} feeds successfully.")
    else:
        scrape_single_feed(args.feed, args.output, args.format)

if __name__ == "__main__":
    main()
