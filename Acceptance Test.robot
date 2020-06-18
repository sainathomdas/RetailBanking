*** Settings ***
Library           SeleniumLibrary

*** Variables ***
${base_url}       http://127.0.0.1:5000/
${CUST_ID}        100000004    # Customer ID
${CUST_SSNID}     123456789
${CASHIER_USERNAME}    admin1234
${CASHIER_PASSWORD}    Admin@1234
${CUST_EXECUTIVE_USERNAME}    admin123
${CUST_EXECUTIVE_PASSWORD}    Admin@1234

*** Test Cases ***
test_cust_executive_login
    Open Browser    ${base_url}    chrome
    Maximize Browser Window
    CustExecutive Login Page Should Be Open
    Click Link    Logout
    Close Browser

test_create_update_customer
    Open Browser    ${base_url}    chrome
    Maximize Browser Window
    CustExecutive Login Page Should Be Open
    Click Element    //*[contains(text(),'Customer Management')]
    Click Link    Create Customer
    Input Text    name:cust_ssid    ${CUST_SSNID}
    Input Text    name:cust_name    Sainath
    Input Text    name:cust_age    22
    Input Text    name:cust_address    Charlapally
    Execute Javascript    window.scrollTo(0,200)
    Select From List By Label    name:cust_state    Andhra Pradesh
    Select From List By Label    name:cust_city    Hyderabad
    Click Button    Create
    Title Should Be    Mars | Create Customer
    Set Selenium Speed    0.2 seconds
    Click Element    //*[contains(text(),'Customer Management')]
    Click Link    Edit Customer
    Input Text    name:id    ${CUST_ID}
    Click Element    id:searchBtn
    Input Text    name:cust_new_name    Sainath Omdas
    Execute Javascript    window.scrollTo(0,100)
    Input Text    name:cust_new_age    22
    Execute Javascript    window.scrollTo(0,200)
    Input Text    name:cust_new_address    Hyderabad
    Execute Javascript    window.scrollTo(0,100)
    Select From List By Label    name:cust_state    Andhra Pradesh
    Select From List By Label    name:cust_city    Hyderabad
    Click Button    Update
    Title Should Be    Mars | Update Customer
    Click Element    //*[contains(text(),'Customer Management')]
    Click Link    Edit Customer
    Select From List By Value    name:input_type    ssn_id
    Input Text    name:id    ${CUST_SSNID}
    Click Element    id:searchBtn
    Input Text    name:cust_new_name    Sainath
    Execute Javascript    window.scrollTo(0,100)
    Input Text    name:cust_new_age    22
    Execute Javascript    window.scrollTo(0,200)
    Input Text    name:cust_new_address    Hyderabad
    Execute Javascript    window.scrollTo(0,100)
    Select From List By Label    name:cust_state    Andhra Pradesh
    Select From List By Label    name:cust_city    Hyderabad
    Click Button    Update
    Title Should Be    Mars | Update Customer
    Click Link    Logout
    Close Browser

test_account_management
    Open Browser    ${base_url}    chrome
    Maximize Browser Window
    CustExecutive Login Page Should Be Open
    Click Element    //*[contains(text(),'Account Management')]
    Click Link    Create Account
    Title Should Be    Mars | Create Account
    Input Text    name:cust_id    ${CUST_ID}
    Select From List By Value    name:account_type    savings
    Input Text    name:deposit_amt    10000
    Click Button    Create
    Set Selenium Speed    0.2 seconds
    Click Element    //*[contains(text(),'Account Management')]
    Click Link    Create Account
    Title Should Be    Mars | Create Account
    Input Text    name:cust_id    ${CUST_ID}
    Select From List By Value    name:account_type    current
    Input Text    name:deposit_amt    5000
    Click Button    Create
    Title Should Be    Mars | Create Account
    Click Link    Logout
    Title Should Be    Mars | Login
    Close Browser

test_customer_and_account_status
    Open Browser    ${base_url}    chrome
    Maximize Browser Window
    CustExecutive Login Page Should Be Open
    Click Element    //*[contains(text(),'Status Details')]
    Click Link    Customer Status
    Title Should Be    Mars | Customer Status
    Click Link    Refresh
    Click Button    View
    Title Should Be    Mars | View Customer
    Click Link    Back
    Title Should Be    Mars | Customer Status
    Click Element    //*[contains(text(),'Status Details')]
    Click Link    Account Status
    Click Link    Refresh
    Click Link    Logout
    Title Should Be    Mars | Login
    Close Browser

