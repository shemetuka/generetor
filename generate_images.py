from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import os

# Шлях до веб-драйвера
driver_path = "C:/tools/chromedriver-win64/chromedriver.exe"  # Змініть на шлях до вашого chromedriver

# Ініціалізація опцій для Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Запуск без графічного інтерфейсу
chrome_options.add_argument("--no-sandbox")  # Для Linux-систем

# Створення об'єкта Service для передавання шляху до chromedriver
service = Service(driver_path)

# Ініціалізація веб-драйвера з опціями
driver = webdriver.Chrome(service=service, options=chrome_options)

# Функція для генерації зображення на основі промпту та збереження його
def generate_image_and_download(prompt, folder="images", width=1920, height=1080, seed=232043480):
    driver.get("https://pollinations.ai")

    try:
        # Чекаємо, поки елемент з'явиться на сторінці
        input_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea"))
        )
        input_element.clear()
        input_element.send_keys(prompt)
        input_element.send_keys(Keys.RETURN)

        time.sleep(5)  # Можна замінити на WebDriverWait для точнішої синхронізації

        # Генерація URL для зображення
        image_url = f"https://image.pollinations.ai/prompt/{prompt}?width={width}&height={height}&seed={seed}&model=flux"
        response = requests.get(image_url)

        if response.status_code == 200:
            if not os.path.exists(folder):
                os.makedirs(folder)

            image_filename = os.path.join(folder, f"{prompt[:10]}.jpg")
            with open(image_filename, 'wb') as file:
                file.write(response.content)
            
            print(f"Зображення збережене як {image_filename}")
        else:
            print("Не вдалося завантажити зображення.")
    except Exception as e:
        print(f"Помилка при роботі з елементом: {str(e)}")

# Функція для обробки текстового файлу з промптами
def process_prompts(file_name):
    with open(file_name, 'r') as file:
        prompts = file.readlines()

    for prompt in prompts:
        prompt = prompt.strip()
        if prompt:
            generate_image_and_download(prompt)

process_prompts("prompts.txt")
driver.quit()
