sequenceDiagram
    participant browser
    participant server

    
    Note right of browser: The user writes something and clicks the save button.
    Note right of browser: The javascripts saves the form in local list and renders the page.


    browser->>server: Post https://studies.cs.helsinki.fi/exampleapp/new_note_spa
    activate server
    Note right of browser:The POST request to the address new_note_spa contains the new note as JSON data containing both the content of the note (content) and the timestamp (date)

    server-->>browser: 201 Created
    deactivate server
    
   
    Note right of browser: The browser remains on the same page witthout calling http
