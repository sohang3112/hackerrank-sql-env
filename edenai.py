import pandas as pd
import requests

api_key = None

# NOTE: using microsoft only - seems to be cheaper & more accurate than google
provider = "microsoft"

# TODO: use sqlite db to avoid repeated api calls for same image url
def table_from_image(image_url: str) -> pd.DataFrame:
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "providers": provider,         
        "language": "en",
        "file_url": image_url
    }
    response = requests.post("https://api.edenai.run/v2/ocr/ocr_tables_async",
                             json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()

    table = data['results']['microsoft']['pages'][0]['tables'][0]
    grid = [
        [cell['text'] for cell in row['cells']]
        for row in table['rows']
    ]
    return pd.DataFrame(grid[1:], columns=grid[0])