from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
import os

# Шлях до веб-драйвера
driver_path = 'C:\Users\пк\Documents\generator\drivers\chromedriver.exe'  # Змініть на шлях до вашого chromedriver

# Ініціалізація веб-драйвера
driver = webdriver.Chrome(driver_path)

# Функція для генерації зображення на основі промпту та збереження його
def generate_image_and_download(prompt, folder="images", width=1920, height=1080, seed=232043480):
    # Відкриваємо веб-сторінку генерації зображень
    driver.get("https://image.pollinations.ai")

    # Знаходимо поле вводу для промпту
    input_element = driver.find_element(By.NAME, "prompt")  # Потрібно змінити, якщо на сторінці інший селектор для поля вводу
    input_element.clear()  # Очищаємо поле вводу, якщо там щось є

    # Вводимо промпт в поле
    input_element.send_keys(prompt)
    input_element.send_keys(Keys.RETURN)  # Надсилаємо запит, натискаючи Enter

    # Чекаємо на результат
    time.sleep(5)  # Чекаємо, поки згенерується зображення (можна замінити на WebDriverWait для точнішої синхронізації)

    # Генерація URL для зображення з потрібними параметрами
    image_url = f"https://image.pollinations.ai/prompt/{prompt}?width={width}&height={height}&seed={seed}&model=flux"

    # Завантажуємо зображення за допомогою requests
    response = requests.get(image_url)
    
    if response.status_code == 200:
        # Створюємо папку для збереження зображень, якщо її немає
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        # Формуємо шлях до збереження зображення
        image_filename = os.path.join(folder, f"{prompt[:10]}.jpg")  # Наприклад, беремо перші 10 символів промпту як ім'я файлу
        
        # Записуємо зображення в файл
        with open(image_filename, 'wb') as file:
            file.write(response.content)
        
        print(f"Зображення збережене як {image_filename}")
    else:
        print("Не вдалося завантажити зображення.")

# Функція для обробки текстового файлу з промптами
def process_prompts(file_name):
    with open(file_name, 'r') as file:
        prompts = file.readlines()
    
    for prompt in prompts:
        prompt = prompt.strip()  # Вилучаємо зайві пробіли та нові рядки
        if prompt:
            generate_image_and_download(prompt)  # Генеруємо та завантажуємо зображення

# Запускаємо обробку промптів з файлу
process_prompts("prompts.txt")

# Закриваємо браузер після виконання
driver.quit()