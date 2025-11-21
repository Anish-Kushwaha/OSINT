#!/usr/bin/env python3
"""
Social Media Finder OSINT Tool
Finds social media accounts linked to phone numbers
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import quote_plus, urlencode
import phonenumbers
from phonenumbers import carrier, geocoder
import argparse

# =====================================================
# BANNER FUNCTION
# =====================================================

def banner():
    print(r"""
    █████╗ ███╗   ██╗██╗██╗  ██╗██╗  ██╗
   ██╔══██╗████╗  ██║██║██║ ██╔╝██║ ██╔╝
   ███████║██╔██╗ ██║██║█████╔╝ █████╔╝ 
   ██╔══██║██║╚██╗██║██║██╔═██╗ ██╔═██╗ 
   ██║  ██║██║ ╚████║██║██║  ██╗██║  ██╗
   ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝

       🗣  𝔸ℕ𝕀𝕊ℍ - 𝕂𝕌𝕊ℍ𝕎𝔸ℍ𝔸 ❤️‍🔥
       SOCIAL MEDIA FINDER OSINT TOOL
       Version: OSINT v2.2
       Website : Anish-kushwaha.b12sites.com
       Email   : Anish_Kushwaha@proton.me
    """)

# =====================================================
# CONFIGURATION
# =====================================================

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

# =====================================================
# SOCIAL MEDIA SEARCH FUNCTIONS
# =====================================================

def search_facebook(phone_number):
    """Search for Facebook account using phone number"""
    results = []
    try:
        url = f"https://www.facebook.com/login/identify/?ctx=recover&phone={quote_plus(phone_number)}"
        response = requests.get(url, headers=HEADERS, timeout=10)

        if "find your account" in response.text.lower():
            soup = BeautifulSoup(response.text, 'html.parser')
            account_elements = soup.find_all(text=re.compile(r'account', re.I))
            if account_elements:
                results.append({
                    'platform': 'Facebook',
                    'method': 'Account Recovery',
                    'found': True,
                    'url': url,
                    'details': 'Account exists - visible in recovery flow'
                })

        search_url = f"https://www.facebook.com/public?query={quote_plus(phone_number)}"
        response = requests.get(search_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        profile_links = soup.find_all('a', href=re.compile(r'/facebook.com/[\w\.]+'))
        for link in profile_links[:5]:
            profile_url = link.get('href', '')
            if profile_url:
                results.append({
                    'platform': 'Facebook',
                    'method': 'Public Search',
                    'found': True,
                    'url': profile_url,
                    'username': profile_url.split('/')[-1],
                    'details': 'Potential profile found in public search'
                })

    except Exception as e:
        results.append({'platform': 'Facebook','found': False,'error': str(e)})

    return results

# -- ALL OTHER SEARCH FUNCTIONS (INSTAGRAM, LINKEDIN, TWITTER, TELEGRAM, WHATSAPP, DIRECTORIES, GITHUB) --
# (YOUR CODE IS KEPT SAME, NO CHANGE)
# ---------------------------------------------------------
# I am NOT removing or modifying your logic, so below is EXACTLY your code.
# ---------------------------------------------------------

def search_instagram(phone_number):
    results = []
    try:
        url = "https://www.instagram.com/accounts/account_recovery/"
        requests.get(url, headers=HEADERS, timeout=10)

        search_patterns = [
            f"site:instagram.com {phone_number}",
            f'"instagram.com" "{phone_number}"',
            f"inurl:instagram.com {phone_number}"
        ]

        for pattern in search_patterns:
            try:
                search_url = f"https://www.google.com/search?q={quote_plus(pattern)}"
                response = requests.get(search_url, headers=HEADERS, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')

                instagram_links = soup.find_all('a', href=re.compile(r'instagram\.com/[\w\._]+'))
                for link in instagram_links:
                    profile_url = link.get('href', '')
                    username = profile_url.split('/')[-1].split('?')[0]
                    results.append({
                        'platform': 'Instagram',
                        'method': 'Google Search',
                        'found': True,
                        'url': f"https://instagram.com/{username}",
                        'username': username,
                        'details': f'Found via search: {pattern}'
                    })
                time.sleep(2)
            except:
                continue
    except Exception as e:
        results.append({'platform': 'Instagram','found': False,'error': str(e)})

    return results


def search_linkedin(phone_number):
    results = []
    try:
        patterns = [
            f'site:linkedin.com "{phone_number}"',
            f'phone {phone_number} "linkedin"',
            f'"linkedin.com/in" "{phone_number}"'
        ]

        for pattern in patterns:
            search_url = f"https://www.google.com/search?q={quote_plus(pattern)}"
            response = requests.get(search_url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            linkedin_links = soup.find_all('a', href=re.compile(r'linkedin\.com/in/[\w\-]+'))
            for link in linkedin_links:
                profile_url = link.get('href', '')
                profile_id = profile_url.split('/in/')[-1].split('?')[0]
                results.append({
                    'platform': 'LinkedIn',
                    'method': 'Google Search',
                    'found': True,
                    'url': f"https://linkedin.com/in/{profile_id}",
                    'profile_id': profile_id,
                    'details': f'Found via: {pattern}'
                })
            time.sleep(2)

    except Exception as e:
        results.append({'platform': 'LinkedIn','found': False,'error': str(e)})

    return results


def search_twitter(phone_number):
    results = []
    try:
        patterns = [
            f'site:twitter.com "{phone_number}"',
            f'"twitter.com" "{phone_number}"',
            f'phone {phone_number} twitter'
        ]

        for pattern in patterns:
            search_url = f"https://www.google.com/search?q={quote_plus(pattern)}"
            response = requests.get(search_url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            twitter_links = soup.find_all('a', href=re.compile(r'twitter\.com/[\w_]+'))
            for link in twitter_links:
                profile_url = link.get('href', '')
                if '/status/' in profile_url:
                    continue
                username = profile_url.split('twitter.com/')[-1].split('?')[0]
                results.append({
                    'platform': 'Twitter',
                    'method': 'Google Search',
                    'found': True,
                    'url': f"https://twitter.com/{username}",
                    'username': username,
                    'details': f'Found via: {pattern}'
                })
            time.sleep(2)

    except Exception as e:
        results.append({'platform': 'Twitter','found': False,'error': str(e)})

    return results


def search_telegram(phone_number):
    results = []
    try:
        clean = re.sub(r'[^\d+]', '', phone_number)
        patterns = [
            f'site:t.me "{clean}"',
            f'"t.me" "{clean}"',
            f'telegram {clean}'
        ]

        for pattern in patterns:
            search_url = f"https://www.google.com/search?q={quote_plus(pattern)}"
            response = requests.get(search_url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            telegram_links = soup.find_all('a', href=re.compile(r't\.me/[\w_]+'))
            for link in telegram_links:
                profile_url = link.get('href', '')
                username = profile_url.split('t.me/')[-1].split('?')[0]
                results.append({
                    'platform': 'Telegram',
                    'method': 'Google Search',
                    'found': True,
                    'url': f"https://t.me/{username}",
                    'username': username,
                    'details': 'Potential Telegram account'
                })
            time.sleep(2)

    except Exception as e:
        results.append({'platform': 'Telegram','found': False,'error': str(e)})

    return results


def search_whatsapp(phone_number):
    results = []
    clean = re.sub(r'[^\d+]', '', phone_number)
    try:
        results.append({
            'platform': 'WhatsApp',
            'method': 'Direct Link',
            'found': True,
            'url': f"https://wa.me/{clean}",
            'details': 'WhatsApp contact link'
        })
    except Exception as e:
        results.append({'platform': 'WhatsApp','found': False,'error': str(e)})
    return results


def search_truecaller_like(phone_number):
    results = []
    try:
        patterns = [
            f'{phone_number} "truecaller"',
            f'{phone_number} "caller id"',
            f'{phone_number} "phone directory"'
        ]

        for pattern in patterns:
            search_url = f"https://www.google.com/search?q={quote_plus(pattern)}"
            response = requests.get(search_url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            directory_sites = ['truecaller', 'callapp', 'whitepages', 'callerid']
            links = soup.find_all('a')

            for link in links:
                href = link.get('href', '')
                text = link.get_text().lower()
                if any(site in href.lower() for site in directory_sites):
                    results.append({
                        'platform': 'Phone Directory',
                        'method': 'Directory Search',
                        'found': True,
                        'url': href,
                        'details': f'Listed in directory: {text[:50]}...'
                    })
            time.sleep(2)

    except Exception as e:
        results.append({'platform': 'Phone Directory','found': False,'error': str(e)})

    return results


def search_github(phone_number):
    results = []
    try:
        patterns = [
            f'site:github.com "{phone_number}"',
            f'"github.com" "{phone_number}"'
        ]

        for pattern in patterns:
            search_url = f"https://www.google.com/search?q={quote_plus(pattern)}"
            response = requests.get(search_url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            github_links = soup.find_all('a', href=re.compile(r'github\.com/[\w\-]+'))
            for link in github_links:
                profile_url = link.get('href', '')
                username = profile_url.split('github.com/')[-1].split('?')[0]
                results.append({
                    'platform': 'GitHub',
                    'method': 'Google Search',
                    'found': True,
                    'url': f"https://github.com/{username}",
                    'username': username,
                    'details': f'Found via: {pattern}'
                })
            time.sleep(2)

    except Exception as e:
        results.append({'platform': 'GitHub','found': False,'error': str(e)})

    return results

# =====================================================
# MASTER SEARCH FUNCTION
# =====================================================

def comprehensive_social_search(phone_number):
    all_results = []

    print(f"\n🔍 Starting social media search for: {phone_number}")
    print("="*60)

    search_functions = [
        ('Facebook', search_facebook),
        ('Instagram', search_instagram),
        ('LinkedIn', search_linkedin),
        ('Twitter', search_twitter),
        ('Telegram', search_telegram),
        ('WhatsApp', search_whatsapp),
        ('GitHub', search_github),
        ('Phone Directories', search_truecaller_like),
    ]

    for name, func in search_functions:
        print(f"📱 Searching {name}...")
        try:
            results = func(phone_number)
            all_results.extend(results)

            found = [r for r in results if r.get('found')]
            if found:
                for r in found:
                    print(f"   ✅ FOUND: {r['url']}")
            else:
                print(f"   ❌ Not found on {name}")

            time.sleep(3)

        except Exception as e:
            print(f"   ⚠️ Error searching {name}: {e}")

    return all_results

# =====================================================
# PHONE NUMBER PARSING
# =====================================================

def parse_phone_number(phone_input, country_code=None):
    try:
        parsed = phonenumbers.parse(phone_input, country_code) if country_code else phonenumbers.parse(phone_input)

        if phonenumbers.is_valid_number(parsed):
            return {
                'e164': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164),
                'national': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL),
                'international': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                'country_code': parsed.country_code,
                'carrier': carrier.name_for_number(parsed, "en"),
                'region': geocoder.description_for_number(parsed, "en"),
                'valid': True
            }
        else:
            return {'valid': False, 'error': 'Invalid phone number'}

    except Exception as e:
        return {'valid': False, 'error': str(e)}

# =====================================================
# DISPLAY RESULTS
# =====================================================

def display_results(all_results, phone_info):
    print("\n" + "="*70)
    print("🎯 SOCIAL MEDIA OSINT REPORT")
    print("="*70)

    print(f"\n📞 TARGET: {phone_info['international']}")
    print(f"📍 REGION: {phone_info.get('region', 'Unknown')}")
    print(f"📡 CARRIER: {phone_info.get('carrier', 'Unknown')}")

    successful = [r for r in all_results if r.get('found')]

    print(f"\n📊 SEARCH SUMMARY:")
    print(f"   ✅ Accounts Found: {len(successful)}")
    print(f"   🔍 Platforms Checked: 8")

    if successful:
        print("\n🎉 SOCIAL MEDIA ACCOUNTS FOUND:")
        print("-" * 50)

        for r in successful:
            print(f"\n📱 {r['platform']}:")
            print(f"   👤 Username/ID: {r.get('username') or r.get('profile_id', 'Direct Link')}")
            print(f"   🔗 Direct Link: {r['url']}")
            print(f"   🎯 Method: {r['method']}")
            if r.get('details'):
                print(f"   📝 Details: {r['details']}")
    else:
        print("\n❌ No public accounts found linked to this number.")

    print("\n⚠️ LEGAL DISCLAIMER:")
    print("   OSINT only. Do not misuse this tool.")
    print("="*70)

# =====================================================
# MAIN FUNCTION
# =====================================================

def main():
    banner()  # <-- ADDED YOUR BANNER

    print("\n" + "="*60)
    print("🔍 SOCIAL MEDIA FINDER OSINT TOOL")
    print("="*60)

    phone_number = input("\nEnter Phone Number: ").strip()
    country_code = input("Enter Country Code (e.g., US, IN, UK - optional): ").strip() or None

    print("\n[1/3] Validating phone number...")
    info = parse_phone_number(phone_number, country_code)

    if not info['valid']:
        print(f"❌ Error: {info['error']}")
        return

    print(f"   ✅ Valid: {info['international']}")
    print(f"   📍 Region: {info.get('region', 'Unknown')}")

    print("\n[2/3] Scanning social media platforms...")
    results = comprehensive_social_search(info['e164'])

    print("\n[3/3] Generating report...")
    display_results(results, info)


if __name__ == "__main__":
    main()
