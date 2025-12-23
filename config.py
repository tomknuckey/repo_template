election_dates = [
    "1945-07-05", "1950-02-23", "1951-10-25", "1955-05-26", "1959-10-08",
    "1964-10-15", "1966-03-31", "1970-06-18", "1974-02-28", "1974-10-10",
    "1979-05-03", "1983-06-09", "1987-06-11", "1992-04-09", "1997-05-01",
    "2001-06-07", "2005-05-05", "2010-05-06", "2015-05-07", "2017-06-08",
    "2019-12-12"
]


#Initial Model
features = ["Incumbent_Duration_Days", "GDP_YoY", "Inflation_YoY", "Unemployment Rate", 
"Incumbent_Labour_election", "Falklands_War_Flag", "Covid_Pandemic_Flag", "majority", 
]
target = "Incumbent_Win"

scale_mode = True
