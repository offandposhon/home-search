# Advanced Zillow API Search 

### Combines the following criteria for a more advanced search than what the Zillow website provides:
  - Location search based off city, state (zipcode not tested)
  - Price Minimum / Maximum
  - Property Type (Single family home, Townhouse, Condo)
  - Contract type (ForSale, ForRent)
  - Minimum Square Footage
  - Minimum Bedroom Count
  - Minimum Bathroom Count
  - Minimum Elementary / Primary school rating (1-10)
  - Minimum Walkability score (1-100) - (How walkable / pedestrian-friendly the area is)
  - Maximum Commute Time (Configurable start / end destination)
    - Important: Commute start time is always "now". For accurate rush-hour commute-times, try running this during morning/evening rush-hour. Directions provided by Mapbox

# How to use

- Gather API keys
  - Unofficial Zillow API via rapid api (https://rapidapi.com/apimaker/api/zillow-com1/details)
  - Mapbox Directions API (https://account.mapbox.com/auth/signup/)

- Create virtual environment (optional)
  - `python3 -m venv hsearch`

- Activate virtual env:
  - `source ./hsearch/bin/activate`

- install dependencies 
  - `pip install -r requirements.txt`

- create environment file: `touch ./.env` 
  - add the following keys
    - RAPID_API_KEY
      - (add your token/secret)
    - MAPBOX_API_KEY
      - (add your token/secret)

- Input your desired values at the top of `search_houses.py`
- Run the advanced search: `python3 ./search_houses.py`
- Results will be output to console in the form of Zillow URL's that you can paste into your browser







