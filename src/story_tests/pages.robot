*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Reset Table And Go To Starting Page

*** Test Cases ***
Go To new reference
    Click Link  New reference
    Title Should Be  New reference

Go To reference list
    Click Link  References
    Title Should Be  References

Go back To main page
    Click Link  References
    Click Link  Home
    Title Should Be  Home

*** Keywords ***
Reset Table And Go To Starting Page
    Reset Table
    Go To Starting page
