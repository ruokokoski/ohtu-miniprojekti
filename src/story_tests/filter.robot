*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Reset Table Add Couple References And Go To Starting Page

*** Test Cases ***
Search
    Click Link  References
    Set Search Author  s
    Test If Element Is Not Visible  Murphy2022Probabilistic
    Test If Element Is Visible  sukunimi1234otsikko
    Set Search Author  search_author=r
    Test If Element Is Visible  Murphy2022Probabilistic
    Test If Element Is Not Visible  sukunimi1234otsikko
    Set Search Author  search_author=
    Set Search Title  p
    Test If Element Is Visible  Murphy2022Probabilistic
    Test If Element Is Not Visible  sukunimi1234otsikko
    Set Search Title  search_title=
    Set Max Year  2000
    Test If Element Is Not Visible  Murphy2022Probabilistic
    Test If Element Is Visible  sukunimi1234otsikko
    Set Max Year  max_year=
    Set Min Year  2000
    Test If Element Is Visible  Murphy2022Probabilistic
    Test If Element Is Not Visible  sukunimi1234otsikko
    

*** Keywords ***
Reset Table Add Couple References And Go To Starting Page
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

    Click Link  New reference
    Set First name  etunimi
    Set Last name  sukunimi
    Click Button  Add author
    Select Reference Type  article
    Set Title  otsikko
    Set Journal  julkaisija
    Set Year  1234
    Submit 

    Go To Starting page

Submit
    Click Button  Save

Test If Element Is Not Visible
    [Arguments]  ${citation_key}
    Wait For Condition  condition=return document.getElementById('${citation_key}').style.display == "none";

Test If Element Is Visible
    [Arguments]  ${citation_key}
    Wait For Condition  condition=return document.getElementById('${citation_key}').style.display == "";

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

Set Journal
    [Arguments]  ${journal}
    Input Text  journal  ${journal}

Set Search Author
    [Arguments]  ${search_author}
    Input Text  search_author  ${search_author}

Set Search Title
    [Arguments]  ${search_title}
    Input Text  search_title  ${search_title}

Set Min Year
    [Arguments]  ${min_year}
    Input Text  min_year  ${min_year}

Set Max Year
    [Arguments]  ${max_year}
    Input Text  max_year  ${max_year}