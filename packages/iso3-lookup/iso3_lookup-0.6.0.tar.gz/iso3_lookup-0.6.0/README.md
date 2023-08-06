# iso3_lookup

Small python package to lookup country iso3 codes from the country name and visa-versa. 

## Install 
```
pip3 install iso3-lookup
```

## About
Does exactly what it says on the tin - user can quickly go between iso3 codes and country name,
currently uses fuzzy logic so spelling isn't too critical however if the algorithm really isn' confident it 
will return an error. The underlying data comes from [this](https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes) 
excellent package and the latest version is pulled when the functions are imported so therefore an internet connection is required.   

## Usage 
- `get_iso3(country)` - get the iso3 code from the country name.
- `get_country(iso3)` - get the country name from the iso3 code.
