import selenium
from selenium.webdriver.common.by import By
from time import sleep
import threading

class autobuy_bot(threading.Thread):
    def __init__(self,amazon_email,amazon_psw,asin,cut_price,autocheckout):
        self.amazon_email=amazon_email
        self.amazon_psw=amazon_psw
        self.asin=asin
        self.cut_price=cut_price
        self.autocheckout=autocheckout
        threading.Thread.__init__(self) 

    def run(self):
        options = selenium.webdriver.ChromeOptions() 
        options.headless = False

        # Configure the undetected_chromedriver options
        driver = selenium.webdriver.Chrome(options=options) 

        driver.get("https://www.amazon.it/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.it%2Fgp%2Fcart%2Fview.html%2Fref%3Dnav_ya_signin%3F&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=itflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0")
        sleep(1)
        driver.find_element(by=By.XPATH, value='//*[@id="ap_email"]').send_keys(self.amazon_email)
        sleep(1)
        driver.find_element(by=By.XPATH, value='//*[@id="continue"]').click()
        sleep(1)
        driver.find_element(by=By.XPATH, value='//*[@id="ap_password"]').send_keys(self.amazon_psw)
        sleep(1)
        driver.find_element(by=By.XPATH, value='//*[@id="signInSubmit"]').click()
        sleep(1)


        driver.get("https://www.amazon.it/dp/"+self.asin+"/ref=olp-opf-redir?aod=1&tag=pysol07-21")
        check=True
        while check==True:
            try:
                sleep(2)
                current_price = int(driver.find_element(by=By.XPATH, value='//*[@id="aod-price-0"]/div/span/span[2]/span[1]').get_attribute("innerHTML").split("<")[0].replace(".",""))
                
            except:
                driver.refresh()
                sleep(2)
                current_price = int(driver.find_element(by=By.XPATH, value='//*[@id="aod-price-0"]/div/span/span[2]/span[1]').get_attribute("innerHTML").split("<")[0].replace(".",""))

            if current_price > self.cut_price:
                print("Non c'è l'errore, infatti l'attuale prezzo è di: "+str(current_price))
            else:
                print("Articolo in errore di prezzo a: "+(current_price))
                add_cart_btn=driver.find_element(by=By.XPATH, value='//*[@id="a-autoid-2-offer-0"]/span/input')
                add_cart_btn.click()
                sleep(0.5)
                driver.find_element(by=By.XPATH, value='//*[@id="sc-buy-box-ptc-button"]/span/input').click()
                if self.autocheckout == True:
                    driver.find_element(by=By.XPATH, value='//*[@id="a-autoid-0-announce"]').click()
                    driver.find_element(by=By.XPATH, value='//*[@id="submitOrderButtonId"]/span/input"]').click()
                else:
                    pass
                check=False
            driver.get("https://www.amazon.it/dp/"+self.asin+"/ref=olp-opf-redir?aod=1&tag=pysol07-21")
            sleep(1)
            

        driver.quit()
    
        


amazon_email="Your amazon email"
amazon_psw="Your amazon password"

asin = ["B0CX5K5HKC","B07W6GNXZG"]
cut_price=[360,10]
autocheckout= [False,False]

threads_list=[]

for i in range(0, len(asin)):
    print(asin[i])
    t=autobuy_bot(amazon_email=amazon_email,amazon_psw=amazon_psw,asin=asin[i],cut_price=cut_price[i],autocheckout=autocheckout[i])
    t.start() 
    threads_list.append(t) 
  
for t in threads_list: 
    t.join()
       
