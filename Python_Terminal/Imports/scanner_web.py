#!/usr/bin/env python3
"""
web_scanner.py - Scanner web leve
Funcionalidades:
- Crawling básico
- Checagem de headers de segurança
- Detecção simples de XSS refletido
- Extração de formulários

Modos:
- CLI com argumentos
- Menu interativo (quando executado sem argumentos)
"""

import argparse
import json
import time
import sys
from urllib.parse import urljoin, urlparse
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup
from colorama import init, Fore, Style

# Inicializa colorama (funciona no Windows)
init(autoreset=True)

# Cores apenas para saída (nunca nos inputs)
C = Fore.CYAN + Style.BRIGHT
G = Fore.GREEN + Style.BRIGHT
Y = Fore.YELLOW + Style.BRIGHT
R = Fore.RED + Style.BRIGHT
W = Fore.WHITE
DIM = Style.DIM
RESET = Style.RESET_ALL

# Configurações padrão
DEFAULT_USER_AGENT = "WebScanner/1.0 (contato: seuemail@example.com - uso apenas autorizado)"
DEFAULT_TIMEOUT = 8
REQUEST_DELAY = 0.25

XSS_TEST_PAYLOAD = "<script>alert(1337)</script>"
XSS_REFLECTED_INDICATORS = [
    "<script>alert(1337)</script>",
    "alert(1337)",
    "&lt;script&gt;alert(1337)&lt;/script&gt;"  # escaped mas ainda interessante
]


def is_same_domain(url: str, base_netloc: str) -> bool:
    try:
        parsed = urlparse(url)
        return parsed.netloc == base_netloc or parsed.netloc.endswith("." + base_netloc)
    except Exception:
        return False


def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    # Remove fragment e query vazia desnecessária
    return parsed._replace(fragment="", query=parsed.query if parsed.query else "").geturl()


def extract_links(html: str, base_url: str) -> set:
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith(("mailto:", "tel:", "javascript:")):
            continue
        absolute = urljoin(base_url, href)
        links.add(normalize_url(absolute))
    return links


def extract_forms(html: str, base_url: str) -> list:
    soup = BeautifulSoup(html, "html.parser")
    forms = []
    for form in soup.find_all("form"):
        action = form.get("action") or ""
        action_url = urljoin(base_url, action)
        method = (form.get("method") or "get").lower()
        inputs = []
        for element in form.find_all(["input", "textarea", "select"]):
            name = element.get("name")
            if not name:
                continue
            field_type = element.get("type") or element.name
            value = element.get("value") or ""
            inputs.append({"name": name, "type": field_type, "value": value})
        if inputs:
            forms.append({
                "action": action_url,
                "method": method,
                "inputs": inputs,
                "raw_preview": str(form)[:300]
            })
    return forms


def check_security_headers(response: requests.Response) -> list:
    headers_lower = {k.lower(): v for k, v in response.headers.items()}
    findings = []

    checks = [
        ("content-security-policy", "CSP ausente - risco de execução de scripts indesejados", "high"),
        ("x-frame-options", "X-Frame-Options ausente - risco de clickjacking", "medium"),
        ("strict-transport-security", "HSTS ausente em HTTPS", "medium") if response.url.startswith("https") else None,
        ("x-content-type-options", "X-Content-Type-Options ausente - risco de MIME sniffing", "low"),
        ("referrer-policy", "Referrer-Policy ausente", "low"),
        ("x-xss-protection", "X-XSS-Protection ausente (legado)", "info"),
    ]

    for header, desc, severity in [c for c in checks if c]:
        if header not in headers_lower:
            findings.append({
                "type": "MissingHeader",
                "header": header.title().replace("-", " "),
                "severity": severity,
                "description": desc
            })

    return findings


def test_xss_reflected(url: str, session: requests.Session) -> list:
    findings = []
    try:
        resp = session.get(url + "?" + urlencode({"q": XSS_TEST_PAYLOAD, "search": XSS_TEST_PAYLOAD, "s": XSS_TEST_PAYLOAD}), timeout=DEFAULT_TIMEOUT)
        content = resp.text.lower()
        for indicator in XSS_REFLECTED_INDICATORS:
            if indicator.lower() in content:
                findings.append({
                    "type": "PotentialXSS",
                    "url": resp.url,
                    "payload": XSS_TEST_PAYLOAD,
                    "severity": "high",
                    "description": "Payload refletido na resposta (possível XSS refletido)"
                })
                break
    except Exception:
        pass
    return findings


