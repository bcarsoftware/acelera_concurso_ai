from playwright.async_api import async_playwright


async def law_page_content(law_link: str) -> str:
    async with async_playwright() as p:
        browser_type = p.chromium
        browser = await browser_type.launch()
        page = await browser.new_page()
        await page.goto(law_link)
        content = await page.wait_for_selector("body")
        data = await content.text_content()
        data = data.strip().replace("\n", " ").replace("\t", "")

        data = data.strip()
        await browser.close()

    return data
