#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Link Checker for Digital Finance Course
========================================

Validates all links across markdown, notebooks, HTML, and LaTeX files.
Supports external URL validation, internal path checking, anchor validation,
and auto-fixing of common issues like Colab username placeholders.

Usage Examples:
    # Basic scan with all report formats
    python check_links.py

    # Scan specific directory
    python check_links.py --path ./day_01

    # Skip external URL validation (faster)
    python check_links.py --skip-external

    # Auto-fix placeholder usernames
    python check_links.py --fix

    # Preview fixes without applying
    python check_links.py --fix --dry-run

    # JSON report only
    python check_links.py --format json --output my_report

    # Verbose output with custom timeout
    python check_links.py --verbose --timeout 15

Author: Digital Finance Course Team
"""

import os
import re
import json
import argparse
import time
import subprocess
from pathlib import Path
from urllib.parse import urlparse, unquote
from typing import Dict, List, Optional, Tuple, Set, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
from collections import defaultdict

try:
    import requests
except ImportError:
    print("Error: 'requests' library required. Install with: pip install requests")
    exit(1)


# =============================================================================
# Constants
# =============================================================================

TIMEOUT = 10
RETRY_COUNT = 3
RATE_LIMIT_DELAY = 0.5
MAX_REDIRECTS = 5
USER_AGENT = "DigitalFinance-LinkChecker/1.0"

# Regex patterns for link extraction
MARKDOWN_LINK = r'\[([^\]]*)\]\(([^)]+)\)'
MARKDOWN_AUTOLINK = r'<(https?://[^>]+)>'
HTML_HREF = r'href=["\']([^"\']+)["\']'
HTML_SRC = r'src=["\']([^"\']+)["\']'
LATEX_HREF = r'\\href\{([^}]+)\}\{[^}]*\}'
LATEX_URL = r'\\url\{([^}]+)\}'

# File extensions to scan
FILE_EXTENSIONS = {
    'markdown': ['.md', '.markdown'],
    'notebook': ['.ipynb'],
    'html': ['.html', '.htm'],
    'latex': ['.tex', '.latex']
}

# Patterns to skip
SKIP_PATTERNS = [
    r'^mailto:',
    r'^javascript:',
    r'^data:',
    r'^localhost',
    r'^127\.0\.0\.1',
    r'^file://',
]

# Placeholder patterns
PLACEHOLDER_PATTERNS = [
    r'YOUR_USERNAME',
    r'yourusername',
    r'your-username',
    r'YOUR-USERNAME',
    r'\bTODO\b',
    r'^#$',  # Exactly "#"
]


# =============================================================================
# Console Colors
# =============================================================================

class Colors:
    """ANSI color codes for console output (disabled on Windows cmd)."""
    if os.name != 'nt' or os.environ.get('TERM'):
        RED = '\033[91m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        MAGENTA = '\033[95m'
        CYAN = '\033[96m'
        BOLD = '\033[1m'
        RESET = '\033[0m'
    else:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = BOLD = RESET = ''


# =============================================================================
# Enums
# =============================================================================

class LinkCategory(Enum):
    """Categories of links based on their target."""
    EXTERNAL = "external"
    INTERNAL = "internal"
    ANCHOR = "anchor"
    COLAB = "colab"
    PLACEHOLDER = "placeholder"
    UNKNOWN = "unknown"


class ValidationStatus(Enum):
    """Status of link validation."""
    OK = "ok"
    BROKEN = "broken"
    PLACEHOLDER = "placeholder"
    TIMEOUT = "timeout"
    ERROR = "error"
    SKIPPED = "skipped"
    REDIRECT = "redirect"


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class Link:
    """Represents a link found in a source file."""
    url: str
    source_file: Path
    line_number: int
    link_text: str = ""
    category: LinkCategory = LinkCategory.UNKNOWN

    def __hash__(self):
        return hash((self.url, str(self.source_file), self.line_number))


@dataclass
class ValidationResult:
    """Result of validating a single link."""
    link: Link
    status: ValidationStatus
    message: str = ""
    response_code: Optional[int] = None
    redirect_url: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'url': self.link.url,
            'source_file': str(self.link.source_file),
            'line_number': self.link.line_number,
            'link_text': self.link.link_text,
            'category': self.link.category.value,
            'status': self.status.value,
            'message': self.message,
            'response_code': self.response_code,
            'redirect_url': self.redirect_url
        }


# =============================================================================
# Link Discovery Module
# =============================================================================

def discover_files(root_dir: Path) -> Dict[str, List[Path]]:
    """
    Find all scannable files organized by type.

    Args:
        root_dir: Root directory to scan

    Returns:
        Dictionary mapping file type to list of file paths
    """
    files_by_type: Dict[str, List[Path]] = defaultdict(list)

    # Directories to skip
    skip_dirs = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', '.omc'}

    for path in root_dir.rglob('*'):
        if path.is_file():
            # Skip if in excluded directory
            if any(skip_dir in path.parts for skip_dir in skip_dirs):
                continue

            suffix = path.suffix.lower()
            for file_type, extensions in FILE_EXTENSIONS.items():
                if suffix in extensions:
                    files_by_type[file_type].append(path)
                    break

    return dict(files_by_type)


def extract_markdown_links(content: str, filepath: Path) -> List[Link]:
    """
    Extract links from markdown content.

    Args:
        content: Markdown text content
        filepath: Source file path

    Returns:
        List of Link objects
    """
    links = []
    lines = content.split('\n')

    for line_num, line in enumerate(lines, 1):
        # Standard markdown links [text](url)
        for match in re.finditer(MARKDOWN_LINK, line):
            link_text, url = match.groups()
            # Handle title in URL: (url "title")
            url = url.split()[0].strip('"\'')
            links.append(Link(
                url=url,
                source_file=filepath,
                line_number=line_num,
                link_text=link_text
            ))

        # Autolinks <https://example.com>
        for match in re.finditer(MARKDOWN_AUTOLINK, line):
            url = match.group(1)
            links.append(Link(
                url=url,
                source_file=filepath,
                line_number=line_num,
                link_text=""
            ))

    return links


def extract_notebook_links(filepath: Path) -> List[Link]:
    """
    Extract links from Jupyter notebook files.

    Args:
        filepath: Path to .ipynb file

    Returns:
        List of Link objects
    """
    links = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"{Colors.YELLOW}Warning: Could not parse {filepath}: {e}{Colors.RESET}")
        return links

    cells = notebook.get('cells', [])

    for cell_idx, cell in enumerate(cells):
        cell_type = cell.get('cell_type', '')
        source = cell.get('source', [])

        # Join source lines
        if isinstance(source, list):
            content = ''.join(source)
        else:
            content = source

        # Extract from markdown cells
        if cell_type == 'markdown':
            cell_links = extract_markdown_links(content, filepath)
            # Adjust line numbers to indicate cell index
            for link in cell_links:
                link.line_number = cell_idx + 1  # Cell number (1-indexed)
            links.extend(cell_links)

        # Also check code cells for URLs in comments or strings
        elif cell_type == 'code':
            # Look for URLs in strings/comments
            for match in re.finditer(r'https?://[^\s\'"<>]+', content):
                url = match.group(0).rstrip('.,;:)')
                links.append(Link(
                    url=url,
                    source_file=filepath,
                    line_number=cell_idx + 1,
                    link_text=""
                ))

    return links


def extract_html_links(content: str, filepath: Path) -> List[Link]:
    """
    Extract links from HTML content.

    Args:
        content: HTML text content
        filepath: Source file path

    Returns:
        List of Link objects
    """
    links = []
    lines = content.split('\n')

    for line_num, line in enumerate(lines, 1):
        # href attributes
        for match in re.finditer(HTML_HREF, line, re.IGNORECASE):
            url = match.group(1)
            links.append(Link(
                url=url,
                source_file=filepath,
                line_number=line_num,
                link_text=""
            ))

        # src attributes
        for match in re.finditer(HTML_SRC, line, re.IGNORECASE):
            url = match.group(1)
            links.append(Link(
                url=url,
                source_file=filepath,
                line_number=line_num,
                link_text=""
            ))

    return links


def extract_latex_links(content: str, filepath: Path) -> List[Link]:
    """
    Extract links from LaTeX content.

    Args:
        content: LaTeX text content
        filepath: Source file path

    Returns:
        List of Link objects
    """
    links = []
    lines = content.split('\n')

    for line_num, line in enumerate(lines, 1):
        # \href{url}{text}
        for match in re.finditer(LATEX_HREF, line):
            url = match.group(1)
            links.append(Link(
                url=url,
                source_file=filepath,
                line_number=line_num,
                link_text=""
            ))

        # \url{url}
        for match in re.finditer(LATEX_URL, line):
            url = match.group(1)
            links.append(Link(
                url=url,
                source_file=filepath,
                line_number=line_num,
                link_text=""
            ))

    return links


def discover_all_links(root_dir: Path, verbose: bool = False) -> List[Link]:
    """
    Discover all links in the project.

    Args:
        root_dir: Root directory to scan
        verbose: Print progress information

    Returns:
        List of all discovered links
    """
    all_links = []
    files_by_type = discover_files(root_dir)

    if verbose:
        total_files = sum(len(files) for files in files_by_type.values())
        print(f"Scanning {total_files} files...")

    # Process markdown files
    for filepath in files_by_type.get('markdown', []):
        try:
            content = filepath.read_text(encoding='utf-8')
            links = extract_markdown_links(content, filepath)
            all_links.extend(links)
            if verbose:
                print(f"  {filepath}: {len(links)} links")
        except Exception as e:
            print(f"{Colors.YELLOW}Warning: Error reading {filepath}: {e}{Colors.RESET}")

    # Process notebooks
    for filepath in files_by_type.get('notebook', []):
        links = extract_notebook_links(filepath)
        all_links.extend(links)
        if verbose:
            print(f"  {filepath}: {len(links)} links")

    # Process HTML files
    for filepath in files_by_type.get('html', []):
        try:
            content = filepath.read_text(encoding='utf-8')
            links = extract_html_links(content, filepath)
            all_links.extend(links)
            if verbose:
                print(f"  {filepath}: {len(links)} links")
        except Exception as e:
            print(f"{Colors.YELLOW}Warning: Error reading {filepath}: {e}{Colors.RESET}")

    # Process LaTeX files
    for filepath in files_by_type.get('latex', []):
        try:
            content = filepath.read_text(encoding='utf-8')
            links = extract_latex_links(content, filepath)
            all_links.extend(links)
            if verbose:
                print(f"  {filepath}: {len(links)} links")
        except Exception as e:
            print(f"{Colors.YELLOW}Warning: Error reading {filepath}: {e}{Colors.RESET}")

    # Categorize all links
    for link in all_links:
        link.category = categorize_link(link.url, link.source_file)

    return all_links


# =============================================================================
# Link Categorization
# =============================================================================

def is_placeholder(url: str) -> bool:
    """Check if URL is a placeholder that needs to be filled in."""
    for pattern in PLACEHOLDER_PATTERNS:
        if re.search(pattern, url, re.IGNORECASE):
            return True
    return False


def is_colab_link(url: str) -> bool:
    """Check if URL is a Google Colab link."""
    return 'colab.research.google.com' in url or 'colab.google.com' in url


def is_anchor(url: str) -> bool:
    """Check if URL is an anchor link (starts with #)."""
    return url.startswith('#') and url != '#'


def is_external(url: str) -> bool:
    """Check if URL is an external link (http/https)."""
    return url.startswith('http://') or url.startswith('https://')


def is_internal(url: str) -> bool:
    """Check if URL is a relative internal path."""
    if is_external(url) or is_anchor(url):
        return False
    # Skip special protocols
    for pattern in SKIP_PATTERNS:
        if re.match(pattern, url, re.IGNORECASE):
            return False
    return True


def should_skip(url: str) -> bool:
    """Check if URL should be skipped entirely."""
    for pattern in SKIP_PATTERNS:
        if re.match(pattern, url, re.IGNORECASE):
            return True
    return False


def categorize_link(url: str, source_file: Path) -> LinkCategory:
    """
    Categorize a link based on its URL pattern.

    Args:
        url: The URL to categorize
        source_file: The source file containing the link

    Returns:
        LinkCategory enum value
    """
    if is_placeholder(url):
        return LinkCategory.PLACEHOLDER

    if is_colab_link(url):
        return LinkCategory.COLAB

    if is_anchor(url):
        return LinkCategory.ANCHOR

    if is_external(url):
        return LinkCategory.EXTERNAL

    if is_internal(url):
        return LinkCategory.INTERNAL

    return LinkCategory.UNKNOWN


# =============================================================================
# Validation Engine
# =============================================================================

class LinkValidator:
    """
    Validates links with caching and rate limiting.
    """

    def __init__(self, root_dir: Path, timeout: int = TIMEOUT, verbose: bool = False):
        self.root_dir = root_dir
        self.timeout = timeout
        self.verbose = verbose
        self.cache: Dict[str, ValidationResult] = {}
        self.domain_last_request: Dict[str, float] = {}
        self.session = requests.Session()
        self.session.headers['User-Agent'] = USER_AGENT

    def _rate_limit(self, url: str) -> None:
        """Apply rate limiting per domain."""
        try:
            domain = urlparse(url).netloc
            if domain in self.domain_last_request:
                elapsed = time.time() - self.domain_last_request[domain]
                if elapsed < RATE_LIMIT_DELAY:
                    time.sleep(RATE_LIMIT_DELAY - elapsed)
            self.domain_last_request[domain] = time.time()
        except Exception:
            pass

    def validate_link(self, link: Link, skip_external: bool = False) -> ValidationResult:
        """
        Validate a single link.

        Args:
            link: Link object to validate
            skip_external: Skip external URL validation

        Returns:
            ValidationResult object
        """
        url = link.url

        # Check cache first
        cache_key = f"{link.category.value}:{url}"
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            # Return new result with same status but correct link
            return ValidationResult(
                link=link,
                status=cached.status,
                message=cached.message,
                response_code=cached.response_code,
                redirect_url=cached.redirect_url
            )

        # Skip certain URL patterns
        if should_skip(url):
            result = ValidationResult(
                link=link,
                status=ValidationStatus.SKIPPED,
                message="Skipped (special protocol)"
            )
            self.cache[cache_key] = result
            return result

        # Route to appropriate validator
        if link.category == LinkCategory.PLACEHOLDER:
            result = ValidationResult(
                link=link,
                status=ValidationStatus.PLACEHOLDER,
                message="Placeholder URL needs to be updated"
            )

        elif link.category == LinkCategory.EXTERNAL or link.category == LinkCategory.COLAB:
            if skip_external:
                result = ValidationResult(
                    link=link,
                    status=ValidationStatus.SKIPPED,
                    message="External validation skipped"
                )
            else:
                result = self.validate_external_url(link)

        elif link.category == LinkCategory.INTERNAL:
            result = self.validate_internal_path(link)

        elif link.category == LinkCategory.ANCHOR:
            result = self.validate_anchor(link)

        else:
            result = ValidationResult(
                link=link,
                status=ValidationStatus.SKIPPED,
                message="Unknown link category"
            )

        self.cache[cache_key] = result
        return result

    def validate_external_url(self, link: Link) -> ValidationResult:
        """
        Validate an external URL.

        Args:
            link: Link object with external URL

        Returns:
            ValidationResult object
        """
        url = link.url
        self._rate_limit(url)

        for attempt in range(RETRY_COUNT):
            try:
                # Try HEAD first (faster)
                response = self.session.head(
                    url,
                    timeout=self.timeout,
                    allow_redirects=True
                )

                # Some servers reject HEAD, try GET
                if response.status_code == 405:
                    response = self.session.get(
                        url,
                        timeout=self.timeout,
                        allow_redirects=True,
                        stream=True  # Don't download body
                    )
                    response.close()

                status_code = response.status_code

                # Check for redirects
                final_url = response.url if response.url != url else None

                if 200 <= status_code < 300:
                    return ValidationResult(
                        link=link,
                        status=ValidationStatus.OK,
                        message="OK",
                        response_code=status_code,
                        redirect_url=final_url
                    )

                elif 300 <= status_code < 400:
                    return ValidationResult(
                        link=link,
                        status=ValidationStatus.REDIRECT,
                        message=f"Redirect to {final_url}",
                        response_code=status_code,
                        redirect_url=final_url
                    )

                elif status_code == 403:
                    # Some sites block bots but link may be valid
                    return ValidationResult(
                        link=link,
                        status=ValidationStatus.OK,
                        message="Access restricted (may be valid)",
                        response_code=status_code
                    )

                elif status_code == 429:
                    # Rate limited, wait and retry
                    if attempt < RETRY_COUNT - 1:
                        time.sleep(2 ** attempt)
                        continue
                    return ValidationResult(
                        link=link,
                        status=ValidationStatus.ERROR,
                        message="Rate limited",
                        response_code=status_code
                    )

                elif 400 <= status_code < 500:
                    return ValidationResult(
                        link=link,
                        status=ValidationStatus.BROKEN,
                        message=f"Client error: {status_code}",
                        response_code=status_code
                    )

                else:  # 5xx
                    if attempt < RETRY_COUNT - 1:
                        time.sleep(2 ** attempt)
                        continue
                    return ValidationResult(
                        link=link,
                        status=ValidationStatus.ERROR,
                        message=f"Server error: {status_code}",
                        response_code=status_code
                    )

            except requests.exceptions.Timeout:
                if attempt < RETRY_COUNT - 1:
                    time.sleep(2 ** attempt)
                    continue
                return ValidationResult(
                    link=link,
                    status=ValidationStatus.TIMEOUT,
                    message="Connection timed out"
                )

            except requests.exceptions.SSLError as e:
                return ValidationResult(
                    link=link,
                    status=ValidationStatus.ERROR,
                    message=f"SSL error: {str(e)[:50]}"
                )

            except requests.exceptions.ConnectionError as e:
                if attempt < RETRY_COUNT - 1:
                    time.sleep(2 ** attempt)
                    continue
                return ValidationResult(
                    link=link,
                    status=ValidationStatus.BROKEN,
                    message=f"Connection failed: {str(e)[:50]}"
                )

            except Exception as e:
                return ValidationResult(
                    link=link,
                    status=ValidationStatus.ERROR,
                    message=f"Error: {str(e)[:50]}"
                )

        return ValidationResult(
            link=link,
            status=ValidationStatus.ERROR,
            message="Max retries exceeded"
        )

    def validate_internal_path(self, link: Link) -> ValidationResult:
        """
        Validate an internal file path.

        Args:
            link: Link object with internal path

        Returns:
            ValidationResult object
        """
        url = link.url

        # Handle URL-encoded paths
        decoded_url = unquote(url)

        # Remove query string and anchor
        path_part = decoded_url.split('?')[0].split('#')[0]

        # Resolve relative to source file's directory
        source_dir = link.source_file.parent

        try:
            # Handle both forward and backward slashes
            path_part = path_part.replace('\\', '/')

            if path_part.startswith('/'):
                # Absolute path from root
                target_path = self.root_dir / path_part.lstrip('/')
            else:
                # Relative path
                target_path = source_dir / path_part

            # Normalize the path
            target_path = target_path.resolve()

            if target_path.exists():
                return ValidationResult(
                    link=link,
                    status=ValidationStatus.OK,
                    message="File exists"
                )
            else:
                return ValidationResult(
                    link=link,
                    status=ValidationStatus.BROKEN,
                    message=f"File not found: {target_path}"
                )

        except Exception as e:
            return ValidationResult(
                link=link,
                status=ValidationStatus.ERROR,
                message=f"Path error: {str(e)[:50]}"
            )

    def validate_anchor(self, link: Link) -> ValidationResult:
        """
        Validate an anchor link.

        Args:
            link: Link object with anchor

        Returns:
            ValidationResult object
        """
        anchor = link.url.lstrip('#')

        # Handle cross-file anchors: file.md#section
        if '#' in link.url and not link.url.startswith('#'):
            parts = link.url.split('#')
            file_path = parts[0]
            anchor = parts[1] if len(parts) > 1 else ''

            # Resolve file path
            source_dir = link.source_file.parent
            target_file = (source_dir / file_path).resolve()

            if not target_file.exists():
                return ValidationResult(
                    link=link,
                    status=ValidationStatus.BROKEN,
                    message=f"Target file not found: {target_file}"
                )

            try:
                content = target_file.read_text(encoding='utf-8')
            except Exception as e:
                return ValidationResult(
                    link=link,
                    status=ValidationStatus.ERROR,
                    message=f"Cannot read target file: {e}"
                )
        else:
            # Same-file anchor
            try:
                content = link.source_file.read_text(encoding='utf-8')
            except Exception as e:
                return ValidationResult(
                    link=link,
                    status=ValidationStatus.ERROR,
                    message=f"Cannot read source file: {e}"
                )

        # Extract headers and generate anchors
        headers = self._extract_headers(content)
        anchors = [self._slugify(h) for h in headers]

        # Also check for explicit anchor IDs
        explicit_anchors = re.findall(r'\{#([^}]+)\}', content)
        anchors.extend(explicit_anchors)

        # HTML id attributes
        html_ids = re.findall(r'id=["\']([^"\']+)["\']', content)
        anchors.extend(html_ids)

        if anchor.lower() in [a.lower() for a in anchors]:
            return ValidationResult(
                link=link,
                status=ValidationStatus.OK,
                message="Anchor found"
            )
        else:
            return ValidationResult(
                link=link,
                status=ValidationStatus.BROKEN,
                message=f"Anchor not found. Available: {', '.join(anchors[:5])}"
            )

    def _extract_headers(self, content: str) -> List[str]:
        """Extract markdown headers from content."""
        headers = []

        # ATX-style headers: # Header
        for match in re.finditer(r'^#{1,6}\s+(.+?)(?:\s*\{#[^}]+\})?\s*$', content, re.MULTILINE):
            headers.append(match.group(1).strip())

        return headers

    def _slugify(self, text: str) -> str:
        """
        Convert header text to GitHub-style anchor slug.

        GitHub rules:
        - Lowercase
        - Replace spaces with hyphens
        - Remove special characters except hyphens
        - Remove leading/trailing hyphens
        """
        slug = text.lower()
        # Remove markdown formatting
        slug = re.sub(r'\*\*([^*]+)\*\*', r'\1', slug)  # Bold
        slug = re.sub(r'\*([^*]+)\*', r'\1', slug)  # Italic
        slug = re.sub(r'`([^`]+)`', r'\1', slug)  # Code
        slug = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', slug)  # Links
        # Replace spaces with hyphens
        slug = re.sub(r'\s+', '-', slug)
        # Remove special characters
        slug = re.sub(r'[^a-z0-9\-_]', '', slug)
        # Remove multiple consecutive hyphens
        slug = re.sub(r'-+', '-', slug)
        # Remove leading/trailing hyphens
        slug = slug.strip('-')
        return slug

    def validate_all_links(
        self,
        links: List[Link],
        skip_external: bool = False
    ) -> List[ValidationResult]:
        """
        Validate all links.

        Args:
            links: List of Link objects to validate
            skip_external: Skip external URL validation

        Returns:
            List of ValidationResult objects
        """
        results = []
        total = len(links)

        for i, link in enumerate(links, 1):
            if self.verbose:
                print(f"  [{i}/{total}] Validating: {link.url[:60]}...")

            result = self.validate_link(link, skip_external)
            results.append(result)

            if self.verbose and result.status not in (ValidationStatus.OK, ValidationStatus.SKIPPED):
                status_color = {
                    ValidationStatus.BROKEN: Colors.RED,
                    ValidationStatus.PLACEHOLDER: Colors.YELLOW,
                    ValidationStatus.TIMEOUT: Colors.YELLOW,
                    ValidationStatus.ERROR: Colors.RED,
                }.get(result.status, '')
                print(f"    {status_color}{result.status.value}: {result.message}{Colors.RESET}")

        return results


# =============================================================================
# Reporting Module
# =============================================================================

def generate_console_report(results: List[ValidationResult]) -> None:
    """
    Generate a colored console report.

    Args:
        results: List of validation results
    """
    # Summary statistics
    total = len(results)
    by_status = defaultdict(list)
    by_category = defaultdict(list)

    for r in results:
        by_status[r.status].append(r)
        by_category[r.link.category].append(r)

    # Print header
    print("\n" + "=" * 70)
    print(f"{Colors.BOLD}LINK CHECK REPORT{Colors.RESET}")
    print("=" * 70)

    # Print summary
    print(f"\n{Colors.BOLD}Summary:{Colors.RESET}")
    print(f"  Total links scanned: {total}")
    print()

    print(f"  {Colors.BOLD}By Status:{Colors.RESET}")
    for status in ValidationStatus:
        count = len(by_status.get(status, []))
        if count > 0:
            color = {
                ValidationStatus.OK: Colors.GREEN,
                ValidationStatus.BROKEN: Colors.RED,
                ValidationStatus.PLACEHOLDER: Colors.YELLOW,
                ValidationStatus.TIMEOUT: Colors.YELLOW,
                ValidationStatus.ERROR: Colors.RED,
                ValidationStatus.SKIPPED: Colors.CYAN,
                ValidationStatus.REDIRECT: Colors.BLUE,
            }.get(status, '')
            print(f"    {color}{status.value}: {count}{Colors.RESET}")

    print()
    print(f"  {Colors.BOLD}By Category:{Colors.RESET}")
    for category in LinkCategory:
        count = len(by_category.get(category, []))
        if count > 0:
            print(f"    {category.value}: {count}")

    # Print issues grouped by file
    issues = [r for r in results if r.status in (
        ValidationStatus.BROKEN,
        ValidationStatus.PLACEHOLDER,
        ValidationStatus.TIMEOUT,
        ValidationStatus.ERROR
    )]

    if issues:
        print(f"\n{Colors.BOLD}Issues Found:{Colors.RESET}")
        print("-" * 70)

        # Group by source file
        by_file = defaultdict(list)
        for issue in issues:
            by_file[str(issue.link.source_file)].append(issue)

        for filepath, file_issues in sorted(by_file.items()):
            print(f"\n{Colors.BOLD}{filepath}{Colors.RESET}")
            for issue in file_issues:
                status_color = {
                    ValidationStatus.BROKEN: Colors.RED,
                    ValidationStatus.PLACEHOLDER: Colors.YELLOW,
                    ValidationStatus.TIMEOUT: Colors.YELLOW,
                    ValidationStatus.ERROR: Colors.RED,
                }.get(issue.status, '')

                print(f"  Line {issue.link.line_number}: {status_color}[{issue.status.value}]{Colors.RESET}")
                print(f"    URL: {issue.link.url[:70]}")
                print(f"    {issue.message}")
    else:
        print(f"\n{Colors.GREEN}No issues found!{Colors.RESET}")

    print("\n" + "=" * 70)


def generate_json_report(results: List[ValidationResult], output_path: Path) -> None:
    """
    Generate a JSON report.

    Args:
        results: List of validation results
        output_path: Path to write JSON file
    """
    # Build report structure
    report = {
        'generated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
        'summary': {
            'total': len(results),
            'by_status': {},
            'by_category': {}
        },
        'issues': [],
        'all_results': []
    }

    # Count by status and category
    for status in ValidationStatus:
        count = sum(1 for r in results if r.status == status)
        if count > 0:
            report['summary']['by_status'][status.value] = count

    for category in LinkCategory:
        count = sum(1 for r in results if r.link.category == category)
        if count > 0:
            report['summary']['by_category'][category.value] = count

    # Collect issues
    for r in results:
        if r.status in (ValidationStatus.BROKEN, ValidationStatus.PLACEHOLDER,
                        ValidationStatus.TIMEOUT, ValidationStatus.ERROR):
            report['issues'].append(r.to_dict())
        report['all_results'].append(r.to_dict())

    # Write JSON
    output_file = output_path.with_suffix('.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    print(f"JSON report written to: {output_file}")


def generate_markdown_report(results: List[ValidationResult], output_path: Path) -> None:
    """
    Generate a Markdown report.

    Args:
        results: List of validation results
        output_path: Path to write Markdown file
    """
    lines = []

    # Header
    lines.append("# Link Check Report")
    lines.append("")
    lines.append(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    # Summary
    lines.append("## Summary")
    lines.append("")
    lines.append(f"Total links scanned: **{len(results)}**")
    lines.append("")

    lines.append("### By Status")
    lines.append("")
    lines.append("| Status | Count |")
    lines.append("|--------|-------|")
    for status in ValidationStatus:
        count = sum(1 for r in results if r.status == status)
        if count > 0:
            lines.append(f"| {status.value} | {count} |")
    lines.append("")

    lines.append("### By Category")
    lines.append("")
    lines.append("| Category | Count |")
    lines.append("|----------|-------|")
    for category in LinkCategory:
        count = sum(1 for r in results if r.link.category == category)
        if count > 0:
            lines.append(f"| {category.value} | {count} |")
    lines.append("")

    # Issues
    issues = [r for r in results if r.status in (
        ValidationStatus.BROKEN,
        ValidationStatus.PLACEHOLDER,
        ValidationStatus.TIMEOUT,
        ValidationStatus.ERROR
    )]

    if issues:
        lines.append("## Issues")
        lines.append("")

        # Group by file
        by_file = defaultdict(list)
        for issue in issues:
            by_file[str(issue.link.source_file)].append(issue)

        for filepath, file_issues in sorted(by_file.items()):
            lines.append(f"### `{filepath}`")
            lines.append("")
            for issue in file_issues:
                status_emoji = {
                    ValidationStatus.BROKEN: ":x:",
                    ValidationStatus.PLACEHOLDER: ":warning:",
                    ValidationStatus.TIMEOUT: ":hourglass:",
                    ValidationStatus.ERROR: ":exclamation:",
                }.get(issue.status, "")

                lines.append(f"- **Line {issue.link.line_number}** {status_emoji} `{issue.status.value}`")
                lines.append(f"  - URL: `{issue.link.url}`")
                lines.append(f"  - {issue.message}")
            lines.append("")
    else:
        lines.append("## No Issues Found")
        lines.append("")
        lines.append("All links validated successfully!")

    # Write file
    output_file = output_path.with_suffix('.md')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"Markdown report written to: {output_file}")


# =============================================================================
# Auto-Fix Module
# =============================================================================

def get_github_username() -> str:
    """
    Get GitHub username from git config or return default.

    Returns:
        GitHub username string
    """
    try:
        result = subprocess.run(
            ['git', 'config', 'user.name'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass

    return "Digital-AI-Finance"


def fix_colab_username(
    filepath: Path,
    old_username: str,
    new_username: str,
    dry_run: bool = False
) -> Tuple[bool, int]:
    """
    Fix Colab URLs with placeholder usernames.

    Args:
        filepath: Path to the file to fix
        old_username: Placeholder username to replace
        new_username: New username to use
        dry_run: If True, don't actually modify files

    Returns:
        Tuple of (success, count of replacements)
    """
    if not filepath.suffix == '.ipynb':
        return False, 0

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Count replacements
        pattern = re.compile(re.escape(old_username), re.IGNORECASE)
        matches = pattern.findall(content)

        if not matches:
            return True, 0

        if dry_run:
            print(f"  Would replace {len(matches)} occurrence(s) in {filepath}")
            return True, len(matches)

        # Create backup
        backup_path = filepath.with_suffix('.ipynb.bak')
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # Replace
        new_content = pattern.sub(new_username, content)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"  Fixed {len(matches)} occurrence(s) in {filepath}")
        return True, len(matches)

    except Exception as e:
        print(f"{Colors.RED}Error fixing {filepath}: {e}{Colors.RESET}")
        return False, 0


def apply_fixes(
    results: List[ValidationResult],
    dry_run: bool = False,
    username: Optional[str] = None
) -> int:
    """
    Apply auto-fixes for known issues.

    Args:
        results: List of validation results
        dry_run: If True, only show what would be done
        username: GitHub username to use for Colab links

    Returns:
        Number of fixes applied
    """
    if username is None:
        username = get_github_username()

    print(f"\n{Colors.BOLD}Auto-Fix{Colors.RESET}")
    print(f"Using GitHub username: {username}")
    if dry_run:
        print(f"{Colors.YELLOW}DRY RUN - no changes will be made{Colors.RESET}")
    print()

    total_fixes = 0

    # Find placeholder issues
    placeholder_results = [
        r for r in results
        if r.status == ValidationStatus.PLACEHOLDER
    ]

    if not placeholder_results:
        print("No placeholder links found to fix.")
        return 0

    # Group by file
    by_file: Dict[Path, List[ValidationResult]] = defaultdict(list)
    for r in placeholder_results:
        by_file[r.link.source_file].append(r)

    # Placeholder patterns to fix
    placeholders_to_fix = ['YOUR_USERNAME', 'yourusername', 'your-username', 'YOUR-USERNAME']

    for filepath, file_results in by_file.items():
        for placeholder in placeholders_to_fix:
            success, count = fix_colab_username(filepath, placeholder, username, dry_run)
            if success:
                total_fixes += count

    print(f"\n{'Would apply' if dry_run else 'Applied'} {total_fixes} fix(es)")
    return total_fixes


# =============================================================================
# CLI Interface
# =============================================================================

def main():
    """Main entry point for the link checker."""
    parser = argparse.ArgumentParser(
        description="Link checker for Digital Finance course",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Scan current directory
  %(prog)s --path ./day_01          # Scan specific directory
  %(prog)s --skip-external          # Skip external URL validation
  %(prog)s --fix                    # Auto-fix placeholder usernames
  %(prog)s --fix --dry-run          # Preview fixes
  %(prog)s --format json            # JSON output only
  %(prog)s --verbose --timeout 15   # Verbose with custom timeout
        """
    )

    parser.add_argument(
        "--path", "-p",
        default=".",
        help="Root directory to scan (default: current directory)"
    )

    parser.add_argument(
        "--output", "-o",
        default="link_report",
        help="Output file base name (default: link_report)"
    )

    parser.add_argument(
        "--format", "-f",
        choices=["console", "json", "markdown", "all"],
        default="all",
        help="Output format (default: all)"
    )

    parser.add_argument(
        "--fix",
        action="store_true",
        help="Auto-fix known issues (placeholder usernames)"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what --fix would do without making changes"
    )

    parser.add_argument(
        "--username",
        help="GitHub username for Colab link fixes (default: from git config)"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )

    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=TIMEOUT,
        help=f"Request timeout in seconds (default: {TIMEOUT})"
    )

    parser.add_argument(
        "--skip-external",
        action="store_true",
        help="Skip external URL validation (faster)"
    )

    parser.add_argument(
        "--external-only",
        action="store_true",
        help="Only check external URLs"
    )

    args = parser.parse_args()

    # Resolve paths
    root_dir = Path(args.path).resolve()
    output_path = Path(args.output)

    if not root_dir.exists():
        print(f"{Colors.RED}Error: Directory not found: {root_dir}{Colors.RESET}")
        return 1

    print(f"{Colors.BOLD}Digital Finance Course - Link Checker{Colors.RESET}")
    print(f"Scanning: {root_dir}")
    print()

    # Discover links
    print("Discovering links...")
    links = discover_all_links(root_dir, verbose=args.verbose)
    print(f"Found {len(links)} links")

    # Filter if external-only
    if args.external_only:
        links = [l for l in links if l.category in (LinkCategory.EXTERNAL, LinkCategory.COLAB)]
        print(f"Filtered to {len(links)} external links")

    if not links:
        print("No links found to check.")
        return 0

    # Validate links
    print("\nValidating links...")
    validator = LinkValidator(root_dir, timeout=args.timeout, verbose=args.verbose)
    results = validator.validate_all_links(links, skip_external=args.skip_external)

    # Generate reports
    if args.format in ('console', 'all'):
        generate_console_report(results)

    if args.format in ('json', 'all'):
        generate_json_report(results, output_path)

    if args.format in ('markdown', 'all'):
        generate_markdown_report(results, output_path)

    # Apply fixes if requested
    if args.fix or args.dry_run:
        apply_fixes(results, dry_run=args.dry_run, username=args.username)

    # Determine exit code
    issues = [r for r in results if r.status in (
        ValidationStatus.BROKEN,
        ValidationStatus.PLACEHOLDER,
        ValidationStatus.ERROR
    )]

    if issues:
        print(f"\n{Colors.RED}Found {len(issues)} issue(s){Colors.RESET}")
        return 1
    else:
        print(f"\n{Colors.GREEN}All links OK!{Colors.RESET}")
        return 0


if __name__ == "__main__":
    exit(main())
