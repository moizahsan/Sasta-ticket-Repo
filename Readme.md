# DataScience API

This API serves the DS API microservice. This service contains APIs for:
- Free cancellation fees calculation
- Date change fees calculation

## How to use
A few prerequisites are required to set this up on your local machine
- .envs/.local/.postgres file
- config.json in dsapi/settings file
```
{
  "DATABASE_URI": "postgresql://XYZ:REPLACE_ME@postgres:5432/REPLACE_ME",
  "DREMIO_USERNAME": "REPLACE_ME",
  "DREMIO_PASSWORD": "REPLACE_ME"
}
```
- Run the following commands to start the localhost on port 5000
```
make init (run individual commands from the Makefile if error is shown)
```
- Utilize curl or postman to hit API

## API Docs
API docs are available on http://localhost:5000/swagger-ui

## Workflows
Workflows added in main.yml in .github. 15 Sept 2022. Test push
