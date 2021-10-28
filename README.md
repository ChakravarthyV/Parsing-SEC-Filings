Benjamin Graham, the father of value investing, formulated his conservative approach to security valuation during the Great Depression. By adhering to the simple axiom of
purchasing a company's shares if and only if current assets net out total liabilities by an amount far greater (>50%) than its market capitalization, Graham put up an annualized rate of ~20% 
from 1936 to 1956. Not surprisingly, the straightfoward arithmetic quickly turned into the now widely recognized neologism "net-net working capital."

The program performs two calculations: net-net working capital (NNWC) and adjusted net asset value (NAV). The latter is defined as total assets less total liabilities, 
while allowing the investor to account for any asset writedowns.

Using a company's unique Central Index Key, a single API call to SEC's EDGAR can deliver quarterly financial data in one sizeable JSON file. For example, Apple's CIK #
is 0000320193 and the API call to https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json provides what is needed.
A perusal of this webpage eventually reveals a feasible method to parse the file and clean up the underlying data structure. 

** The program has in it the implementation of such an algorithm -- one that can generalize to provide orderly financial datasets for any SEC-registered company. 
The calculations of NNWC and NAV are simply direct applications of that algorithm. **


