import selenium
from selenium import webdriver
from time import sleep
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt

transcripts =[]
views =[]
likes = []
dis_likes =[]
Title =[]
length = []
coments=[]

# chromedriver give your executable path
my_driver = "chromedriver.exe"
def london(url):
    # un comment the first driver for relative path and comment the second driver
    # driver = webdriver.Chrome(my_driver)
    driver = webdriver.Chrome(executable_path=r'C:\Users\User\Downloads\chromedriver_win32\chromedriver.exe')
    
    # url="https://www.youtube.com/watch?v=YXN_lNZZAZA&ab_channel=Kontor.TV"
    # url="https://www.youtube.com/watch?v=6LD30ChPsSs&ab_channel=ThinkMusicIndia"
    # url = "https://www.youtube.com/watch?v=_TFribViDSs&ab_channel=AshStudio7"
    driver.get(url)

    sleep(2)

    # accept the cookies 
    cookies = driver.find_element_by_xpath('/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[2]/div[2]/div[5]/div[2]/ytd-button-renderer[2]/a/tp-yt-paper-button')
    cookies.click()

    sleep(2)

    # no of video views 
    view=driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[6]/div[2]/ytd-video-primary-info-renderer/div/div/div[1]/div[1]/ytd-video-view-count-renderer/span[1]')
    views.append(view.text)
    # no of video likes 
    like =driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[6]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div/ytd-toggle-button-renderer[1]/a/yt-formatted-string')
    likes.append(like.text)
    # no of video dislikes 
    dis_like =driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[6]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div/ytd-toggle-button-renderer[2]/a/yt-formatted-string')
    dis_likes.append(dis_like.text)
    # title of the video 
    title =driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[6]/div[2]/ytd-video-primary-info-renderer/div/h1/yt-formatted-string')
    Title.append(title.text)
    # length of the video
    len_video = driver.find_element_by_xpath('//span[@class="ytp-time-duration"]')
    length.append(len_video.text)

    sleep(2)
    # to open the  transcripts
    dots=driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[6]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/yt-icon-button/button/yt-icon')
    dots.click()
    
    sleep(1)
    # to check whether the video has transcription or not!
    check_trans = driver.find_element_by_xpath("/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-menu-popup-renderer").text
    
    print(check_trans)
    if 'transcript' in check_trans:
        print('Yes! It has transcript')
        sleep(1)
        trans=driver.find_element_by_xpath('/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-menu-popup-renderer/tp-yt-paper-listbox/ytd-menu-service-item-renderer/tp-yt-paper-item/yt-formatted-string')
        trans.click()
        sleep(1)
        # timestamps of the transcripts
        dots_trans = driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[2]/div/div[1]/ytd-engagement-panel-section-list-renderer/div[1]/ytd-engagement-panel-title-header-renderer/div[2]/div[5]/ytd-menu-renderer/yt-icon-button/button/yt-icon')
        dots_trans.click()
        sleep(1)
        timestamps = driver.find_element_by_xpath('/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-menu-popup-renderer/tp-yt-paper-listbox/ytd-menu-service-item-renderer/tp-yt-paper-item/yt-formatted-string')
        timestamps.click()
        sleep(1)
        # transcription adding to the empty list
        trans_desc =driver.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[2]/div/div[1]/ytd-engagement-panel-section-list-renderer/div[2]/ytd-transcript-renderer/div[1]").text
        transcripts.append(trans_desc)
        data ={'Title':Title,'Likes':likes,'Dis_Likes':dis_likes,'No_Of_Views':views,'Transcripts':transcripts,'Video_length':length}
    else:
        print('no! It has no transcript')
        data ={'Title':Title,'Likes':likes,'Dis_Likes':dis_likes,'No_Of_Views':views,'Video_length':length}
    
    # no of comments for the video
    # coment = driver.find_element_by_xpath('//span[@class="style-scope yt-formatted-string"]')
    # coments.append(coment.text)
    # print(coment.text)
    
    #  to stop the video
    stop_play = driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div/div/div/ytd-player/div/div/div[1]/video')
    stop_play.click()
    
    df = pd.DataFrame(data)
    df['No_Of_Views'] = df['No_Of_Views'].str.replace('views', '')
    # print(df)
    # adding to the csv file
    # df.to_csv("Name of the file1.txt")
    # print(coments)
    return print(df)

url="https://www.youtube.com/watch?v=YXN_lNZZAZA&ab_channel=Kontor.TV"
# url="https://www.youtube.com/watch?v=zMFb8Y2QLPc&ab_channel=Olympics"
# url="https://www.youtube.com/watch?v=6LD30ChPsSs&ab_channel=ThinkMusicIndia"
london(url)
