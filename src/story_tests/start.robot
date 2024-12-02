*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Reset Table And Go To Starting Page

*** Test Cases ***
At start main page works
    Title Should Be  Home

*** Keywords ***
Reset Table And Go To Starting Page
    Reset Table
    Go To Starting page
    
