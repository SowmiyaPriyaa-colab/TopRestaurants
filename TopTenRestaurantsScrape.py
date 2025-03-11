import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def convert_review_count(review_text):
    review_text = review_text.replace(" reviews", "").replace(",", "").replace("(", "").replace(")", "")
    if review_text.endswith("K"):
        return int(float(review_text[:-1]) * 1000)
    elif review_text.endswith("M"):
        return int(float(review_text[:-1]) * 1000000)
    try:
        return int(review_text)
    except ValueError:
        return 0


def save_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def human_like_scroll(driver):
    for _ in range(random.randint(2, 5)):
        driver.execute_script("window.scrollBy(0, arguments[0]);", random.randint(200, 500))
        time.sleep(random.uniform(2, 5))

def main():
    city = input("Enter the city name: ").strip()
    search_query = f"top ten restaurants {city}"
    chrome_driver_path = "P:/eclipse workspace/drivers/chromedriver-win64/chromedriver.exe"
    
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get("https://www.google.com/")
        driver.maximize_window()
        time.sleep(3)
        
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(search_query)
        search_box.submit()
        time.sleep(5)
        
        try:
            driver.find_element(By.XPATH, "//span[normalize-space(text())='More places']").click()
        except Exception:
            input("CAPTCHA detected! Please solve it manually and press Enter to continue...")
        
        time.sleep(5)
        human_like_scroll(driver)
        
        restaurant_names = driver.find_elements(By.XPATH, "//span[@class='OSrXXb']")
        ratings_list = []
        
        for i in range(1, len(restaurant_names) + 1):
            try:
                rating_element = driver.find_element(By.XPATH, f"(//span[@class='Y0A0hc'])[{i}]")
                rating_text = rating_element.text.strip().split("(")[0].strip()
                ratings_list.append(rating_text)
            except Exception:
                ratings_list.append("0")
        
        review_elements = driver.find_elements(By.XPATH, "//span[@class='RDApEe YrbPuc']")
        review_list = [convert_review_count(review.text.strip()) for review in review_elements]
        restaurant_data = {}
        
        
        count = 0
        for i in range(len(restaurant_names)):
            if count >= 10:
                break
            try:
                rating = float(ratings_list[i])
                review_count = review_list[i]
                
                if rating > 4.0 and review_count > 1000:
                    formatted_value = f"Ratings: {ratings_list[i]}, Reviews: {review_count}"
                    numbered_name = f"{count + 1}. {restaurant_names[i].text}"  
                    restaurant_data[numbered_name] = formatted_value
                    count+=1
            except ValueError:
                print(f"Skipping invalid data: {ratings_list[i]}, {review_list[i]}")
        
        file_path = "P:/eclipse workspace/json/top_ten_restaurants.json"
        save_to_json(restaurant_data, file_path)
        print(f"Data saved successfully to {file_path}")
        print("Top 10 Restaurants:")
        for name, details in restaurant_data.items():
            print(f"{name} -> {details}")
        
    except Exception as e:
        print(e)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
