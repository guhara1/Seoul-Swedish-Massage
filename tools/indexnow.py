#!/usr/bin/env python3
"""
IndexNow + Google Sitemap Ping 일괄 색인 통보 도구
사용법: python tools/indexnow.py

- Bing / 네이버 IndexNow: 전체 URL 즉시 통보
- Google / Bing: sitemap ping
"""

import urllib.request
import urllib.error
import json
import time
import sys

# ── 설정 ─────────────────────────────────────────
HOST = "seoul-swedish-massage.pages.dev"
BASE = f"https://{HOST}"
INDEXNOW_KEY = "43a9134c37f401bc08a36d9445b9525a"
SITEMAP_URL = f"{BASE}/sitemap.xml"

# IndexNow 지원 엔진 엔드포인트
INDEXNOW_ENDPOINTS = [
    "https://api.indexnow.org/indexnow",           # Bing + 파트너 통합
    "https://searchadvisor.naver.com/indexnow",    # 네이버 직접
]

# ── URL 목록 (sitemap.xml 기반 자동 파싱) ────────
def get_urls_from_sitemap():
    import urllib.request
    import re
    try:
        with urllib.request.urlopen(SITEMAP_URL, timeout=10) as r:
            content = r.read().decode('utf-8')
        return re.findall(r'<loc>(https?://[^<]+)</loc>', content)
    except Exception as e:
        print(f"[!] sitemap 파싱 실패, 로컬 목록 사용: {e}")
        return []


def get_urls_local():
    """로컬 파일에서 URL 목록 읽기 (오프라인 fallback)"""
    import os, re
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    urls = [BASE + '/']
    seoul_dir = os.path.join(base_dir, 'seoul')
    if os.path.isdir(seoul_dir):
        for d in os.listdir(seoul_dir):
            if os.path.isfile(os.path.join(seoul_dir, d, 'index.html')):
                urls.append(f"{BASE}/seoul/{d}/")
    for extra in ['reservation/', 'precautions/', 'support/', 'hometai-guide/', 'privacy/']:
        urls.append(BASE + '/' + extra)
    return urls


# ── IndexNow 제출 ─────────────────────────────────
def submit_indexnow(urls, endpoint):
    """IndexNow API에 URL 배치 제출 (한 번에 최대 10,000개)"""
    payload = {
        "host": HOST,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE}/{INDEXNOW_KEY}.txt",
        "urlList": urls
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        endpoint,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            status = r.status
            body = r.read().decode('utf-8', errors='ignore')
            return status, body
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return 0, str(e)


# ── Sitemap Ping ─────────────────────────────────
def ping_sitemap(engine_name, ping_url):
    try:
        with urllib.request.urlopen(ping_url, timeout=15) as r:
            print(f"  ✅ {engine_name} ping 성공 (HTTP {r.status})")
    except urllib.error.HTTPError as e:
        print(f"  ⚠️  {engine_name} ping HTTP {e.code}")
    except Exception as e:
        print(f"  ❌ {engine_name} ping 실패: {e}")


# ── 메인 ─────────────────────────────────────────
def main():
    print("=" * 60)
    print("  서울 출장마사지 간다GO — 색인 통보 도구")
    print("=" * 60)

    # URL 수집
    print("\n[1] URL 목록 수집 중...")
    urls = get_urls_from_sitemap()
    if not urls:
        urls = get_urls_local()
    print(f"  총 {len(urls)}개 URL 확인")

    # ── IndexNow (Bing + 네이버) ──────────────────
    print("\n[2] IndexNow 제출 (Bing / 네이버) ...")
    CHUNK = 500  # 한 번에 500개씩 나눠서 전송
    chunks = [urls[i:i+CHUNK] for i in range(0, len(urls), CHUNK)]

    for endpoint in INDEXNOW_ENDPOINTS:
        engine = "네이버" if "naver" in endpoint else "Bing"
        ok = 0
        for i, chunk in enumerate(chunks):
            status, body = submit_indexnow(chunk, endpoint)
            if status in (200, 202):
                ok += len(chunk)
            else:
                print(f"  ⚠️  {engine} chunk {i+1} — HTTP {status}: {body[:80]}")
            if len(chunks) > 1:
                time.sleep(1)
        if ok:
            print(f"  ✅ {engine}: {ok}개 URL 통보 완료")

    # ── Sitemap Ping ──────────────────────────────
    print("\n[3] Sitemap Ping ...")
    import urllib.parse
    enc = urllib.parse.quote(SITEMAP_URL, safe='')
    ping_sitemap("Google", f"https://www.google.com/ping?sitemap={enc}")
    ping_sitemap("Bing",   f"https://www.bing.com/ping?sitemap={enc}")

    print("\n✅ 모든 색인 통보 완료!")
    print(f"   IndexNow 키: {INDEXNOW_KEY}")
    print(f"   키 파일 URL: {BASE}/{INDEXNOW_KEY}.txt")
    print(f"   Sitemap:     {SITEMAP_URL}")


if __name__ == "__main__":
    main()
