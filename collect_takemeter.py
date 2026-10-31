"""Collect public r/ItsAllAboutGames Reddit comments for CodePath TakeMeter.

Run locally: python collect_takemeter.py --file labels.csv --target 200
Appends only genuine Reddit comments; never assigns labels.
Requires public Reddit JSON endpoints to be accessible. Does not bypass blocks.
"""
import argparse
import csv
import json
import random
import shutil
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

SUB = 'ItsAllAboutGames'
BASE = 'https://www.reddit.com'
AGENT = 'TakeMeterStudentDatasetCollector/1.0 (educational; public Reddit comments)'

def get_json(url):
    req = urllib.request.Request(url, headers={'User-Agent':AGENT, 'Accept':'application/json'})
    with urllib.request.urlopen(req, timeout=25) as response:
        return json.load(response)

def read_rows(path):
    if not path.exists():
        return []
    last = None
    for enc in ('utf-8-sig', 'cp1252'):
        try:
            with path.open('r', encoding=enc, newline='') as f:
                reader=csv.DictReader(f)
                if reader.fieldnames != ['text','label','note']:
                    raise ValueError(f'Expected text,label,note, found: {reader.fieldnames!r}')
                return list(reader)
        except UnicodeDecodeError as e:
            last=e
    raise last

def collect_comments(children):
    for item in children:
        if item.get('kind') != 't1':
            continue
        data = item.get('data',{})
        yield data
        replies = data.get('replies')
        if isinstance(replies,dict):
            yield from collect_comments(replies.get('data',{}).get('children',[]))

def normalize(txt):
    return ' '.join(txt.split()).casefold()

def main():
    ap=argparse.ArgumentParser(description='Append real Reddit comments into a TakeMeter labels.csv file.')
    ap.add_argument('--file',default='labels.csv')
    ap.add_argument('--target',type=int,default=200)
    ap.add_argument('--threads',type=int,default=80, help='Maximum number of discussion threads to scan')
    ap.add_argument('--min-chars',type=int,default=15)
    args=ap.parse_args()
    path=Path(args.file)
    rows=read_rows(path)
    seen={normalize(row['text']) for row in rows if row.get('text')}
    print(f'Existing entries: {len(rows)}; target: {args.target}')
    if len(rows)>=args.target:
        print('Target already reached. No changes made.')
        return
    if path.exists():
        backup=path.with_name(path.name+'.before_collection.bak')
        shutil.copy2(path,backup)
        print(f'Backup saved: {backup}')
    # Query multiple public listing sorts to diversify discussion sources.
    ids=[]
    for sort in ['top?t=all','new','hot','controversial?t=year']:
        url=f'{BASE}/r/{SUB}/{sort}&limit=100' if '?' in sort else f'{BASE}/r/{SUB}/{sort}.json?limit=100'
        if '?' in sort:
            prefix,query=sort.split('?',1)
            url=f'{BASE}/r/{SUB}/{prefix}.json?{query}&limit=100'
        try:
            listing=get_json(url)
            for item in listing.get('data',{}).get('children',[]):
                d=item.get('data',{})
                if d.get('id') and d['id'] not in ids and d.get('subreddit','').lower()==SUB.lower():
                    ids.append(d['id'])
            print(f'Discovered {len(ids)} unique threads')
        except (urllib.error.URLError, ValueError, json.JSONDecodeError) as e:
            print(f'Could not load listing {sort}: {e}',file=sys.stderr)
        time.sleep(2)
    if not ids:
        print('Reddit listings unavailable. No new examples were invented or added.',file=sys.stderr)
        return
    added=0
    for idx,post_id in enumerate(ids[:args.threads],1):
        if len(rows)>=args.target:break
        try:
            url=f'{BASE}/r/{SUB}/comments/{post_id}.json?limit=500&sort=top&depth=6'
            payload=get_json(url)
            if not isinstance(payload,list) or len(payload)<2:continue
            thread=payload[0]['data']['children'][0]['data']
            if thread.get('subreddit','').lower()!=SUB.lower():continue
            # Collect comments only; never scrape external linked articles.
            candidates=list(collect_comments(payload[1].get('data',{}).get('children',[])))
            random.Random(post_id).shuffle(candidates)
            count=0
            for d in candidates:
                value=d.get('body','')
                if not isinstance(value,str):continue
                value=value.strip()
                if len(value)<args.min_chars or value in ('[removed]','[deleted]'):continue
                if d.get('author','').lower() in ('automoderator','reddit'):continue
                key=normalize(value)
                if not key or key in seen:continue
                rows.append({'text':value,'label':'','note':''})
                seen.add(key)
                count+=1;added+=1
                if len(rows)>=args.target:break
            print(f'Thread {idx}/{min(len(ids),args.threads)} ({post_id}): +{count}; now {len(rows)}/{args.target}')
        except (urllib.error.URLError, ValueError, KeyError, IndexError, json.JSONDecodeError) as e:
            print(f'Skipped {post_id}: {e}',file=sys.stderr)
        time.sleep(2)
    if added:
        # Atomic write; standardized UTF-8 including proper quoted multiline fields.
        temp=path.with_suffix('.tmp')
        with temp.open('w',encoding='utf-8',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=['text','label','note'],extrasaction='ignore')
            writer.writeheader();writer.writerows(rows)
        temp.replace(path)
    print(f'Finished: {len(rows)} entries, {added} added; remaining: {max(0,args.target-len(rows))}.')
    print('Manually verify source provenance and review examples before labeling.')

if __name__=='__main__':
    main()
