*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Reset Table And Go To Starting Page

*** Test Cases ***
Add A New Valid Article Reference
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  article
    Click Button  Optional fields
    Set Title  Probabilistic machine learning: an introduction
    Set Journal  MIT Press
    Set Year  2022
    Submit 
    Page Should Contain  text=Murphy, Kevin P
    Page Should Contain  text=Probabilistic machine learning: an introduction
    Page Should Contain  text=MIT Press
    Page Should Contain  text=2022
    Page Should Contain  text=Murphy2022Probabilistic

Add A New Valid Article Reference With Optional (Number)
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  article
    Set Title  Probabilistic machine learning: an introduction
    Click Button  Optional fields
    Set Journal  MIT Press
    Set Year  2022
    Set Number  number test
    Submit 
    Page Should Contain  text=number test

Add A New Valid Article Reference With Optional (Volume)
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Click Button  Optional fields
    Set Volume  volume test
    Select Reference Type  article
    Set Title  Probabilistic machine learning: an introduction
    Set Journal  MIT Press
    Set Year  2022
    
    Submit 
    Page Should Contain  text=volume test

Add A New Valid Article Reference With Optional (Month)
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Click Button  Optional fields
    Set Month  month test
    Select Reference Type  article
    Set Title  Probabilistic machine learning: an introduction
    Set Journal  MIT Press
    Set Year  2022
    Submit 
    Page Should Contain  text=month test

Add A New Valid Article Reference With Optional (Note)
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Click Button  Optional fields
    Set Note  note test
    Select Reference Type  article
    Set Title  Probabilistic machine learning: an introduction
    Set Journal  MIT Press
    Set Year  2022
    Submit 
    Page Should Contain  text=note test

*** Keywords ***
Reset Table And Go To Starting Page
    Reset Table
    Go To Starting page

Submit
    Click Button  Save

Set First name
    [Arguments]  ${first_name}
    Input Text  first_name  ${first_name}

Set Last name
    [Arguments]  ${last_name}
    Input Text  last_name  ${last_name}

Select Reference Type
    [Arguments]  ${reference_type}
    Select From List By Label  entry_type  ${reference_type}

Set Title
    [Arguments]  ${title}
    Input Text  title  ${title}

Set Journal
    [Arguments]  ${journal}
    Input Text  journal  ${journal}

Set Year
    [Arguments]  ${year}
    Input Text  year  ${year}

Set Number
    [Arguments]  ${number}
    Input Text  number  ${number}

Set Volume
    [Arguments]  ${volume}
    Input Text  volume  ${volume}

Set Month
    [Arguments]  ${month}
    Input Text  month  ${month}

Set Note
    [Arguments]  ${note}
    Input Text  note  ${note}
