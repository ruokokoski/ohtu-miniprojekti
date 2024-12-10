*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Reset Table And Go To Starting Page

*** Test Cases ***

Add A Booklet Reference
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  booklet
    Set Title  Probabilistic machine learning: an introduction
    Set Year  2022
    Submit 
    Page Should Contain  text=Murphy, Kevin P
    Page Should Contain  text=Probabilistic machine learning: an introduction
    Page Should Contain  text=2022
    Page Should Contain  text=Murphy2022Probabilistic

Add A Conference Reference
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  conference
    Set Title  Probabilistic machine learning: an introduction
    Set Year  2022
    Set Booktitle  booktitle test
    Submit 
    Page Should Contain  text=Murphy, Kevin P
    Page Should Contain  text=Probabilistic machine learning: an introduction
    Page Should Contain  text=2022
    Page Should Contain  text=Murphy2022Probabilistic
    Page Should Contain  text=booktitle test

Add A Inbook Reference
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  inbook
    Set Title  Probabilistic machine learning: an introduction
    Set Year  2022
    Set Chapter  chapter test
    Set Pages  pages test
    Set Publisher  publisher test
    Submit 
    Page Should Contain  text=Murphy, Kevin P
    Page Should Contain  text=Probabilistic machine learning: an introduction
    Page Should Contain  text=2022
    Page Should Contain  text=Murphy2022Probabilistic
    Page Should Contain  text=chapter test
    Page Should Contain  text=pages test
    Page Should Contain  text=publisher test

Add A Incollection Reference
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  incollection
    Set Title  Probabilistic machine learning: an introduction
    Set Year  2022
    Set Booktitle  booktitle test
    Set Publisher  publisher test
    Submit 
    Page Should Contain  text=Murphy, Kevin P
    Page Should Contain  text=Probabilistic machine learning: an introduction
    Page Should Contain  text=2022
    Page Should Contain  text=Murphy2022Probabilistic
    Page Should Contain  text=booktitle test
    Page Should Contain  text=publisher test

Add A Inproceedings Reference
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  inproceedings
    Set Title  Probabilistic machine learning: an introduction
    Set Year  2022
    Set Booktitle  booktitle test
    Submit 
    Page Should Contain  text=Murphy, Kevin P
    Page Should Contain  text=Probabilistic machine learning: an introduction
    Page Should Contain  text=2022
    Page Should Contain  text=Murphy2022Probabilistic
    Page Should Contain  text=booktitle test

Add A Manual Reference
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  manual
    Set Title  Probabilistic machine learning: an introduction
    Set Year  2022
    Submit 
    Page Should Contain  text=Murphy, Kevin P
    Page Should Contain  text=Probabilistic machine learning: an introduction
    Page Should Contain  text=2022
    Page Should Contain  text=Murphy2022Probabilistic

Add A Mastersthesis Reference
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  mastersthesis
    Set Title  Probabilistic machine learning: an introduction
    Set Year  2022
    Set School  school test
    Submit 
    Page Should Contain  text=Murphy, Kevin P
    Page Should Contain  text=Probabilistic machine learning: an introduction
    Page Should Contain  text=2022
    Page Should Contain  text=Murphy2022Probabilistic
    Page Should Contain  text=school test

Add A Phdthesis Reference
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  phdthesis
    Set Title  Probabilistic machine learning: an introduction
    Set Year  2022
    Set School  school test
    Submit 
    Page Should Contain  text=Murphy, Kevin P
    Page Should Contain  text=Probabilistic machine learning: an introduction
    Page Should Contain  text=2022
    Page Should Contain  text=Murphy2022Probabilistic
    Page Should Contain  text=school test

Add A Proceedings Reference
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  proceedings
    Set Title  Probabilistic machine learning: an introduction
    Set Year  2022
    Submit 
    Page Should Contain  text=Murphy, Kevin P
    Page Should Contain  text=Probabilistic machine learning: an introduction
    Page Should Contain  text=2022
    Page Should Contain  text=Murphy2022Probabilistic

Add A Techreport Reference
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  techreport
    Set Title  Probabilistic machine learning: an introduction
    Set Year  2022
    Set Institution  institution test
    Submit 
    Page Should Contain  text=Murphy, Kevin P
    Page Should Contain  text=Probabilistic machine learning: an introduction
    Page Should Contain  text=2022
    Page Should Contain  text=Murphy2022Probabilistic
    Page Should Contain  text=institution test

