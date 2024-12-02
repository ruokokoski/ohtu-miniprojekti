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
    Click Button  Tallenna muutokset
    #Page Should Contain  text=Viite päivitetty onnistuneesti
    Page Should Contain  text=edited last name, edited first name
    Page Should Not Contain  text=Murphy, Kevin P

Edit A Reference (Edit Title)
    Click Link  Viitteet
    Click Button  Edit
    Set Title  edited title
    Click Button  Tallenna muutokset
    #Page Should Contain  text=Viite päivitetty onnistuneesti
    Page Should Contain  text=Viite päivitetty onnistuneesti
    Page Should Not Contain  text=Probabilistic machine learning: an introduction

Edit A Reference (Edit Publisher)
    Click Link  Viitteet
    Click Button  Edit
    Click Button  Näytä valinnaiset
    Set Publisher  edited publisher
    Click Button  Tallenna muutokset
    #Page Should Contain  text=Viite päivitetty onnistuneesti
    Page Should Contain  text=edited publisher
    Page Should Not Contain  text=MIT Press

Edit A Reference (Edit Year)
    Click Link  Viitteet
    Click Button  Edit
    Set Year  2000
    Click Button  Tallenna muutokset
    #Page Should Contain  text=Viite päivitetty onnistuneesti
    Page Should Contain  text=2000
    #Page Should Not Contain  text=1234

Edit A Reference (Edit Address)
    Click Link  Viitteet
    Click Button  Edit
    Click Button  Näytä valinnaiset
    Set Address  edited address
    Click Button  Tallenna muutokset
    #Page Should Contain  text=Viite päivitetty onnistuneesti
    Page Should Contain  text=edited address

Edit A Reference (Edit Volume)
    Click Link  Viitteet
    Click Button  Edit
    Click Button  Näytä valinnaiset
    Set Volume  edited volume
    Click Button  Tallenna muutokset
    #Page Should Contain  text=Viite päivitetty onnistuneesti
    Page Should Contain  text=edited volume

Edit A Reference (Edit Series)
    Click Link  Viitteet
    Click Button  Edit
    Click Button  Näytä valinnaiset
    Set Series  edited series
    Click Button  Tallenna muutokset
    #Page Should Contain  text=Viite päivitetty onnistuneesti
    Page Should Contain  text=edited series

Edit A Reference (Edit Edition)
    Click Link  Viitteet
    Click Button  Edit
    Click Button  Näytä valinnaiset
    Set Edition  edited edition
    Click Button  Tallenna muutokset
    #Page Should Contain  text=Viite päivitetty onnistuneesti
    Page Should Contain  text=edited edition

Edit A Reference (Edit Month)
    Click Link  Viitteet
    Click Button  Edit
    Click Button  Näytä valinnaiset
    Set Month  edited month
    Click Button  Tallenna muutokset
    #Page Should Contain  text=Viite päivitetty onnistuneesti
    Page Should Contain  text=edited month

Edit A Reference (Edit Note)
    Click Link  Viitteet
    Click Button  Edit
    Click Button  Näytä valinnaiset
    Set Note  edited note
    Click Button  Tallenna muutokset
    #Page Should Contain  text=Viite päivitetty onnistuneesti
    Page Should Contain  text=edited note

Edit A Reference (Edit URL)
    Click Link  Viitteet
    Click Button  Edit
    Click Button  Näytä valinnaiset
    Set URL  http://localhost:5001/
    Click Button  Tallenna muutokset
    #Page Should Contain  text=Viite päivitetty onnistuneesti
    Page Should Contain  text=http://localhost:5001/

Edit A Reference (Edit ISBN)
    Click Link  Viitteet
    Click Button  Edit
    Click Button  Näytä valinnaiset
    Set ISBN  edited ISBN
    Click Button  Tallenna muutokset
    #Page Should Contain  text=Viite päivitetty onnistuneesti
    Page Should Contain  text=edited ISBN

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
    Set Publisher  MIT Press
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

Set Title
    [Arguments]  ${title}
    Input Text  title  ${title}

Set Publisher
    [Arguments]  ${publisher}
    Input Text  publisher  ${publisher}

Set Year
    [Arguments]  ${year}
    Input Text  year  ${year}

Set Address
    [Arguments]  ${address}
    Input Text  address  ${address}

Set Volume
    [Arguments]  ${volume}
    Input Text  volume  ${volume}

Set Series
    [Arguments]  ${series}
    Input Text  series  ${series}

Set Edition
    [Arguments]  ${edition}
    Input Text  edition  ${edition}

Set Month
    [Arguments]  ${month}
    Input Text  month  ${month}

Set Note
    [Arguments]  ${note}
    Input Text  note  ${note}

Set URL
    [Arguments]  ${url}
    Input Text  url  ${url}

Set ISBN
    [Arguments]  ${isbn}
    Input Text  isbn  ${isbn}