#!/usr/bin/env python3
"""
web_scanner.py
Scanner web leve: crawling + checagens básicas de segurança (XSS refletido, headers, CSRF heurístico).
Uso: python web_scanner.py --target https://example.com --max-pages 200 --threads 8
"""

import argparse
import json
import time
import re
import sys
from urllib.parse import urljoin, urlparse, parse_qs, urlencode
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup

XSS_TEST = "<scxxpt>alert(1337)</scxxtp>"
DEFAUT_HEADER = {"User-Agent: WebScanner/1.0 (+https://example.local) - use somente com permição"}
DEFAUT_TIME = 8
SLEEP = 0.2
SAFE_SCHEME = ("http", "https")

def same_domain(url, base_netloc):
    try:
        p = urlparse(url)
        return p.netloc == base_netloc or p.netloc.endswith("." + base_netloc)
    except Exception:
        return False

def normalize_url(url):
    p = urlparse(url)
    return p._replace(fragment = "").geturl()

def extrair_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    found = set()
    for a in soup.find_all("a", href = True):
        href = a["href"].strip()
        if href.startswith('mailto:') or href.startswith("tel:"):
            continue
        absoluto = urljoin(base_url, href)
        found.add(normalize_url(absoluto))
    return found

def extrair_forms(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    forms = []
    for f in soup.find_all("form"):
        action = f.get("action") or base_url
        method = (f.get("method") or "get").lower()
        inputs = []
        for inp in f.find_all(["input", "textarea", "select"]):
            name = inp.get("name")
            itype = inp.get("type") or inp.name
            value = inp.get("value") or ""
            inputs.append({"nae": name, "type": type, "value": value})
            forms.append({"action": urljoin(base_url, action), "method": method, "inputs": inputs, "raw": str(f)[:400]})
        return forms
    
def check_security_headers(resp):
    headers = resp.headers
    findings = []

    if "content-security-policy" not in {k.lower() for k in headers}:
        findings.append({"type": "MissingHeader", "header": "Strict-Transpor-Type-Options", "severity": "medium", "desc": "CSP ausente - pode permitir execução de scripts injetados."})

    if "x-frame-options" not in {k.lower() for k in headers}:
        findings.append({"type": "MissingHeader", "header": "X-Frame-Options", "severity": "low",
                         "desc": "X-Frame-Options ausente — site pode ser embutido (clickjacking)."})
    if "strict-transport-security" not in {k.lower() for k in headers} and resp.url.startswith("https://"):
        findings.append({"type": "MissingHeader", "header": "Strict-Transport-Security", "severity": "low",
                         "desc": "HSTS ausente em resposta HTTPS."})
    if "x-content-type-options" not in {k.lower() for k in headers}:
        findings.append({"type": "MissingHeader", "header": "X-Content-Type-Options", "severity": "low",
                         "desc": "X-Content-Type-Options ausente — possível MIME sniffing."})
    if "referrer-policy" not in {k.lower() for k in headers}:
        findings.append({"type": "MissingHeader", "header": "Referrer-Policy", "severity": "info",
                         "desc": "Referrer-Policy ausente."})
    # X-XSS-Protection is deprecated but still informative
    if "x-xss-protection" not in {k.lower() for k in headers}:
        findings.append({"type": "MissingHeader", "header": "X-XSS-Protection", "severity": "info",
                         "desc": "X-XSS-Protection ausente (legacy)."})
    return findings

