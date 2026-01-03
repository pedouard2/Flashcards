<%*
let title = await tp.system.prompt("Chapter/Note Title") || "New_Note";
await tp.file.rename(title);
let path = tp.file.folder(true).replace(/\//g, "::");
%>
TARGET DECK: <% path %>::<% title %>

Q: 
A: