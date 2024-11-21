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
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Lisää author
    Set Title  Probabilistic machine learning: an introduction
    Set Publisher  MIT Press
    Set Year  2022
    Submit 
    Page Should Contain  text=Kevin P Murphy


*** Keywords ***
Reset Table And Go To Starting Page
    Reset Table
    Go To Starting page

Submit
    Click Button  Tallenna

Set First name
    [Arguments]  ${first_name}
    Input Text  first_name  ${first_name}

Set Last name
    [Arguments]  ${last_name}
    Input Text  last_name  ${last_name}

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
    