Add A Unpublished Reference
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  unpublished
    Set Title  Probabilistic machine learning: an introduction
    Set Year  2022
    Set Note  note test
    Submit 
    Page Should Contain  text=Murphy, Kevin P
    Page Should Contain  text=Probabilistic machine learning: an introduction
    Page Should Contain  text=2022
    Page Should Contain  text=Murphy2022Probabilistic
    Page Should Contain  text=note test

Add A Misc Reference
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  misc
    Set Title  Probabilistic machine learning: an introduction
    Set Year  2022
    Submit 
    Page Should Contain  text=Murphy, Kevin P
    Page Should Contain  text=Probabilistic machine learning: an introduction
    Page Should Contain  text=2022
    Page Should Contain  text=Murphy2022Probabilistic

Add A Booklet Reference With All Optional Fields
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  booklet
    Set Title  Probabilistic machine learning: an introduction
    Set Year  2022
    Set Howpublished  howpublished test
    Set Address  address test
    Set Month  month test
    Set Note  note test
    Submit
    Page Should Contain  text=howpublished test
    Page Should Contain  text=address test
    Page Should Contain  text=month test
    Page Should Contain  text=note test

Add A Conference Reference With All Optional Fields
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  conference
    Set Title  Probabilistic machine learning: an introduction
    Set Year  2022
    Set Booktitle  booktitle test
    Set Editor  editor test
    Set Volume  volume test
    Set Number  number test
    Set Series  series test
    Set Pages  pages test
    Set Address  address test
    Set Month  month test
    Set Organization  organization test
    Set Publisher  publisher test
    Set Note  note test
    Submit
    Page Should Contain  text=booktitle test
    Page Should Contain  text=editor test
    Page Should Contain  text=volume test
    Page Should Contain  text=number test
    Page Should Contain  text=series test
    Page Should Contain  text=pages test
    Page Should Contain  text=address test
    Page Should Contain  text=month test
    Page Should Contain  text=organization test
    Page Should Contain  text=publisher test
    Page Should Contain  text=note test

Add A Inbook Reference With All Optional Fields
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  inbook
    Set Title  Probabilistic machine learning: an introduction
    Set Year  2022
    Set Chapter  chapter test
    Set Pages  pages test
    Set Publisher  publisher test
    Set Volume  volume test
    Set Series  series test
    Set Address  address test
    Set Edition  edition test
    Set Month  month test
    Set Note  note test
    Submit
    Page Should Contain  text=chapter test
    Page Should Contain  text=pages test
    Page Should Contain  text=publisher test
    Page Should Contain  text=volume test
    Page Should Contain  text=series test
    Page Should Contain  text=address test
    Page Should Contain  text=edition test
    Page Should Contain  text=month test
    Page Should Contain  text=note test

Add A Incollection Reference With All Optional Fields
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  incollection
    Set Title  Probabilistic machine learning: an introduction
    Set Year  2022
    Set Booktitle  booktitle test
    Set Publisher  publisher test
    Set Editor  editor test
    Set Volume  volume test
    Set Number  number test
    Set Series  series test
    Set Type  type test
    Set Chapter  chapter test
    Set Pages  pages test
    Set Address  address test
    Set Edition  edition test
    Set Month  month test
    Set Note  note test
    Submit
    Page Should Contain  text=booktitle test
    Page Should Contain  text=publisher test
    Page Should Contain  text=editor test
    Page Should Contain  text=volume test
    Page Should Contain  text=number test
    Page Should Contain  text=series test
    Page Should Contain  text=type test
    Page Should Contain  text=chapter test
    Page Should Contain  text=pages test
    Page Should Contain  text=address test
    Page Should Contain  text=edition test
    Page Should Contain  text=month test
    Page Should Contain  text=note test

Add A Inproceedings Reference With All Optional Fields
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  inproceedings
    Set Title  Probabilistic machine learning: an introduction
    Set Year  2022
    Set Booktitle  booktitle test
    Set Editor  editor test
    Set Volume  volume test
    Set Number  number test
    Set Series  series test
    Set Pages  pages test
    Set Address  address test
    Set Month  month test
    Set Organization  organization test
    Set Publisher  publisher test
    Set Note  note test
    Submit
    Page Should Contain  text=booktitle test
    Page Should Contain  text=editor test
    Page Should Contain  text=volume test
    Page Should Contain  text=number test
    Page Should Contain  text=series test
    Page Should Contain  text=pages test
    Page Should Contain  text=address test
    Page Should Contain  text=month test
    Page Should Contain  text=organization test
    Page Should Contain  text=publisher test
    Page Should Contain  text=note test

