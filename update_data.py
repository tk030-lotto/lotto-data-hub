import os
import sys
import json
import re
import time
import requests
import io
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DATA_UPDATER")

# 各種くじのCSVデータ元URL定義
LOTTERY_CSV_URLS = {
    'loto6': 'https://loto-life.net/csv/loto6',
    'loto7': 'https://loto-life.net/csv/loto7',
    'miniloto':  'https://loto-life.net/csv/mini',
    'numbers3': 'https://loto-life.net/csv/numbers3',
    'numbers4': 'https://loto-life.net/csv/numbers4',
    'bingo5': 'https://loto-life.net/csv/bingo5'
}

def clean_val(val):
    if not isinstance(val, str):
        return val
    s = val.strip()
    match = re.search(r'="(.+?)"', s)
    if match:
        return match.group(1)
    return s.strip('"')

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    return df.map(clean_val)

def fetch_and_parse_csv(game_key, url):
    logger.info(f"Downloading CSV for {game_key} from {url}...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    max_retries = 3
    retry_delay = 30
    
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            break
        except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
            if attempt == max_retries:
                raise e
            logger.warning(f"Attempt {attempt} failed: {e}. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            
    csv_bytes = response.content
    decoded_text = None
    for enc in ('cp932', 'utf-8', 'utf-8-sig'):
        try:
            decoded_text = csv_bytes.decode(enc)
            break
        except UnicodeDecodeError:
            continue
            
    if not decoded_text:
        raise ValueError(f"Failed to decode CSV bytes for {game_key}")
        
    df = pd.read_csv(io.StringIO(decoded_text.strip()))
    df.columns = [clean_val(c) if isinstance(c, str) else c for c in df.columns]
    df = clean_data(df)
    
    parsed_history = []
    
    if game_key == 'bingo5':
        # ビンゴ5のCSV解析ロジック
        for _, row in df.iterrows():
            try:
                round_no = int(row.iloc[0])
                date_str = str(row.iloc[1]).strip()
                numbers = [int(row.iloc[col]) for col in range(2, 10)]
                
                if len(numbers) != 8:
                    continue
                
                # 数字の妥当性チェック (各枠の範囲チェック)
                valid = True
                for i, num in enumerate(numbers):
                    lo = i * 5 + 1
                    hi = i * 5 + 5
                    if not (lo <= num <= hi):
                        valid = False
                        break
                if not valid:
                    continue
                    
                parsed_history.append({
                    "round": round_no,
                    "date": date_str,
                    "numbers": numbers,
                    "bonus": []
                })
            except Exception:
                continue
    else:
        # ロト・ナンバーズのCSV解析ロジック
        pick_counts = {
            'loto6': 6,
            'loto7': 7,
            'miniloto': 5,
            'numbers3': 3,
            'numbers4': 4
        }
        pick_count = pick_counts[game_key]
        is_numbers = game_key.startswith('numbers')
        
        for _, row in df.iterrows():
            try:
                round_no = int(row['開催回'])
                date_str = str(row['開催日']).strip()
                
                if is_numbers:
                    target_col = '抽選数字' if '抽選数字' in row else df.columns[2]
                    num_str = str(row[target_col]).strip()
                    num_str = re.sub(r'\D', '', num_str)
                    numbers = [int(d) for d in num_str]
                    bonus = []
                else:
                    numbers = []
                    for i in range(1, pick_count + 1):
                        numbers.append(int(row[f'第{i}数字']))
                    
                    bonus = []
                    if game_key == 'loto7':
                        bonus = [int(row['ボーナス数字1']), int(row['ボーナス数字2'])]
                    else:
                        bonus = [int(row['ボーナス数字'])]
                
                parsed_history.append({
                    "round": round_no,
                    "date": date_str,
                    "numbers": numbers,
                    "bonus": bonus
                })
            except Exception:
                continue
                
    parsed_history.sort(key=lambda x: x['round'], reverse=True)
    return parsed_history

def main():
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    
    success_count = 0
    
    for game_key, url in LOTTERY_CSV_URLS.items():
        try:
            history = fetch_and_parse_csv(game_key, url)
            if not history:
                logger.error(f"No parsed data for {game_key}")
                continue
                
            file_path = os.path.join(data_dir, f"{game_key}.json")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
                
            logger.info(f"Successfully updated {file_path}. Latest round: {history[0]['round']}")
            success_count += 1
        except Exception as e:
            logger.error(f"Error updating {game_key}: {e}")
            
    if success_count == len(LOTTERY_CSV_URLS):
        logger.info("All lottery data files updated successfully.")
        sys.exit(0)
    else:
        logger.warning(f"Some updates failed. Successful: {success_count}/{len(LOTTERY_CSV_URLS)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
