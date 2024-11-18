*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Table And Go To Starting Page

*** Test Cases ***
At start main page works
    Go To  ${HOME_URL}
    Title Should Be  Koti


*** Keywords ***
Reset Table And Go To Starting Page
    Reset Table
    Go To Starting page