test_customer_and_account_search
    Open Browser    ${base_url}    chrome
    Maximize Browser Window
    CustExecutive Login Page Should Be Open
    Click Element    //*[contains(text(),'Search')]
    Click Link    Search Customer
    Title Should Be    Mars | Search Customer
    Select From List By Value    name:input_type    ssn_id
    Input Text    name:id    ${CUST_SSNID}
    Click Element    id:searchBtn
    Title Should Be    Mars | Search Customer
    Go To    http://127.0.0.1:5000/customer_search
    Title Should Be    Mars | Search Customer
    Select From List By Value    name:input_type    cust_id
    Input Text    name:id    ${CUST_ID}
    Click Element    id:searchBtn
    Title Should Be    Mars | Search Customer
    Go To    http://127.0.0.1:5000/account_search/
    Title Should Be    Mars | Search Account
    Select From List By Value    name:input_type    cust_id
    Input Text    name:id    ${CUST_ID}
    Click Element    id:searchBtn
    Title Should Be    Mars | Search Account
    Go To    http://127.0.0.1:5000/account_search/
    Title Should Be    Mars | Search Account
    Select From List By Value    name:input_type    acc_id
    Input Text    name:id    300000003
    Click Element    id:searchBtn
    Title Should Be    Mars | Search Account
    Click Link    Logout
    Title Should Be    Mars | Login
    Close Browser

test_cashier_login
    Open Browser    ${base_url}    chrome
    Maximize Browser Window
    Cashier Login Page Should Be Open
    Click Link    Logout
    Close Browser

test_account_actions
    Open Browser    ${base_url}    chrome
    Maximize Browser Window
    Go To Cashier Login Page
    Click Link    Account Details
    Title Should Be    Mars | Account Details
    Click Button    Deposit
    Title Should Be    Mars | Deposit
    Input Text    name:deposit_amt    5000
    Click Button    Deposit
    Title Should Be    Mars | Account Details
    Click Button    Withdraw
    Title Should Be    Mars | Withdraw
    Input Text    name:withdraw_amt    1000
    Click Button    Withdraw
    Title Should Be    Mars | Account Details
    Click Button    Transfer
    Title Should Be    Mars | Transfer
    Input Text    name:target_account_id    300000003
    Select From List By Value    name:target_account_type    savings
    Execute Javascript    window.scrollTo(0,200)
    Input Text    name:transfer_amt    100
    Click Button    Transfer
    Title Should Be    Mars | Account Details
    Click Link    Logout
    Close Browser

test_account_statement
    Open Browser    ${base_url}    chrome
    Maximize Browser Window
    Go To Cashier Login Page
    Click Link    Account Statement
    Title Should Be    Mars | Account Statement
    Input Text    name:account_id    300000002
    Select Radio Button    statement_type    transactions
    Set Selenium Speed    0.2 seconds
    Select From List By Value    name:num_of_transactions    5
    Click Button    Submit
    Set Selenium Speed    0.2 seconds
    Set Selenium Speed    0.2 seconds
    Set Selenium Speed    0.2 seconds
    #Click Element    //*[contains(text(),'PDF')]
    Set Selenium Speed    0.2 seconds
    Set Selenium Speed    0.2 seconds
    #Click Element    //*[contains(text(),'CSV')]
    Set Selenium Speed    0.2 seconds
    Set Selenium Speed    0.2 seconds
    #Click Element    //*[contains(text(),'Excel')]
    Execute Javascript    window.scrollTo(0,200)
    Click Link    Go Back
    Title Should Be    Mars | Account Statement
    Click Link    Logout
    Close Browser

test_delete_customer
    Open Browser    ${base_url}    chrome
    Maximize Browser Window
    CustExecutive Login Page Should Be Open
    Click Element    //*[contains(text(),'Customer Management')]
    Click Link    Delete Customer
    Select From List By Value    name:input_type    cust_id
    Input Text    name:id    ${CUST_ID}
    Click Element    id:searchBtn
    Click Link    Cancel
    Title Should Be    Mars | Delete Customer
    Click Element    //*[contains(text(),'Customer Management')]
    Click Link    Delete Customer
    Select From List By Value    name:input_type    cust_id
    Input Text    name:id    ${CUST_ID}
    Click Element    id:searchBtn
    Click Button    Delete
    Title Should Be    Mars | Delete Customer
    Click Link    Logout
    Close Browser

*** Keywords ***
Go To Cashier Login Page
    Cashier Login Page Should Be Open

Cashier Login Page Should Be Open
    Title Should Be    Mars | Login
    Input Text    name:username    ${CASHIER_USERNAME}
    Input Text    name:password    ${CASHIER_PASSWORD}
    Select From List By Value    name:login_type    cashier
    Click Button    Login
    Title Should Be    Mars | Home

CustExecutive Login Page Should Be Open
    Title Should Be    Mars | Login
    Input Text    name:username    ${CUST_EXECUTIVE_USERNAME}
    Input Text    name:password    ${CUST_EXECUTIVE_PASSWORD}
    Select From List By Value    name:login_type    cust_executive
    Click Button    Login
    Title Should Be    Mars | Home

Go To CustExecutive Login Page
    CustExecutive Login Page Should Be Open
