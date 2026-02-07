"""HTML processing: text modification (™), link and form rewriting for proxy."""

from bs4 import BeautifulSoup
from bs4.element import NavigableString

from app.logger import get_logger
from app.utils.text import add_trademark
from config.settings import settings

logger = get_logger(__name__)


def _add_trademark_to_text_nodes(soup: BeautifulSoup) -> None:
    """Add ™ after 6-letter words in all text nodes (except script/style).

    Args:
        soup: BeautifulSoup object to process.
    """
    for element in soup.find_all(string=True):
        if (
            isinstance(element, NavigableString)
            and element.parent
            and element.parent.name not in ("script", "style")
        ):
            try:
                new_text = add_trademark(str(element))
                element.replace_with(new_text)
            except Exception as e:
                logger.warning(
                    "Failed to add trademark to text node",
                    extra={"error": str(e)},
                )
                # Continue processing other nodes


def _is_hn_url(url: str) -> bool:
    """Return True if URL belongs to HN (avoid rewriting other hosts).

    Args:
        url: URL to check.

    Returns:
        True if URL belongs to HN domain.
    """
    if not url or not isinstance(url, str):
        return False
    base = settings.hn_base_url.rstrip("/")
    return url == base or url.startswith(base + "/")


def _rewrite_links(soup: BeautifulSoup, proxy_url: str) -> None:
    """Rewrite href in links to proxy URL (relative and full HN URLs).

    Args:
        soup: BeautifulSoup object to process.
        proxy_url: Proxy base URL for rewriting.
    """
    for link in soup.find_all("a", href=True):
        try:
            href = link.get("href", "")
            if not href:
                continue
            if href.startswith("/"):
                link["href"] = f"{proxy_url}{href}"
            elif _is_hn_url(href):
                link["href"] = href.replace(
                    settings.hn_base_url.rstrip("/"), proxy_url
                )
        except Exception as e:
            logger.warning(
                "Failed to rewrite link",
                extra={"href": str(link.get("href", "")), "error": str(e)},
            )


def _rewrite_forms(soup: BeautifulSoup, proxy_url: str) -> None:
    """Rewrite form action to proxy URL.

    Args:
        soup: BeautifulSoup object to process.
        proxy_url: Proxy base URL for rewriting.
    """
    base = settings.hn_base_url.rstrip("/")
    for form in soup.find_all("form", action=True):
        try:
            action = form.get("action", "")
            if not action:
                continue
            if action.startswith("/"):
                form["action"] = f"{proxy_url}{action}"
            elif _is_hn_url(action):
                form["action"] = action.replace(base, proxy_url)
        except Exception as e:
            logger.warning(
                "Failed to rewrite form action",
                extra={"action": str(form.get("action", "")), "error": str(e)},
            )


def process_html(html: str, proxy_url: str) -> str:
    """Parse HTML, add ™ to text, rewrite links and forms; return HTML string.

    Args:
        html: HTML content to process.
        proxy_url: Proxy base URL for rewriting links.

    Returns:
        Processed HTML string.

    Raises:
        ValueError: If HTML is invalid or processing fails.
    """
    if not html or not html.strip():
        return html

    if not proxy_url or not isinstance(proxy_url, str):
        logger.warning("Invalid proxy_url", extra={"proxy_url": proxy_url})
        return html

    try:
        soup = BeautifulSoup(html, "lxml")
        _add_trademark_to_text_nodes(soup)
        _rewrite_links(soup, proxy_url)
        _rewrite_forms(soup, proxy_url)
        return str(soup)
    except Exception as e:
        logger.error(
            "Failed to process HTML",
            extra={"error": str(e), "html_length": len(html)},
            exc_info=True,
        )
        return html
