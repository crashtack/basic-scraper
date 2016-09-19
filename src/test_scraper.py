def test_load_inspection_page():
    from scraper import load_inspection_page
    data, encoding = load_inspection_page('inspection_page.html')
    assert data.__sizeof__() > 0
