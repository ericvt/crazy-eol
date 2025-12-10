You are an expert in analyzing structured data.
Your challenge is to look at a set of data and determining action and/or research needed to solve a specific problem:

Data: use data_processed.csv

Context:
the data is structured by "Tenant", Tenants are logical grouping of "Branch". There can be mutliple branches for a given Tenant and branch cannot belong to many tenant (one to many relationship).Branches contain technical articles of different types. Those types are represented by the "Content Group Category" field. Each of these types can be localized into different Translation Flavor and into a set of cultures listed in the "Cultures" field. A culture is a locale such as "ja-jp"
We will leave the other fields for now as they will not be relevant for the analysis we want to do.

Analysis #1
A) Show: unique tenants, unique branches, unique Content Group category, unique cultures and unique Translation flavors. Show numbers and values in a table only, no details needed
b) Show: Branch to Content Group Category combination. How many Culture grouping ?
c) Show : Minimum culture in a grouping, maximum cultures in a grouping, Average cultures per grouping

Analysis #2
Using data from #1
Show relationship between Content Group Categories and Translation Flavors.
Is there any rows that identical?

Analysis #3
A) Calculate and list the cultures applied to MT Translation Flavor. Show that as "MT supported locales"
Calculate and list the cultures not applied to MT Translation Flavor. Show that as "MT non-supported locales"
B) Calculate and list the cultures applied to AIPE Translation Flavor. Show that as "AIPE supported locales"
Calculate and list the cultures not applied to AIPE Translation Flavor. Show that as "AIPE non-supported locales"

Analysis #4
Using the analysis 1 thru 3, is there any branch where translation flavor = MT that does not match the full culture list from "MT supported locales", meaning are we missing MT supported cultures for those branches

Analysis #5 - Find out the most common culture. For this particular culture:
a) calculate the number of unique branches it is included in
b) How many unique branch does not include that culture

Always display the % against the overall dataset
Stick to showing the numbers asked only. Do not report key findings or examples.
Generate the result into a markdown file called report.md under the claude folder.