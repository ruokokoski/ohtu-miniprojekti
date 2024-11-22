*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Reset Table And Go To Starting Page

*** Test Cases ***
Go To new reference
    Click Link  Uusi viite
    Title Should Be  Uusi viite

Go To reference list
    Click Link  Viitteet
    Title Should Be  Viitteet

Go back To main page
    Click Link  Viitteet
    Click Link  Koti
    Title Should Be  Koti

*** Keywords ***
Reset Table And Go To Starting Page
    Reset Table
    Go To Starting page
