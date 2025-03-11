# TopRestaurants
Problem Statement:

Develop a Python script that fulfills the following requirements:
Prompt the user to enter the name of a city.
Retrieve the top 10 restaurants in the specified city based on the food, comparing ratings and reviews through a Google search.
Store the collected restaurant data in a JSON file, using the restaurant names as keys and their relevant details (such as ratings and reviews) as values.
-----------------------------------------------------------------------------------------------------------------------------------------
Approach:
Web Scraping Setup:
Uses Selenium WebDriver to automate a search query on Google.
Sets Chrome options to prevent bot detection.
Implements explicit waits (WebDriverWait) instead of sleep() for efficient element loading.

Fetching Data:
Inputs the city name from the user and searches for "top ten restaurants [city]".
Extracts restaurant names, ratings, and review counts using XPath selectors.

Filtering & Storing Data:
Filters restaurants with ratings above 4.0 and more than 1000 reviews.
Saves the extracted data in a JSON file.

Handling Edge Cases:
Includes exception handling for missing elements.
Detects CAPTCHAs
Converts review counts (e.g., "2K", "1.5M") into integer values.

Challenges:

CAPTCHA Handling:
Google may detect automated scraping and prompt a CAPTCHA.
The script pauses and requires manual intervention to proceed.

Dynamic Page Structure:
Google frequently updates its UI, potentially breaking XPath locators.
May require periodic updates to adapt to changes.

Rate Limits & Bot Detection:
Excessive requests can trigger Google’s anti-bot measures.
Solution: Use rotating user-agents and delays between requests if needed.

Data Inconsistencies:
Some restaurants may have missing ratings or review counts.
The script defaults to 0 if values are unavailable.
