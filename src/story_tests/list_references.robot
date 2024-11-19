*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser

*** Test Cases ***
User presses Viitelistaus and page opens
    Go To  ${HOME_URL}
    Click Link  Viitelistaus
    Title Should Be  Viitteet