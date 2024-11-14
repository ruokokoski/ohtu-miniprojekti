*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser

*** Test Cases ***
Open And Configure Browser
    Go To  ${HOME_URL}
    Title Should Be  Viitelistaus