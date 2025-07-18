# 📱 bKash App Testing Automation

This program is built using **Python** and uses **Appium** as the testing framework. It automates the testing of different features in the **bKash Merchant Application**. The tests cover core functionalities like login, balance check, transactions, payments, and more.  

The test suite is designed to print both **success** and **failure** messages in the terminal to clearly determine test results. Each test outputs:  
✅ Specific messages for individual elements (e.g., button found, screen loaded).  
✅ A final summary message for each specific feature at the end of its execution.

---

## 🚀 Features Tested

The following features of the bKash Merchant app are automated:  

- 🔐 **Login**  
- 💳 **Check Balance**  
- 📥 **Check Inbox**  
- 📜 **Check Transactions**  
- 🕌 **Namaz & Roja Details**  
- 💸 **Send Money**  
- 🏪 **Merchant Payment**  
- 📷 **Check QR Code**  
- 🧾 **Pay Bills**  
- 💰 **Savings Registration**  
- 🏧 **Agent Cashout**  
- 🚪 **Logout**  

Each feature includes explicit assertions and descriptive console outputs to indicate progress and results.

---

## How to run the code?
1. On first terminal execute 'adb devices' to check the device connectivity. <br>
2. On second terminal execute 'appium &' to start the Appium server. <br>
3. On third terminal exacute 'cd bkash-app-testing-automation' to change the directory to bkash-app-testing-automation. <br>
4. Then, on that terminal exacute 'python3 bkash-app-test.py' to begin the testing process. <br>

---

## 🛠️ Built With

- **Python 3.x** – Programming language
- **Appium** – Mobile app automation framework
- **Selenium WebDriver** – Underlying driver for Appium

---
