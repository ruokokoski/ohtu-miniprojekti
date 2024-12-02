*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Starting Page

*** Test Cases ***
Search Google Scholar
    Click Link  Home
    Select Radio Button  database  Google Scholar
    Set Search Query  syöpä
    Submit
    Page Should Contain  text=Searching...
    Page Should Contain  text=Miten syöpä syntyy
    Page Should Contain  text=M Laiho
Search AMC Library
    Click Link  Home
    Select Radio Button  database  ACM
    Set Search Query  testi
    Submit
    Page Should Contain  text=Searching...
    Page Should Contain  text=Machine Learning-Based Jamming Detection and Classification in Wireless Networks
    Page Should Contain  text=Enrico Testi, Luca Arcangeloni

*** Keywords ***
Set Search Query  
    [Arguments]  ${query}
    Input Text  query  ${query}

Submit
    Click Button  Search