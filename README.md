# paste-site
A pretty trivial paste site on i’m working on. Don’t expect too much from it

## Deployment
1. clone the repo

2. Make a postgres database named `pastesite`, and create a table with this code: 
```sql
CREATE TABLE pastes(id VARCHAR(255) PRIMARY KEY, content TEXT);
```

3. make a .env file with your potsgres password as "POSTGRES_PASS"
4. Run the file.


Thanks to Tom and Jay for the (soon to be done) frontend.
