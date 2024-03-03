import aiohttp
import asyncio
import time
import requests
import json


def url_scanner(url):
    async def submit_url_for_scan(url, api_key):
        headers = {
            "Content-Type": "application/json",
            "API-Key": api_key
        }
        payload = {
            "url": url,
            "visibility": "public",
            "tags": ["example"]
        }
        async with aiohttp.ClientSession() as session:
            async with session.post("https://urlscan.io/api/v1/scan/", headers=headers, json=payload) as response:
                data = await response.json()
                return data

    async def get_scan_results(scan_id, api_key):
        headers = {
            "API-Key": api_key
        }
        url = f"https://urlscan.io/api/v1/result/{scan_id}/"
        async with aiohttp.ClientSession() as session:
            while True:
                async with session.get(url, headers=headers) as response:
                    data = await response.json()
                    if data.get("status") != 404:
                        return data
                    else:
                        print(
                            "Scan still in progress. Waiting 5 seconds before checking again...")
                        await asyncio.sleep(5)

    # Example usage
    api_key = ""
    url = input

    async def main():
        scan_data = await submit_url_for_scan(url, api_key)
        if scan_data:
            scan_id = scan_data["uuid"]
            print("Scan submitted successfully. Scan ID:", scan_id)
            scan_results = await get_scan_results(scan_id, api_key)
            if scan_results:
                data = scan_results
                results = {

                    "links": data["data"]["links"],
                    "pages": data["page"]

                }
                return results

    asyncio.run(main())
