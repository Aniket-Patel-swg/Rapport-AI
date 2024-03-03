from flask import Flask, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

app = Flask(__name__)
CORS(app)

print("Server is runing on ")

# Define a route to start scraping
@app.route('/start_internshala', methods=['GET'])
def start_scraping():
   
    total_data = {}
    data_list =[]

    for number in range(2, 3):
        url = f"https://internshala.com/internships/css,natural-language-processing-nlp,react-internship/page-{number}/"

        response = requests.get(url)
        soup = BeautifulSoup(response.content,'html.parser')

        driver = webdriver.Chrome()

        driver.get(f"https://internshala.com/internships/page-{number}/")

        # Wait for the 'no thanks' button and click it
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "no_thanks")))
        print("first button: ", button)
        button.click()

        if response.status_code == 200:
            print('now website is open')
            
            # Initialize an empty list to store the links
            links_list = []

            while True:  # Loop indefinitely
                # Locate all elements with the specified CSS selector
                next_buttons = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"a[data-source_cta='view_details']")))

                # Loop through each element
                for next_button in next_buttons:
                    if (next_button.get_attribute('href')):
                        print("Link: ", next_button.get_attribute('href'))
                    # Append the link to the list
                    
                        links_list.append(next_button.get_attribute('href'))

                try:
                    # Find the next button to navigate to the next page
                    next_button = driver.find_element(By.ID, "next")
                    # Click the next button
                    print("next button",next_button)
                    next_button.click()

                    
                    time.sleep(2)
                    
                    next_close_button = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"a[data-source_cta='view_details']")))
                    print("next close button: ",next_close_button)
                    next_close_button.click()
                    # Wait for a short duration to ensure the page is loaded
                    time.sleep(2)
                except:
                    # If no next button is found, break the loop
                    break

            print("All links:", links_list)
            
         
            for link in links_list:
                if not link.strip():
                    print("Empty or invalid link:", link)
                print("Actual link: ",link)
                        # Use requests library to access the link and extract data
                response = requests.get(link)
                soup = BeautifulSoup(response.content,'html.parser')
                        
                        # Find title
                title = soup.find(class_="profile_on_detail_page").get_text(strip=True)
                    
                    # Find skills
                skills = [skill.get_text(strip=True) for skill in soup.find_all(class_="round_tabs")]

                job_position = soup.find(class_="heading_2_4 heading_title").get_text(strip=True)

                company_name = soup.find(class_="link_display_like_text view_detail_button").get_text(strip=True)
                
                if company_name in total_data:
                    total_data[company_name].append({
                        'title': title,
                        'skills': skills,
                        'position': job_position,
                        'link': link
                    })
                else:
                    total_data[company_name] = [{
                        'title': title,
                        'skills': skills,
                        'position': job_position,
                        'link': link
                    }]

                entry = {
                    'company': company_name,
                    'title': title,
                    'skills': skills,
                    'link': link
                }

                # Append the entry to the list
                data_list.append(entry)    

            # with open("final_output.txt",'w') as file:
            #     json.dump(total_data,file)   

            # with open("list_output.txt",'w') as file:
            #     json.dump(data_list,file)
    
    # Once scraping is complete, you can return a response
    json_data = jsonify(data_list)
    print("json: ",json_data)

    # Once scraping is complete, return the JSON data
    return json_data

if __name__ == '__main__':
    app.run(debug=True)
