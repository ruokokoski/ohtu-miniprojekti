*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Reset Table Add A Reference And Go To Starting Page

*** Test Cases ***
Edit A Reference (Edit Author)
    Click Link  References
    Mouse Over  editbutton 
    Click Button  Edit
    Click Button  Delete
    Set First name  edited first name
    Set Last name  edited last name
    Click Button  Add author
    Click Button  Save
    #Page Should Contain  text=Reference updated
    Page Should Contain  text=edited last name, edited first name
    Page Should Not Contain  text=Murphy, Kevin P

Edit A Reference (Edit Title)
    Click Link  References
    Mouse Over  editbutton 
    Click Button  Edit
    Set Title  edited title
    Click Button  Save
    #Page Should Contain  text=Reference updated
    Page Should Contain  text=Reference updated
    Page Should Not Contain  text=Probabilistic machine learning: an introduction

Edit A Reference (Edit Publisher)
    Click Link  References
    Mouse Over  editbutton 
    Click Button  Edit
    Set Publisher  edited publisher
    Click Button  Save
    #Page Should Contain  text=Reference updated
    Page Should Contain  text=edited publisher
    Page Should Not Contain  text=MIT Press

Edit A Reference (Edit Year)
    Click Link  References
    Mouse Over  editbutton 
    Click Button  Edit
    Set Year  2000
    Click Button  Save
    #Page Should Contain  text=Reference updated
    Page Should Contain  text=2000
    #Page Should Not Contain  text=1234

Edit A Reference (Edit Address)
    Click Link  References
    Mouse Over  editbutton 
    Click Button  Edit
    Set Address  edited address
    Click Button  Save
    #Page Should Contain  text=Reference updated
    Page Should Contain  text=edited address

Edit A Reference (Edit Volume)
    Click Link  References
    Mouse Over  editbutton 
    Click Button  Edit
    Set Volume  edited volume
    Click Button  Save
    #Page Should Contain  text=Reference updated
    Page Should Contain  text=edited volume

Edit A Reference (Edit Series)
    Click Link  References
    Mouse Over  editbutton 
    Click Button  Edit
    Set Series  edited series
    Click Button  Save
    #Page Should Contain  text=Reference updated
    Page Should Contain  text=edited series

Edit A Reference (Edit Edition)
    Click Link  References
    Mouse Over  editbutton 
    Click Button  Edit
    Set Edition  edited edition
    Click Button  Save
    #Page Should Contain  text=Reference updated
    Page Should Contain  text=edited edition

Edit A Reference (Edit Month)
    Click Link  References
    Mouse Over  editbutton 
    Click Button  Edit
    Set Month  edited month
    Click Button  Save
    #Page Should Contain  text=Reference updated
    Page Should Contain  text=edited month

Edit A Reference (Edit Note)
    Click Link  References
    Mouse Over  editbutton 
    Click Button  Edit
    Set Note  edited note
    Click Button  Save
    #Page Should Contain  text=Reference updated
    Page Should Contain  text=edited note

Edit A Reference (Edit URL)
    Click Link  References
    Mouse Over  editbutton 
    Click Button  Edit
    Set URL  http://localhost:5001/
    Click Button  Save
    #Page Should Contain  text=Reference updated
    Page Should Contain  text=http://localhost:5001/

Edit A Reference (Edit ISBN)
    Click Link  References
    Mouse Over  editbutton 
    Click Button  Edit
    Set ISBN  edited ISBN
    Click Button  Save
    #Page Should Contain  text=Reference updated
    Page Should Contain  text=edited ISBN

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