def crawl_and_scan(target_url: str, max_pages: int = 150, max_threads: int = 6):
    parsed = urlparse(target_url)
    base_netloc = parsed.netloc
    base_scheme = parsed.scheme

    if base_scheme not in ("http", "https"):
        print(f"{R}Esquema nao suportado: {base_scheme}{RESET}")
        return

    session = requests.Session()
    session.headers.update({"User-Agent": DEFAULT_USER_AGENT})
    session.verify = True  # pode mudar para False em testes locais

    visited = set()
    to_visit = deque([target_url])
    results = {
        "target": target_url,
        "start_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "pages_visited": 0,
        "vulnerabilities": [],
        "forms_found": [],
        "security_headers": []
    }

    print(f"{G}Iniciando scan em: {target_url}{RESET}")
    print(f"  Limite de paginas: {max_pages}   Threads: {max_threads}\n")

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_url = {}

        while to_visit and results["pages_visited"] < max_pages:
            while to_visit and len(future_to_url) < max_threads * 2:
                url = to_visit.popleft()
                if url in visited:
                    continue
                visited.add(url)
                results["pages_visited"] += 1
                future = executor.submit(
                    lambda u: (
                        u,
                        session.get(u, timeout=DEFAULT_TIMEOUT, allow_redirects=True)
                    ),
                    url
                )
                future_to_url[future] = url

            for future in as_completed(future_to_url):
                url = future_to_url.pop(future)
                try:
                    resp = future.result()[1]
                    if resp.status_code != 200:
                        continue

                    html = resp.text
                    links = extract_links(html, url)
                    forms = extract_forms(html, url)

                    # Adiciona formulários encontrados
                    results["forms_found"].extend(forms)

                    # Checa headers
                    header_findings = check_security_headers(resp)
                    results["security_headers"].extend(header_findings)

                    # Teste simples de XSS refletido
                    xss_findings = test_xss_reflected(url, session)
                    results["vulnerabilities"].extend(xss_findings)

                    # Adiciona links novos para fila
                    for link in links:
                        if link not in visited and is_same_domain(link, base_netloc):
                            to_visit.append(link)

                    print(f"{DIM}Visitado ({results['pages_visited']}): {url}{RESET}")

                    time.sleep(REQUEST_DELAY)

                except Exception as e:
                    print(f"{R}Erro ao processar {url}: {e}{RESET}")

    session.close()

    # Relatório final
    print(f"\n{G}Scan concluido{RESET}")
    print(f"Paginas visitadas: {results['pages_visited']}")
    print(f"Formularios encontrados: {len(results['forms_found'])}")
    print(f"Vulnerabilidades detectadas: {len(results['vulnerabilities'])}")
    print(f"Problemas de headers: {len(results['security_headers'])}")

    if results["vulnerabilities"]:
        print(f"\n{Y}Possiveis XSS refletidos encontrados:{RESET}")
        for v in results["vulnerabilities"]:
            print(f"  {R}HIGH{Y} → {v['url']}")
            print(f"      Payload: {v['payload']}")

    if results["security_headers"]:
        print(f"\n{Y}Headers de seguranca ausentes ou problematicos:{RESET}")
        for h in results["security_headers"]:
            sev = h["severity"].upper()
            color = R if "high" in sev else Y if "medium" in sev else DIM
            print(f"  {color}{sev}{RESET} → {h['header']}  ({h['description']})")

    # Salva relatório JSON
    report_file = f"scan_{base_netloc.replace('.', '_')}_{int(time.time())}.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nRelatorio salvo em: {report_file}\n")


def show_menu():
    print(f"\n{C}Web Scanner Leve - Menu{RESET}")
    print("-" * 50)
    print(f" {G}1{Y}  Iniciar scan (crawling + analise)")
    print(f" {G}2{Y}  Testar apenas headers de seguranca")
    print(f" {G}3{Y}  Testar XSS refletido em URL especifica")
    print(f" {R}0{Y}  Sair")
    print("-" * 50)


