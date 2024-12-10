*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Reset Table Add A Reference And Go To Starting Page

*** Test Cases ***
Delete a reference
    Click Link  References
    Mouse Over  editbutton 
    Click Button  Delete
    Handle Alert
    Page Should Not Contain  text=Murphy

*** Keywords ***
Reset Table Add A Reference And Go To Starting Page
    Reset Table
    Go To Starting page
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  book
    Set Title  Probabilistic machine learning: an introduction
    Set Publisher  MIT Press
    Set Year  2022
    Submit 
    Go To Starting page

Submit
    Click Button  Save

Select Reference Type
    [Arguments]  ${reference_type}
    Select From List By Label  entry_type  ${reference_type}

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

Set Year
    [Arguments]  ${year}
    Input Text  year  ${year}