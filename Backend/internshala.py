import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

total_data = {}

for number in range(1, 5):
    url = f"https://internshala.com/internships/css,react,javascript-internship/-{number}/"

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

        # # Locate all elements with the specified CSS selector
        # next_buttons = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"a[data-source_cta='view_details']")))

        # # Loop through each element
        # for next_button in next_buttons:
        #     print("Link: ", next_button.get_attribute('href'))
        #     # Append the link to the list
        #     links_list.append(next_button.get_attribute('href'))
            

        # print("All links:", links_list)

        # with open("all_links.txt","w") as file:
        #     for link in links_list:
        #         file.write(link + ',\n')



        # # for link in links_list:

        # #     new_driver = webdriver.Chrome() 
        # #     new_driver.get(link)
        # #     new_button = WebDriverWait(new_driver, 10).until(EC.element_to_be_clickable((By.ID, "no_thanks")))
        # #     print("first button: ", new_button)
        # #     new_button.click()

        # #     # Example scraping - you can replace this with your specific scraping logic
        # #     job_title = new_driver.find_element(By.CLASS_NAME,"profile_on_detail_page")
        # #     company_name = new_driver.find_element(By.CLASS_NAME,"link_display_like_text view_detail_button")
        # #     about = new_driver.find_element(By.CLASS_NAME,"text-container")

        # #     print("job title: ",job_title.get_attribute)
        # #     print("company name: ",company_name)
        # #     print("about : ",about)

        # #     driver.close()

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
        
        # Write links_list to a new text file

        with open(f'links{number}.txt', 'w') as file:
            for link in links_list:
                file.write(link + ',' +'\n')
        for link in links_list:
            with open(f'links{number}.txt','w') as file:
                file.write(link + ',' + '\n')
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

            company_name = soup.find(class_="link_display_like_text view_detail_button").get_text(strip=True)
                
                # Store data in dictionary
            # total_data[title] = {
            #     'skills': skills,
            #     'link': link
            # }
             # Store data in dictionary
            if company_name in total_data:
                total_data[company_name].append({
                    'title': title,
                    'skills': skills,
                    'link': link
                })
            else:
                total_data[company_name] = [{
                    'title': title,
                    'skills': skills,
                    'link': link
                }]



# def extract_data_from_link(link):
#     # Use requests library to access the link and extract data
#     response = requests.get(link)
#     soup = BeautifulSoup(response.content,'html.parser')
    
#     # title = soup.find_all(class_="profile_on_detail_page")
#     # print("Title: ",title)
#     # skills = soup.find_all(class_="round_tabs")
#     # print("Skills: ",skills)
#     # apply_link = link
#      # Find title
#     title = soup.find(class_="profile_on_detail_page").get_text(strip=True)
    
#     # Find skills
#     skills = [skill.get_text(strip=True) for skill in soup.find_all(class_="round_tabs")]
    
#     # Store data in dictionary
#     total_data[title] = {
#         'skills': skills,
#         'link': link
#     }.

# def extract_data_from_link(link):
    # Check if the link is empty or contains only whitespace characters
    

# def process_text_file(file_path):
#     with open(file_path, 'r') as file:
#         for line in file:
#             # Split each line by comma to get individual links
#             links = line.strip().split(',')
#             for link in links:
#                 # Process each link
#                 # extract_data_from_link(link.strip())
#                 print("link: ",link)
    
#                 if not link.strip():
#                     print("Empty or invalid link:", link)
#                     return
#                 print("Actual link: ",link)
#                 # Use requests library to access the link and extract data
#                 response = requests.get(link)
#                 soup = BeautifulSoup(response.content,'html.parser')
                
#                 # Find title
#                 title = soup.find(class_="profile_on_detail_page").get_text(strip=True)
                
#                 # Find skills
#                 skills = [skill.get_text(strip=True) for skill in soup.find_all(class_="round_tabs")]
                
#                 # Store data in dictionary
#                 total_data[title] = {
#                     'skills': skills,
#                     'link': link
#                 }

# # Example usage:
# for i in range(1,5):
#     text_file_path = f'./links{number}.txt'
#     process_text_file(text_file_path)
#     number = number + 1

with open("final_output.txt",'w') as file:
    json.dump(total_data,file)
# print(total_data)