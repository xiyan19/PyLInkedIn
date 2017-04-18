# -*- coding: utf-8 -*-

"""
    此脚本爬取LinkedIn中指定公司的所有职位信息，并输出去重之后的结果。

    Last commit info:
    ~~~~~~~~~~~~~~~~~
    $LastChangedDate: 3/1/2017
    $Annotation: Create.
    $Author: xiyan19
"""


import time, sys
from splinter import Browser
import module_TestNetwork

# LinkedIn账号及密码
userName = ''
password = ''

# 指定所使用的浏览器
browser = Browser('chrome')


def login():
    """
    该函数用于登陆LinkedIn。

    :return: 无
    """
    SignInPage = "https://www.linkedin.com/uas/login?goback=&trk=hb_signin"
    browser.visit(SignInPage)

    browser.find_by_id("session_key-login").fill(userName)
    browser.find_by_id("session_password-login").fill(password)
    browser.find_by_id("btn-primary").click()

    # "[-] " + userName + " login failed!"
    print("[+] " + userName + " login success!")

    # 等待登陆完毕
    time.sleep(10)


def searchCompanies(CompaniesName):
    """
    该函数输入一个包含各公司名称的List，输出各公司职位信息的List到文件JobList中。

    :param CompaniesName: list
    :return: 无
    """
    for name in CompaniesName:
        if name is '':
            print("[-] Company's name is null! Exit.")
            sys.exit()

        nextCompany = 0

        # 跳转到公司查询页面
        site = "http://www.linkedin.com/search/results/companies/?keywords=" + name + "&origin=SWITCH_SEARCH_VERTICAL"
        browser.visit(site)
        time.sleep(5)

        # 用循环防止网页加载过慢导致找不到对应元素的问题
        for times in range(1, 6):
            if browser.is_element_present_by_xpath("//a[@class='search-result__result-link ember-view']"):
                browser.find_by_xpath("//a[@class='search-result__result-link ember-view']").click()
                time.sleep(3)
                break
            if times < 5:
                print("[-] Can't find 1 level href. CompanyName: " + name + ". Try again. Times: " + str(times) + "...")
                browser.reload()
                time.sleep(10)
            else:
                print("[-] Can't find 1 level href. CompanyName: " + name + ". Exit. Times: " + str(times))
                print("[-] " + name + " isn't finished")
                nextCompany = 1

        if nextCompany == 1:
            continue

        for times in range(1, 6):
            if browser.is_element_present_by_xpath("//a[@class='org-company-employees-snackbar__details-highlight snackbar-description-see-all-link']"):
                browser.find_by_xpath("//a[@class='org-company-employees-snackbar__details-highlight snackbar-description-see-all-link']").click()
                time.sleep(2)
                browser.windows[0].close()
                break
            if times < 5:
                print("[-] Can't find 2 level href. CompanyName: " + name + ". Try again. Times: " + str(times) + "...")
                browser.reload()
                time.sleep(10)
            else:
                print("[-] Can't find 2 level href. CompanyName: " + name + ". Exit. Times: " + str(times))
                print("[-] " + name + " isn't finished")
                nextCompany = 1

        if nextCompany == 1:
            continue

        tag = 0
        while tag != 1:
            orign_url = browser.url
            for pages in range(1, 1000):
                nextPage = orign_url + "&page=" + str(pages)
                browser.visit(nextPage)
                time.sleep(5)

                if browser.is_element_present_by_xpath("//div[@class='search-no-results text-align-center m4 ember-view']"):
                    tag = 1
                    break
                else:
                    pList = []
                    for times in range(1, 6):
                        browser.evaluate_script("scrollTo(0,document.body.scrollHeight)")
                        time.sleep(3)
                        browser.evaluate_script("scrollTo(0,document.body.scrollHeight)")
                        time.sleep(3)
                        browser.evaluate_script("scrollTo(0,document.body.scrollHeight)")
                        time.sleep(3)

                        if browser.is_element_present_by_xpath("//p[@class='search-result__snippets mt2 Sans-13px-black-55% ember-view']"):
                            pList = browser.find_by_xpath("//p[@class='search-result__snippets mt2 Sans-13px-black-55% ember-view']")
                            break
                        if times < 5:
                            print("[-] Can't find 3 level p. CompanyName: " + name + ". Try again. Times: " + str(times) + "...")
                            browser.reload()
                        else:
                            print("[-] Can't find 3 level p. CompanyName: " + name + ". Exit. Times: " + str(times))
                            print("[-] " + name + " isn't finished")
                            nextCompany = 1

                    if nextCompany == 1:
                        break

                    output_file = open("JobList", "a")
                    for pNode in pList:
                        jobName = pNode.text
                        jobName = jobName.lstrip("目前就职: ")
                        output_file.write(jobName + "\n")

                    output_file.close()

            if nextCompany == 1:
                break

        if nextCompany == 1:
            continue

        print("[+] " + name + " finished.")

    return


if __name__ == '__main__':
    # 测试网络
    website = ["www.linkedin.com"]
    module_TestNetwork.netCheck(website)

    # 登陆LinkedIn
    login()

    # 从文件中读取待搜索的公司名称列表
    input_file = open("Companylist.distinct", 'r')
    nameList = []
    for line in input_file:
        line = line.rstrip("\n")
        nameList.append(line)

    input_file.close()

    # 输出JobList文件
    searchCompanies(nameList)