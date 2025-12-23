

0. Check that the data is probably useful



1. Define the Problem 


### Aims

We want to understand what causes political parties to rise / fall in the polls, for example whether it's unemployment, GDP or inflation, in comparison to length in power.

Would be also intresting to see the casual nature of whether for example a local scandal effects polling more in that area

Also how well polling predicts the actual results


**Benefits**

Useful for political parties to determine what factors could cause this issue

**Caveats**

Unemployment Data only up to 2016 - sure can find other data

Sample size is small, with about 20 elections

There will be change in how people think for example different attitudes to immigration

Data is at county level as the lowest granularity

Maybe other can be found here https://www.electoralcalculus.co.uk/flatfile.html

Election that data says was 1975 was 1974

Unemployment Data is only from 1971, meaning in order to use that we need to either filter things out, get a new data source or something smart

    
2. Research Related Work



3. Understand the Data - Crap in / Crap out

There is useful data, when creating the target variable of incumbent poll lead, which is how much the current party in power is winning by in the polls we can that there are factors that correlate with it.

This is intuitive where GDP Growth is positively correlated, where unemployment %, inflation and length of duration in power is negatively correlated.

Other factors will be important as wel


### Analytical Questions

* Get a combined single dataset, then can do plots / eda

For example

* Correlation between time in goverment and polling

* Correlation between unemployment and polling 

Start looking at causal things

Need to get election dates 


4. Plan for Validation


5. Develop a Baseline Model

6. Iterate and Improve


7. Deploy Monitor and Maintain 
