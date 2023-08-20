## Instructions:

**In order to run locally**:</br>
create a copy of config-example.ini on its same folder and call it config.ini. The client api will be exposed at port 5000.

**In order to run with docker**:</br>
run docker-compose up --build from within client folder. The client api will be exposed at port 5001.

#### Implementation Notes:
1. In order to check if an email is valid, we're taking into account only the email format. (If we'd want to also verify that the address really exists, we'd need of course to do some external call.)
2. The code attempts to retrieve the currency rates from the internet. If not available, it uses file rates.json.
3. When an error is found in one of the payments: payment is ignored, error is written to log, flow continues.
4. There are 2 rates files: ideally, we'd update the one in the root level from time to time, while the one in the tests folder can remain the same.