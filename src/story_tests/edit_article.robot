*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Reset Table Add A Reference And Go To Starting Page

*** Test Cases ***
Edit A Reference (Edit Author)
    Click Link  Viitteet
    Click Button  Edit
    Click Button  Poista
    Set First name  edited first name
    Set Last name  edited last name
    Click Button  Lisää author
    Select Reference Type  article
    Click Button  Tallenna muutokset
    #Page Should Contain  text=Viite päivitetty onnistuneesti
    Page Should Contain  text=edited last name, edited first name
    Page Should Not Contain  text=Murphy, Kevin P

Edit A Reference (Edit Title)
    Click Link  Viitteet
    Click Button  Edit
    Set Title  edited title
    Select Reference Type  article
    Click Button  Tallenna muutokset
    #Page Should Contain  text=Viite päivitetty onnistuneesti
    Page Should Contain  text=edited title
    Page Should Not Contain  text=Probabilistic machine learning: an introduction

Edit A Reference (Edit Journal)
    Click Link  Viitteet
    Click Button  Edit
    Select Reference Type  article
    Click Button  Näytä valinnaiset
    Set Journal  edited journal
    Click Button  Tallenna muutokset
    #Page Should Contain  text=Viite päivitetty onnistuneesti
    Page Should Contain  text=edited journal
    Page Should Not Contain  text=MIT Press

Edit A Reference (Edit Year)
    Click Link  Viitteet
    Click Button  Edit
    Set Year  2000
    Select Reference Type  article
    Click Button  Tallenna muutokset
    #Page Should Contain  text=Viite päivitetty onnistuneesti
    Page Should Contain  text=2000
    Page Should Not Contain  text=1234

Edit A Reference (Edit Number)
    Click Link  Viitteet
    Click Button  Edit
    Select Reference Type  article
    Click Button  Näytä valinnaiset
    Set Number  edited number
    Click Button  Tallenna muutokset
    #Page Should Contain  text=Viite päivitetty onnistuneesti
    Page Should Contain  text=edited number

Edit A Reference (Edit Volume)
    Click Link  Viitteet
    Click Button  Edit
    Click Button  Näytä valinnaiset
    Set Volume  edited volume
    Select Reference Type  article
    Click Button  Tallenna muutokset
    #Page Should Contain  text=Viite päivitetty onnistuneesti
    Page Should Contain  text=edited volume

Edit A Reference (Edit Month)
    Click Link  Viitteet
    Click Button  Edit
    Click Button  Näytä valinnaiset
    Set Month  edited month
    Select Reference Type  article
    Click Button  Tallenna muutokset
    #Page Should Contain  text=Viite päivitetty onnistuneesti
    Page Should Contain  text=edited month

Edit A Reference (Edit Note)
    Click Link  Viitteet
    Click Button  Edit
    Click Button  Näytä valinnaiset
    Set Note  edited note
    Select Reference Type  article
    Click Button  Tallenna muutokset
    #Page Should Contain  text=Viite päivitetty onnistuneesti
    Page Should Contain  text=edited note

*** Keywords ***
Reset Table Add A Reference And Go To Starting Page
    Reset Table
    Go To Starting page
    Click Link  Uusi viite
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Lisää author
    Click Button  Näytä valinnaiset
    Set Title  Probabilistic machine learning: an introduction
    Select Reference Type  article
    Set Journal  MIT Press
    Set Year  2022
    Submit 
    Go To Starting page

Submit
    Click Button  Tallenna

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