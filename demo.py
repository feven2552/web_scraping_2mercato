import requests
from bs4 import BeautifulSoup

class Scraper:
    def init(self, url, bot_token, channel_id):
        self.url = url
        self.bot_token = bot_token
        self.channel_id = channel_id

    def scrape_data(self):
        data = []
        response = requests.get(self.url)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        paragraphs = soup.find_all('p')

        for paragraph in paragraphs:
            item = {}
            heading = paragraph.find_previous(['h3'])
            if heading:
                heading_text = heading.get_text()
                item['heading'] = heading_text
            paragraph_text = paragraph.get_text()
            item['paragraph'] = paragraph_text
            data.append(item)
        return data

    def post_to_telegram(self, data):
        base_url = f'https://api.telegram.org/bot{self.bot_token}/sendMessage'
        headers = {'Content-Type': 'application/json'}
        for item in data:
            message = ""
            if 'heading' in item:
                message += f"<b>{item['heading']}</b>\n"
            if 'paragraph' in item:
                message += f"{item['paragraph']}\n"
            if message:
                payload = {
                    'chat_id': self.channel_id,
                    'text': message,
                    'parse_mode': 'HTML'
                }
                requests.post(base_url, headers=headers, json=payload)

if name == 'main':
    url = 'https://www.2merkato.com'
    bot_token = '6247275701:AAHvVrfJRTek0cO9kYqw4PDmj-oat5YBTNk'
    channel_id = '-1001953447226'

    scraper = Scraper(url, bot_token, channel_id)
    data = scraper.scrape_data()
    scraper.post_to_telegram(data)