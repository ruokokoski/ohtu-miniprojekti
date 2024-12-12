*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Starting Page

*** Test Cases ***
# tests commented out in fear of scraping protection kicking in. adding # at the start of next line activates tests
*** Comments ***
Search Google Scholar
    Click Link  Home
    Select Radio Button  database  Google Scholar
    Set Search Query  Matti Luukkainen
    Submit
    Page Should Contain  text=Searching...
    Page Should Contain  text=Extreme apprenticeship
    Page Should Contain  text=M Luukkainen
    
Search AMC Library
    Click Link  Home
    Select Radio Button  database  ACM
    Set Search Query  transformer time series
    Submit
    Page Should Contain  text=Searching...
    Page Should Contain  text=Modality-aware Transformer
    Page Should Contain  text=Hajar Emami Gohari

Search HELKA Library
    Click Link  Home
    Select Radio Button  database  Helka
    Set Search Query  Harry Potter ja viisasten kivi
    Submit
    Click Link  Harry Potter ja viisasten kivi
    Page Should Contain  text=J.K. Rowling

*** Keywords ***
Set Search Query  
    [Arguments]  ${query}
    Input Text  query  ${query}

Submit
    Click Button  Search