*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Reset Table And Go To Starting Page

*** Test Cases ***
Add a new valid book reference
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  book
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
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  book
    Set Title  Probabilistic machine learning: an introduction
    Set Publisher  MIT Press
    Set Year  2022
    Set Address  address test
    Submit 
    Page Should Contain  text=address test

Add a new valid book reference with optional (volume)
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  book
    Set Title  Probabilistic machine learning: an introduction
    Set Publisher  MIT Press
    Set Year  2022
    Set Volume  volume test
    Submit 
    Page Should Contain  text=volume test

Add a new valid book reference with optional (series)
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  book
    Set Title  Probabilistic machine learning: an introduction
    Set Publisher  MIT Press
    Set Year  2022
    Set Series  series test
    Submit 
    Page Should Contain  text=series test

Add a new valid book reference with optional (edition)
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  book
    Set Title  Probabilistic machine learning: an introduction
    Set Publisher  MIT Press
    Set Year  2022
    Set Edition  edition test
    Submit 
    Page Should Contain  text=edition test

Add a new valid book reference with optional (month)
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  book
    Set Title  Probabilistic machine learning: an introduction
    Set Publisher  MIT Press
    Set Year  2022
    Set Month  month test
    Submit 
    Page Should Contain  text=month test

Add a new valid book reference with optional (note)
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  book
    Set Title  Probabilistic machine learning: an introduction
    Set Publisher  MIT Press
    Set Year  2022
    Set Note  note test
    Submit 
    Page Should Contain  text=note test

Add a new valid book reference with optional (URL)
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  book
    Set Title  Probabilistic machine learning: an introduction
    Set Publisher  MIT Press
    Set Year  2022
    Set URL  http://localhost:5001/references
    Submit 
    Page Should Contain  text=http://localhost:5001/references

Add a new valid book reference with optional (ISBN)
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  book
    Set Title  Probabilistic machine learning: an introduction
    Set Publisher  MIT Press
    Set Year  2022
    Set ISBN  testi isbn
    Submit 
    Page Should Contain  text=testi isbn

Add a new blank book reference
    Click Link  New reference
    Submit 
    Title Should Be  New reference

Add a new partially filled book reference (no number in year)
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  book
    Set Title  Probabilistic machine learning: an introduction
    Set Publisher  MIT Press
    Set Year  -
    Submit 
    Title Should Be  New reference

Add a new partially filled book reference (year too small)
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  book
    Set Title  Probabilistic machine learning: an introduction
    Set Publisher  MIT Press
    Set Year  0
    Submit 
    Title Should Be  New reference

Add a new partially filled book reference (title too short)
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  book
    Set Title  a
    Set Publisher  MIT Press
    Set Year  2022
    Submit 
    Page Should Contain  text=Title must be at least 2 characters long

Add a new partially filled book reference (no author submited)
    Click Link  New reference
    Select Reference Type  book
    Set Title  Probabilistic machine learning: an introduction
    Set Publisher  MIT Press
    Set Year  2022
    Submit 
    Alert Should Be Present

Add a new partially filled book reference (blank author submited)
    Click Link  New reference
    Select Reference Type  book
    Click Button  Add author
    Alert Should Be Present

Add a new partially filled book reference (only first name submited)
    Click Link  New reference
    Select Reference Type  book
    Set First name  Kevin P
    Click Button  Add author
    Alert Should Be Present

Add a new partially filled book reference (only last name submited)
    Click Link  New reference
    Select Reference Type  book
    Set Last name  Murphy
    Click Button  Add author
    Alert Should Be Present

Add a new invalid book reference (year too large)
    Click Link  New reference
    Select Reference Type  book
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Set Title  Probabilistic machine learning: an introduction
    Set Publisher  MIT Press
    Set Year  10000
    Submit 
    Title Should Be  New reference

*** Keywords ***
Reset Table And Go To Starting Page
    Reset Table
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