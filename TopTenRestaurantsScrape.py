import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to convert review count text into an integer
def convert_review_count(review_text):
    review_text = review_text.replace(" reviews", "").replace(",", "").replace("(", "").replace(")", "")
    if review_text.endswith("K"):  # Convert thousands to integer
        return int(float(review_text[:-1]) * 1000)
    elif review_text.endswith("M"):  # Convert millions to integer
        return int(float(review_text[:-1]) * 1000000)
    try:
        return int(review_text)  # Convert plain numbers
    except ValueError:
        return 0  # Return 0 if conversion fails

# Function to save extracted data into a JSON file
def save_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def main():
    # Get user input for the city name
    city = input("Enter the city name: ").strip()
    search_query = f"top ten restaurants {city}"
    chrome_driver_path = "P:/eclipse workspace/drivers/chromedriver-win64/chromedriver.exe"  # Path to Chrome driver
    
    # Set Chrome options to prevent detection as an automated bot
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    # Initialize the Chrome driver
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 10)  # Set explicit wait time
    
    try:
        # Open Google search
        driver.get("https://www.google.com/")
        driver.maximize_window()
        
        # Locate the search bar and enter the query
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
        search_box.send_keys(search_query)
        search_box.submit()
        
        # Click on 'More places' to see more restaurant listings
        try:
            more_places_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space(text())='More places']")))
            more_places_button.click()
        except Exception:
            input("CAPTCHA detected! Please solve it manually and press Enter to continue...")
        
        # Extract restaurant names
        restaurant_names = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[@class='OSrXXb']")))
        ratings_list = []
        
        # Extract ratings for each restaurant
        for i in range(1, len(restaurant_names) + 1):
            try:
                rating_element = driver.find_element(By.XPATH, f"(//span[@class='Y0A0hc'])[{i}]")
                rating_text = rating_element.text.strip().split("(")[0].strip()
                ratings_list.append(rating_text)
            except Exception:
                ratings_list.append("0")  # Default to 0 if rating is not found
        
        # Extract review counts for each restaurant
        review_elements = driver.find_elements(By.XPATH, "//span[@class='RDApEe YrbPuc']")
        review_list = [convert_review_count(review.text.strip()) for review in review_elements]
        restaurant_data = {}
        
        count = 0  # Counter to track top 10 restaurants
        for i in range(len(restaurant_names)):
            if count >= 10:
                break  # Stop after collecting 10 restaurants
            try:
                rating = float(ratings_list[i])
                review_count = review_list[i]
                
                # Filter restaurants with rating above 4.0 and more than 1000 reviews
                if rating > 4.0 and review_count > 1000:
                    formatted_value = f"Ratings: {ratings_list[i]}, Reviews: {review_count}"
                    numbered_name = f"{count + 1}. {restaurant_names[i].text}"  # Numbered restaurant name
                    restaurant_data[numbered_name] = formatted_value
                    count += 1
            except ValueError:
                print(f"Skipping invalid data: {ratings_list[i]}, {review_list[i]}")
        
        # Save the extracted data to a JSON file
        file_path = "P:/eclipse workspace/json/top_ten_restaurants.json"
        save_to_json(restaurant_data, file_path)
        print(f"Data saved successfully to {file_path}")
        
        # Display the results to the user
        print("Top 10 Restaurants:")
        for name, details in restaurant_data.items():
            print(f"{name} -> {details}")
        
    except Exception as e:
        print(e)  # Print any encountered error
    finally:
        driver.quit()  # Ensure the browser closes at the end

if __name__ == "__main__":
    main()
