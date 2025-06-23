from playwright.sync_api import sync_playwright
import json
import matplotlib.pyplot as plt 

def fetch_data():
    with sync_playwright() as p:
        browser = p.webkit.launch()
        page = browser.new_page()
        page.goto("https://www.youtube.com/@midulive/videos")
        page.wait_for_selector(".badge-shape-wiz__text")
        times = [t.inner_text() for t in page.query_selector_all(".badge-shape-wiz__text")]
        times = times[::2 ]
        secs = []
        for t in times:
            m = int(t.split(":")[0]) * 60
            s = int(t.split(":")[1])
            secs.append(m + s)
        with open("data.txt", "a") as file:
            file.write(f"{secs}\n\n")
        views = page.wait_for_selector("#metadata-line")
        divs = page.locator("div#metadata-line")
        count = divs.count()
        amount_views = []
        for i in range(count):
            el = divs.nth(i)
            span = el.locator("span").first
            text = span.inner_text()
            print(text.split(" "))
            amount_views.append({"num": text.split(" ")[0].replace("\xa0k", ""), "currency": text.split(" ")[0][-1]})
        with open("data.txt", "a") as file:
            file.write(f"{amount_views}\n\n")
        print(secs)
        print(amount_views)

        browser.close()

# This data was saved into data.txt and then pasted into the .py file for better illustration:
seconds = [321, 873, 549, 600, 1188, 695, 498, 649, 731, 330, 966, 1038, 337, 434, 454, 704, 660, 787, 796, 802, 547, 805, 826, 1229, 878, 390, 262, 409]
views = [{'num': '58', 'currency': 'k'}, {'num': '95', 'currency': 'k'}, {'num': '62', 'currency': 'k'}, {'num': '52', 'currency': 'k'}, {'num': '125', 'currency': 'k'}, {'num': '58', 'currency': 'k'}, {'num': '25', 'currency': 'k'}, {'num': '86', 'currency': 'k'}, {'num': '115', 'currency': 'k'}, {'num': '59', 'currency': 'k'}, {'num': '78', 'currency': 'k'}, {'num': '154', 'currency': 'k'}, {'num': '28', 'currency': 'k'}, {'num': '63', 'currency': 'k'}, {'num': '54', 'currency': 'k'}, {'num': '68', 'currency': 'k'}, {'num': '41', 'currency': 'k'}, {'num': '72', 'currency': 'k'}, {'num': '55', 'currency': 'k'}, {'num': '56', 'currency': 'k'}, {'num': '70', 'currency': 'k'}, {'num': '81', 'currency': 'k'}, {'num': '87', 'currency': 'k'}, {'num': '115', 'currency': 'k'}, {'num': '110', 'currency': 'k'}, {'num': '81', 'currency': 'k'}, {'num': '53', 'currency': 'k'}, {'num': '53', 'currency': 'k'}]

views_mil = []


for item in views:
    if item["currency"] == "k":
        views_mil.append(int(item["num"]) * 1000)
    
import matplotlib.pyplot as plt

fig, axes = plt.subplots(figsize=(8.0, 5.0))

scatter = axes.scatter(x=seconds, y=views_mil, c=views_mil, cmap="viridis_r")

fig.colorbar(scatter, ax=axes)  # Añade la barra de color vinculada a ese scatter

title = "Relación segundos-vistas de los últimos 28 videos de @midulive (22-06-2025 23:49 GTM-6)"

axes.set_title(title, loc='center', wrap=True)
axes.set_ylabel("Vistas")
axes.set_xlabel("Segundos")
axes.text(200, -18000, "Fuente: https://www.youtube.com/@midulive/videos\nProyecto: Josué Arias G. Github: ariasj07")

plt.tight_layout()
plt.savefig("test1.png")
