from setup import build_nginx_download_url, extract_latest_nginx_version


def test_build_nginx_download_url_uses_expected_zip_link() -> None:
    assert build_nginx_download_url("1.27.5") == "https://nginx.org/download/nginx-1.27.5.zip"


def test_extract_latest_nginx_version_from_list_page() -> None:
    html = """
    <html>
      <body>
        <a href="nginx-1.27.5.zip">nginx-1.27.5.zip</a>
        <a href="nginx-1.26.3.zip">nginx-1.26.3.zip</a>
      </body>
    </html>
    """
    assert extract_latest_nginx_version(html) == "1.27.5"
