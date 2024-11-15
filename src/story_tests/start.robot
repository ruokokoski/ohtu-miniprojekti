*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser

*** Test Cases ***
At start main page works
    Go To  ${HOME_URL}
    Title Should Be  Viitelistaus