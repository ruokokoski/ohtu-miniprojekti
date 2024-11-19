*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Reset Table And Go To Starting Page

*** Test Cases ***
At start main page works
    Go To Starting page
    Title Should Be  Koti

Go To new reference
    Click Link  Uusi viite
    Title Should Be  Uusi viite

Go To reference list
    Click Link  Viitelistaus
    Title Should Be  Viitteet

Add a new book reference
    Click Link  Uusi viite
    Set Citation key  murphy2022
    Set Author  Murphy, Kevin P
    Set Title  Probabilistic machine learning: an introduction
    Set Publisher  MIT Press
    Set Address  US
    Set Year  2022
    Submit 
    Go To Starting page
    Click Link  Viitelistaus
    Page Should Contain  text=Murphy, Kevin P


*** Keywords ***
Reset Table And Go To Starting Page
    Reset Table
    Go To Starting page

Submit
    Click Button  Tallenna

Set Citation key
    [Arguments]  ${citation_key}
    Input Text  citation_key  ${citation_key}

Set Author
    [Arguments]  ${author}
    Input Text  author  ${author}

Set Title
    [Arguments]  ${title}
    Input Text  title  ${title}

Set Publisher
    [Arguments]  ${publisher}
    Input Text  publisher  ${publisher}

Set Address
    [Arguments]  ${address}
    Input Text  address  ${address}

Set Year
    [Arguments]  ${year}
    Input Text  year  ${year}
    