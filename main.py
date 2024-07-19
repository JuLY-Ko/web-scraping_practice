from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

with sync_playwright() as p:  
    browser = p.chromium.launch(headless=False)  
    page = browser.new_page()  
    
    page.goto("https://www.wanted.co.kr/search?query=flutter&tab=position")
    
    """
    time.sleep(5)
    # page.screenshot(path="screenshot.png")  # 스크린샷 저장
    page.click("button.Aside_searchButton__rajGo")
    # = page.locatoer("button.Aside_searchButton__rajGo").click()
    time.sleep(5)
    page.get_by_placeholder("검색어를 입력해 주세요.").fill("flutter")
    time.sleep(5)
    # page.keyboard().down("Enter")
    page.keyboard.down("Enter")
    time.sleep(10)
    page.click("a#search_tab_position")
    """ 
    for x in range(5):
        time.sleep(5)
        page.keyboard.down("End")

    content = (page.content())
    soup = BeautifulSoup(content, "html.parser")

    jobs = soup.find_all("div", class_="JobList_container__Hv_EA")
    jobs_db = []
    for job in jobs:
        a_tag = job.find('a')
        link = f"https://www.wanted.co.kr{a_tag['href']}" if a_tag and 'href' in a_tag.attrs else "No link"

        title_tag = job.find("strong", class_="JobCard_title__HBpZf")
        title = title_tag.text if title_tag else "No title"

        company_tag = job.find("span", class_="JobCard_companyName__N1YrF")
        company_name = company_tag.text if company_tag else "No company name"

        reward_tag = job.find("span", class_="JobCard_reward__cNlG5")
        reward = reward_tag.text if reward_tag else "No reward"
        job = {
            "title": title,
            "company_name": company_name,
            "reward": reward,
            "link": link
        }
        jobs_db.append(job)
   


with open("jobs.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Company Name", "Reward", "Link"])  # 헤더 작성

        for job in jobs_db:
            writer.writerow(job.values())

print(jobs_db)
print(len(jobs_db))


    

