from selenium import webdriver
import time
import subprocess
import os
import random
import tkinter as tk
from tkinter import ttk
from tkinter import Menu

# UI initialisation
win = tk.Tk()
win.title("Linked In Downloader")

# Object to configure Chrome
options = webdriver.ChromeOptions()

# Start Chrome in headless mode
# options.add_argument('headless')
options.add_argument('--mute-audio')

# Set window size of Chrome
options.add_argument('window-size=1200x600')

# Define variable 'driver' and apply the predefined options
driver = webdriver.Chrome('/Applications/chromedriver', options=options)


# try:
def site_login():
    driver.get("https://www.linkedin.com/uas/login?fromSignIn=true&trk=learning&_l=de_DE&uno_session_redirect=%2Flearning%2Fme&session_redirect=%2Flearning%2FloginRedirect.html&is_enterprise_authed=")
    if driver.find_elements_by_css_selector('#username'):
        print("username exists")
        driver.find_element_by_id("username").send_keys(login_mail.get())
        driver.find_element_by_id("password").send_keys(login_pw.get())
        time.sleep(3)
        if driver.find_elements_by_css_selector("[type='submit']")[0]:
            print("button was input")
            print(driver.find_elements_by_css_selector("[type='submit']")[0].get_attribute("class"))
            driver.find_elements_by_css_selector("[type='submit']")[0].click()
        else:
            driver.find_element_by_css_selector("button[type='submit']").click()
            print("button was button")
    else:
        print("session_key-login exists")
        driver.find_element_by_id("session_key-login").send_keys(login_mail.get())
        driver.find_element_by_id("session_password-login").send_keys(login_pw.get())
        driver.find_element_by_css_selector("input[type='submit']").click()


def link_count():
    video_list = driver.find_elements_by_css_selector("a.toc-item")
    link_counter = len(video_list)
    print(link_counter)
    return link_counter


def notify_progress(title, subtitle, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}" subtitle "{}"'
              """.format(text, title, subtitle))


def input_dialog():
    # try:
        siteurl = subprocess.check_output(['osascript', '-e', \
                                           r'''set theText to text returned of (display dialog "Please insert URL here:" default answer "" with title "exchange to python" with icon 1)'''])

        topic = subprocess.check_output(['osascript', '-e', \
                                           r'''set theText to text returned of (display dialog "Please insert topic here:" default answer "" with title "exchange to python" with icon 1)'''])

        url_new = siteurl.decode('UTF-8')
        topic_new = topic.decode('UTF-8')
        print(topic_new)
        filename = "/Users/Marco/Documents/" + topic_new + ".txt"
        f = open(filename, "a")
        f.write("URL zum Tutorial: " + url_new)
        f.write("=====================================================\n\n\n")

        driver.get(url_new)
        time.sleep(3)
        # play_button = driver.find_elements_by_css_selector("button.ssplayer-play-button")
        # print(play_button[0].get_attribute("display"))
        # play_button[0].click()
        # time.sleep(3)
        # pause_button = driver.find_elements_by_css_selector("button.ssplayer-pause-button")
        # print(pause_button[0].get_attribute("display"))
        # pause_button[0].click()
        driver.find_element_by_class_name("course-body__info-tab-name-content").click()
        content_list = driver.find_elements_by_css_selector("a.toc-item")
        link_counter = len(content_list)
        print(link_counter)
        site_refresh = False
        count = 0
        for x in content_list:
            wait = random.randint(10, 21)
            time.sleep(wait)
            current_url = driver.current_url
            if driver.find_elements_by_css_selector("footer.quiz-body__footer"):
                driver.find_element_by_css_selector("button[data-control-name='next_chapter']").click()
            else:
                next_button = driver.find_elements_by_css_selector("button.ssplayer-next-button")
                video_url_list = driver.find_elements_by_css_selector("video")
                if video_url_list:
                    video_url = driver.find_element_by_css_selector("video").get_attribute("src")
                    f.write(video_url)
                    f.write("\n\n")
                    time.sleep(wait)
                    player_loader = driver.find_elements_by_css_selector("div.ssplayer-loader.ssplayer-active")
                    if player_loader:
                        driver.refresh()
                        time.sleep(wait)
                    elif next_button[0].get_attribute("disabled"):
                        print(next_button[0].get_attribute("disabled"))
                        break
                    elif next_button:
                        next_button[0].click()
                        count += 1
                        notify_progress("LinkedIn Grabber", "Fetching Video Links", str(count) + " von " + str(link_counter))
                        print(count)
                    elif not next_button and not site_refresh:
                        site_refresh = True
                        driver.refresh()
                        time.sleep(5)
                    else:
                        notify_progress("Error", "Couldn't find or click next button", "Last URL = " + current_url)
                        break
                else:
                    notify_progress("Error", "Couldn't find video URL", "Last URL = " + current_url)
                    break

        f.close()
    # except:
    #     os.system("""
    #                   osascript -e 'display notification "{}" with title "{}" subtitle "{}"'
    #                   """.format("An Error occured", "LinkedIn Grabber", "Error"))


def notify_complete(title, subtitle, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}" subtitle "{}"'
              """.format(text, title, subtitle))


def driver_quit():
    driver.quit()


# UI design
AccountDetailsFrame = ttk.LabelFrame(win, text="Login")
AccountDetailsFrame.grid(column=0, row=0, padx=10, pady=10)

ttk.Label(AccountDetailsFrame, text="Mail Address").grid(column=0, row=0)
login_mail = tk.StringVar()
entered_login_mail = tk.Entry(AccountDetailsFrame, width=25, textvariable=login_mail)
entered_login_mail.grid(column=1, row=0)

ttk.Label(AccountDetailsFrame, text="Password").grid(column=0, row=1)
login_pw = tk.StringVar()
entered_login_pw = tk.Entry(AccountDetailsFrame, width=25, textvariable=login_pw)
entered_login_pw.grid(column=1, row=1)

# #button
login_button = ttk.Button(win, text="Connect", command=site_login)
login_button.grid(column=0, row=2, sticky="WE", padx=10, pady=5)
quit_button = ttk.Button(win, text="Quit Instance", command=driver_quit)
quit_button.grid(column=0, row=3, sticky="WE", padx=10, pady=5)


# #exit code
def _exit():
    driver.quit()
    win.quit()
    win.destroy()
    exit()


# #menubar
menubar = Menu(win)
win.config(menu=menubar)
fileMenu = Menu(menubar)
menubar.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Exit", command=_exit)

for child in AccountDetailsFrame.winfo_children():
    child.grid_configure(padx=10, pady=10)

# UI execution
win.mainloop()

# site_login()
# input_dialog()
# notify_complete("All links successfully saved in file.", link_count(), "Completed")
# driver.quit()
