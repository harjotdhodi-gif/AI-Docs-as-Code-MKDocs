from __future__ import annotations

from bs4 import BeautifulSoup


def modify_html(html: str, href: str) -> str:
    """Reduce a Material page to its document content before WeasyPrint renders it."""
    soup = BeautifulSoup(html, "html.parser")

    for selector in (
        "header.md-header",
        "nav.md-tabs",
        ".md-sidebar",
        "footer.md-footer",
        ".md-top",
        ".md-dialog",
        ".md-search",
        ".md-content__button",
        ".md-source-file",
        "script",
        "noscript",
    ):
        for node in soup.select(selector):
            node.decompose()

    article = soup.select_one("article.md-content__inner")
    body = soup.body
    if article is not None and body is not None:
        article = article.extract()
        body.clear()
        wrapper = soup.new_tag("main")
        wrapper["class"] = ["pdf-document"]
        wrapper.append(article)
        body.append(wrapper)

    return str(soup)


def get_stylesheet() -> str:
    """Return print-specific CSS for clean, readable, per-page PDF exports."""
    return r"""
    @page {
      size: A4 portrait;
      margin: 18mm 16mm 20mm;
      @top-left {
        content: "Scriptorium Lab Services Documentation";
        color: #5f5a55;
        font-family: "DejaVu Sans", Arial, sans-serif;
        font-size: 8.5pt;
      }
      @top-right {
        content: "Page " counter(page);
        color: #5f5a55;
        font-family: "DejaVu Sans", Arial, sans-serif;
        font-size: 8.5pt;
      }
      @bottom-left {
        content: "Copyright © 2026, SCRIPTORIUM LAB SERVICES FZCO.";
        color: #77716b;
        font-family: "DejaVu Sans", Arial, sans-serif;
        font-size: 7.5pt;
      }
    }

    html,
    body,
    .pdf-document,
    article.md-content__inner {
      width: auto !important;
      max-width: none !important;
      min-height: 0 !important;
      margin: 0 !important;
      padding: 0 !important;
      color: #222222 !important;
      font-family: "DejaVu Sans", Arial, sans-serif !important;
      font-size: 10.5pt !important;
      line-height: 1.55 !important;
      background: #ffffff !important;
      background-image: none !important;
      border: 0 !important;
      box-shadow: none !important;
    }

    .pdf-document::before,
    .pdf-document::after,
    article.md-content__inner::before,
    article.md-content__inner::after,
    .help-home__hero-art,
    .md-main::before,
    .md-main::after {
      display: none !important;
      content: none !important;
    }

    h1 {
      margin: 0 0 10pt !important;
      color: #1d2748 !important;
      font-family: "DejaVu Serif", Georgia, serif !important;
      font-size: 23pt !important;
      font-weight: 400 !important;
      line-height: 1.18 !important;
      break-after: avoid;
      page-break-after: avoid;
    }

    h2 {
      margin: 17pt 0 7pt !important;
      color: #24211f !important;
      font-size: 16pt !important;
      font-weight: 600 !important;
      line-height: 1.25 !important;
      break-after: avoid;
      page-break-after: avoid;
    }

    h3 {
      margin: 13pt 0 5pt !important;
      color: #312d2a !important;
      font-size: 12.5pt !important;
      font-weight: 650 !important;
      break-after: avoid;
      page-break-after: avoid;
    }

    p,
    li {
      font-size: 10.5pt !important;
      line-height: 1.55 !important;
    }

    p {
      margin: 0 0 8pt !important;
    }

    a {
      color: #075f7d !important;
      text-decoration: underline !important;
    }

    pre,
    code {
      font-family: "DejaVu Sans Mono", monospace !important;
    }

    pre {
      padding: 8pt !important;
      white-space: pre-wrap !important;
      overflow-wrap: anywhere !important;
      background: #f2f4f5 !important;
      border: 0.6pt solid #d1d6d8 !important;
      break-inside: avoid;
      page-break-inside: avoid;
    }

    table {
      width: 100% !important;
      border-collapse: collapse !important;
      font-size: 8.8pt !important;
      break-inside: avoid;
      page-break-inside: avoid;
    }

    th,
    td {
      padding: 5pt !important;
      vertical-align: top !important;
      border: 0.6pt solid #c8cdcf !important;
    }

    th {
      background: #eef1f2 !important;
    }

    img,
    svg {
      max-width: 100% !important;
      height: auto !important;
      break-inside: avoid;
      page-break-inside: avoid;
    }

    .admonition,
    details,
    blockquote,
    .help-home__catalog-card,
    .help-home__service,
    .help-home__assurance {
      margin: 9pt 0 !important;
      padding: 8pt 10pt !important;
      color: #222222 !important;
      background: #f7f8f8 !important;
      border: 0.8pt solid #cfd5d7 !important;
      box-shadow: none !important;
      break-inside: avoid;
      page-break-inside: avoid;
    }

    .help-home,
    .help-home__hero,
    .help-home__catalog,
    .help-home__services,
    .help-home__catalog-grid,
    .help-home__service-grid,
    .help-home__link-columns,
    .help-home__assurance,
    .help-home__hero-inner {
      display: block !important;
      width: auto !important;
      max-width: none !important;
      min-height: 0 !important;
      margin: 0 !important;
      padding: 0 !important;
      color: #222222 !important;
      background: #ffffff !important;
      background-image: none !important;
      border: 0 !important;
      box-shadow: none !important;
    }

    .help-home__eyebrow,
    .help-home__lead,
    .help-home h1 {
      color: #222222 !important;
    }

    .help-home__search,
    .md-button {
      display: none !important;
    }
    """
