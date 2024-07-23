import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

# Initialize the console
console = Console()

def check_csp_header(url):
    try:
        response = requests.get(url)
        headers = response.headers

        if 'Content-Security-Policy' in headers:
            return True, headers['Content-Security-Policy']
        else:
            return False, None
    except requests.RequestException as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        return None, None

def main():
    console.print(Panel("OWASP-2021-A05: Security Misconfiguration - Content Security Policy (CSP) Header Not Set", style="bold blue", box=box.DOUBLE))
    
    url = console.input("[bold green]Enter the URL to check: [/bold green]")
    
    has_csp, csp_header = check_csp_header(url)
    
    table = Table(title="CSP Header Check Result", box=box.ROUNDED)
    table.add_column("URL", justify="left", style="cyan", no_wrap=True)
    table.add_column("CSP Header Present", justify="center", style="magenta")
    table.add_column("CSP Header Value", justify="left", style="green")
    
    if has_csp is None:
        console.print("[bold red]Failed to check the URL.[/bold red]")
    elif has_csp:
        table.add_row(url, "[bold green]Yes[/bold green]", csp_header)
        console.print(table)
        console.print("[bold green]The CSP header is set correctly.[/bold green]")
    else:
        table.add_row(url, "[bold red]No[/bold red]", "[bold red]N/A[/bold red]")
        console.print(table)
        console.print("[bold red]The CSP header is missing! This can lead to XSS vulnerabilities.[/bold red]")
        console.print("[bold yellow]Proof of Concept:[/bold yellow] You can inject a script tag in the URL parameters to demonstrate XSS.")
        console.print(f"[bold yellow]Example:[/bold yellow] {url}?q=<script>alert('XSS')</script>")
    
    console.print(Panel("Script by @ibnurusdianto", style="bold green", box=box.DOUBLE))
    console.print(Panel("Moo! 🐄", style="bold magenta", box=box.ROUNDED))

if __name__ == "__main__":
    main()