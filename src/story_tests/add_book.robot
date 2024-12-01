*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Reset Table And Go To Starting Page

*** Test Cases ***
Add a new valid book reference
    Click Link  Uusi viite
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Lisää author
    Set Title  Probabilistic machine learning: an introduction
    Set Publisher  MIT Press
    Set Year  2022
    Submit 
    Page Should Contain  text=Murphy, Kevin P
    Page Should Contain  text=Probabilistic machine learning: an introduction
    Page Should Contain  text=MIT Press
    Page Should Contain  text=2022
    Page Should Contain  text=Murphy2022Probabilistic

Add a new valid book reference with optional (address)
    Click Link  Uusi viite
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Lisää author
    Set Title  Probabilistic machine learning: an introduction
    Set Publisher  MIT Press
    Set Year  2022
    Click Button  Näytä valinnaiset
    Set Address  address test
    Submit 
    Page Should Contain  text=address test

Add a new valid book reference with optional (volume)
    Click Link  Uusi viite
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Lisää author
    Set Title  Probabilistic machine learning: an introduction
    Set Publisher  MIT Press
    Set Year  2022
    Click Button  Näytä valinnaiset
    Set Volume  volume test
    Submit 
    Page Should Contain  text=volume test

Add a new valid book reference with optional (series)
    Click Link  Uusi viite
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Lisää author
    Set Title  Probabilistic machine learning: an introduction
    Set Publisher  MIT Press
    Set Year  2022
    Click Button  Näytä valinnaiset
    Set Series  series test
    Submit 
    Page Should Contain  text=series test

Add a new valid book reference with optional (edition)
    Click Link  Uusi viite
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Lisää author
    Set Title  Probabilistic machine learning: an introduction
    Set Publisher  MIT Press
    Set Year  2022
    Click Button  Näytä valinnaiset
    Set Edition  edition test
    Submit 
    Page Should Contain  text=edition test

Add a new valid book reference with optional (month)
    Click Link  Uusi viite
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Lisää author
    Set Title  Probabilistic machine learning: an introduction
    Set Publisher  MIT Press
    Set Year  2022
    Click Button  Näytä valinnaiset
    Set Month  month test
    Submit 
    Page Should Contain  text=month test

Add a new valid book reference with optional (note)
    Click Link  Uusi viite
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Lisää author
    Set Title  Probabilistic machine learning: an introduction
    Set Publisher  MIT Press
    Set Year  2022
    Click Button  Näytä valinnaiset
    Set Note  note test
    Submit 
    Page Should Contain  text=note test

Add a new valid book reference with optional (URL)
    Click Link  Uusi viite
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Lisää author
    Set Title  Probabilistic machine learning: an introduction
    Set Publisher  MIT Press
    Set Year  2022
    Click Button  Näytä valinnaiset
    Set URL  http://localhost:5001/references
    Submit 
    Page Should Contain  text=http://localhost:5001/references

Add a new valid book reference with optional (ISBN)
    Click Link  Uusi viite
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Lisää author
    Set Title  Probabilistic machine learning: an introduction
    Set Publisher  MIT Press
    Set Year  2022
    Click Button  Näytä valinnaiset
    Set ISBN  testi isbn
    Submit 
    Page Should Contain  text=testi isbn

Add a new blank book reference
    Click Link  Uusi viite
    Submit 
    Title Should Be  Uusi viite

Add a new partially filled book reference (no number in year)
    Click Link  Uusi viite
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Lisää author
    Set Title  Probabilistic machine learning: an introduction
    Set Publisher  MIT Press
    Set Year  -
    Submit 
    Title Should Be  Uusi viite

Add a new partially filled book reference (year too small)
    Click Link  Uusi viite
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Lisää author
    Set Title  Probabilistic machine learning: an introduction
    Set Publisher  MIT Press
    Set Year  0
    Submit 
    Title Should Be  Uusi viite

Add a new partially filled book reference (title too short)
    Click Link  Uusi viite
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Lisää author
    Set Title  a
    Set Publisher  MIT Press
    Set Year  2022
    Submit 
    Page Should Contain  text=Title must be at least 2 characters long

Add a new partially filled book reference (publisher too short)
    Click Link  Uusi viite
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Lisää author
    Set Title  Probabilistic machine learning: an introduction
    Set Publisher  a
    Set Year  2022
    Submit 
    Page Should Contain  text=Publisher must be at least 2 characters long

Add a new partially filled book reference (no author submited)
    Click Link  Uusi viite
    Set Title  Probabilistic machine learning: an introduction
    Set Publisher  MIT Press
    Set Year  2022
    Submit 
    Alert Should Be Present

Add a new partially filled book reference (blank author submited)
    Click Link  Uusi viite
    Click Button  Lisää author
    Alert Should Be Present

Add a new partially filled book reference (only first name submited)
    Click Link  Uusi viite
    Set First name  Kevin P
    Click Button  Lisää author
    Alert Should Be Present

Add a new partially filled book reference (only last name submited)
    Click Link  Uusi viite
    Set Last name  Murphy
    Click Button  Lisää author
    Alert Should Be Present

Add a new invalid book reference (year too large)
    Click Link  Uusi viite
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Lisää author
    Set Title  Probabilistic machine learning: an introduction
    Set Publisher  MIT Press
    Set Year  10000
    Submit 
    Title Should Be  Uusi viite

Add a new invalid book reference (title too long)
    Click Link  Uusi viite
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Lisää author
    Set Title  aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    Set Publisher  MIT Press
    Set Year  2022
    Submit 
    Page Should Contain  text=Title must be under 100 characters long

Add a new invalid book reference (publisher too long)
    Click Link  Uusi viite
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Lisää author
    Set Title  Probabilistic machine learning: an introduction
    Set Publisher  aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    Set Year  2022
    Submit 
    Page Should Contain  text=Publisher must be under 100 characters long

*** Keywords ***
Reset Table And Go To Starting Page
    Reset Table
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