Add A Manual Reference With All Optional Fields
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  manual
    Set Title  Probabilistic machine learning: an introduction
    Set Year  2022
    Set Organization  organization test
    Set Address  address test
    Set Edition  edition test
    Set Month  month test
    Set Note  note test
    Submit
    Page Should Contain  text=organization test
    Page Should Contain  text=address test
    Page Should Contain  text=edition test
    Page Should Contain  text=month test
    Page Should Contain  text=note test

Add A Mastersthesis Reference With All Optional Fields
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  mastersthesis
    Set Title  Probabilistic machine learning: an introduction
    Set Year  2022
    Set School  school test
    Set Type  type test
    Set Address  address test
    Set Month  month test
    Set Note  note test
    Submit
    Page Should Contain  text=school test
    Page Should Contain  text=type test
    Page Should Contain  text=address test
    Page Should Contain  text=month test
    Page Should Contain  text=note test

Add A Phdthesis Reference With All Optional Fields
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  phdthesis
    Set Title  Probabilistic machine learning: an introduction
    Set Year  2022
    Set School  school test
    Set Type  type test
    Set Address  address test
    Set Month  month test
    Set Note  note test
    Submit
    Page Should Contain  text=school test
    Page Should Contain  text=type test
    Page Should Contain  text=address test
    Page Should Contain  text=month test
    Page Should Contain  text=note test

Add A Proceedings Reference With All Optional Fields
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  proceedings
    Set Title  Probabilistic machine learning: an introduction
    Set Year  2022
    Set Editor  editor test
    Set Volume  volume test
    Set Number  number test
    Set Series  series test
    Set Address  address test
    Set Publisher  publisher test
    Set Note  note test
    Set Month  month test
    Set Organization  organization test
    Submit
    Page Should Contain  text=editor test
    Page Should Contain  text=volume test
    Page Should Contain  text=number test
    Page Should Contain  text=series test
    Page Should Contain  text=address test
    Page Should Contain  text=publisher test
    Page Should Contain  text=note test
    Page Should Contain  text=month test
    Page Should Contain  text=organization test

Add A Techreport Reference With All Optional Fields
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  techreport
    Set Title  Probabilistic machine learning: an introduction
    Set Year  2022
    Set Institution  institution test
    Set Type  type test
    Set Number  number test
    Set Address  address test
    Set Month  month test
    Set Note  note test
    Submit
    Page Should Contain  text=institution test
    Page Should Contain  text=type test
    Page Should Contain  text=number test
    Page Should Contain  text=address test
    Page Should Contain  text=month test
    Page Should Contain  text=note test

Add A Unpublished Reference With All Optional Fields
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  unpublished
    Set Title  Probabilistic machine learning: an introduction
    Set Year  2022
    Set Note  note test
    Set Month  month test
    Submit
    Page Should Contain  text=note test
    Page Should Contain  text=month test

Add A Misc Reference With All Optional Fields
    Click Link  New reference
    Set First name  Kevin P
    Set Last name  Murphy
    Click Button  Add author
    Select Reference Type  misc
    Set Title  Probabilistic machine learning: an introduction
    Set Year  2022
    Set Howpublished  howpublished test
    Set Month  month test
    Set Note  note test
    Submit
    Page Should Contain  text=howpublished test
    Page Should Contain  text=month test
    Page Should Contain  text=note test

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

Set Howpublished
    [Arguments]  ${howpublished}
    Input Text  howpublished  ${howpublished}

Set Booktitle
    [Arguments]  ${booktitle}
    Input Text  booktitle  ${booktitle}

Set Editor
    [Arguments]  ${editor}
    Input Text  editor  ${editor}

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

Set Journal
    [Arguments]  ${journal}
    Input Text  journal  ${journal}

Set Number
    [Arguments]  ${number}
    Input Text  number  ${number}

Set Pages
    [Arguments]  ${pages}
    Input Text  pages  ${pages}

Set Organization
    [Arguments]  ${organization}
    Input Text  organization  ${organization}

Set Chapter
    [Arguments]  ${chapter}
    Input Text  chapter  ${chapter}

Set Type
    [Arguments]  ${type}
    Input Text  type  ${type}

Set School
    [Arguments]  ${school}
    Input Text  school  ${school}

Set Institution
    [Arguments]  ${institution}
    Input Text  institution  ${institution}