def main():
    parser = argparse.ArgumentParser(
        description="Web Scanner leve - crawling e checagens basicas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python web_scanner.py --target https://example.com
  python web_scanner.py --target https://example.com --max-pages 100 --threads 4
  python web_scanner.py --target https://example.com --only-headers
        """
    )
    parser.add_argument("--target", help="URL inicial (ex: https://example.com)")
    parser.add_argument("--max-pages", type=int, default=150, help="Numero maximo de paginas")
    parser.add_argument("--threads", type=int, default=6, help="Numero de threads simultaneas")
    parser.add_argument("--only-headers", action="store_true", help="Checar apenas headers de seguranca")
    parser.add_argument("--test-xss", help="Testar XSS refletido apenas nesta URL")

    args = parser.parse_args()

    # Modo CLI
    if args.target or args.test_xss:
        if args.test_xss:
            session = requests.Session()
            session.headers.update({"User-Agent": DEFAULT_USER_AGENT})
            findings = test_xss_reflected(args.test_xss, session)
            if findings:
                print(f"{R}Possivel XSS refletido detectado:{RESET}")
                for f in findings:
                    print(f"  URL: {f['url']}")
                    print(f"  Payload: {f['payload']}")
            else:
                print(f"{G}Nenhum reflexo de XSS detectado nesta URL.{RESET}")
            return

        if args.only_headers:
            try:
                resp = requests.get(args.target, timeout=DEFAULT_TIMEOUT, headers={"User-Agent": DEFAULT_USER_AGENT})
                findings = check_security_headers(resp)
                if findings:
                    print(f"{Y}Problemas encontrados em {args.target}:{RESET}")
                    for f in findings:
                        print(f"  {f['header']} ausente - {f['description']}")
                else:
                    print(f"{G}Todos os headers importantes estao presentes.{RESET}")
            except Exception as e:
                print(f"{R}Erro ao acessar URL: {e}{RESET}")
            return

        # Scan completo
        crawl_and_scan(args.target, args.max_pages, args.threads)
        return

    # Modo interativo (menu)
    while True:
        show_menu()
        choice = input("Escolha uma opcao: ").strip()

        if choice == "0":
            print(f"{Y}Saindo...{RESET}")
            break

        elif choice == "1":
            target = input("URL alvo (ex: https://example.com): ").strip()
            if not target:
                print(f"{R}URL obrigatoria.{RESET}")
                continue
            if not target.startswith(("http://", "https://")):
                target = "https://" + target
            max_pages = input("Numero maximo de paginas (padrao 150): ").strip()
            max_pages = int(max_pages) if max_pages.isdigit() else 150
            threads = input("Numero de threads (padrao 6): ").strip()
            threads = int(threads) if threads.isdigit() else 6

            crawl_and_scan(target, max_pages, threads)

        elif choice == "2":
            target = input("URL para checar headers: ").strip()
            if not target:
                continue
            if not target.startswith(("http://", "https://")):
                target = "https://" + target
            try:
                resp = requests.get(target, timeout=DEFAULT_TIMEOUT, headers={"User-Agent": DEFAULT_USER_AGENT})
                findings = check_security_headers(resp)
                if findings:
                    print(f"\n{Y}Resultados para {target}:{RESET}")
                    for f in findings:
                        print(f"  {f['header']} - {f['description']}")
                else:
                    print(f"{G}Headers de seguranca principais encontrados.{RESET}")
            except Exception as e:
                print(f"{R}Erro: {e}{RESET}")

        elif choice == "3":
            url = input("URL completa para testar XSS refletido: ").strip()
            if not url:
                continue
            session = requests.Session()
            session.headers.update({"User-Agent": DEFAULT_USER_AGENT})
            findings = test_xss_reflected(url, session)
            if findings:
                print(f"{R}Possivel reflexo encontrado!{RESET}")
                for f in findings:
                    print(f"  {f['url']}")
            else:
                print(f"{G}Nenhum reflexo detectado com o payload testado.{RESET}")

        else:
            print(f"{R}Opcao invalida.{RESET}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{R}Interrompido pelo usuario.{RESET}")
    except Exception as e:
        print(f"{R}Erro fatal: {e}{RESET}")
        sys.exit(1)