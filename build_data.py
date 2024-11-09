import county_demographics

from data import CountyDemographics


# Given county demographics in dictionary form, convert to an object.
# input: county demographics information as an inconsistently typed dictionary
# output: the county demographics information as a CountyDemographics object
#
# Note that this function assumes the dictionary is properly structured.
def convert_county(county) -> CountyDemographics:
    if 'Median Houseold Income' in county['Income']:
        county['Income']['Median Household Income'] =\
                county['Income']['Median Houseold Income']
        del county['Income']['Median Houseold Income']
    return CountyDemographics(
            county['Age'],
            county['County'],
            county['Education'],
            county['Ethnicities'],
            county['Income'],
            county['Population'],
            county['State']
        )


# To avoid reprocessing the full data set on multiple calls of get_data.
_converted = None


# This function retrieves the full demographics data set and converts
# it to store each entry as a CountyDemographics object.
# input: no input
# output: county information as a list of CountyDemographics objects
def get_data() -> list[CountyDemographics]:
    global _converted
    if not _converted:
       report = county_demographics.get_report()
       _converted = [convert_county(county) for county in report]
    return _converted

def population_total(counties: List[data.CountyDemographics]) -> int:
    """Calculate the total 2014 population across the set of counties in the provided list.
    input: A list of CountyDemographics objects
    output: The total 2014 population as an integer
    """
    total_population = 0
    for county in counties:
        total_population += county.demographics['2014 Population']
    return total_population

def filter_by_state(counties: list[CountyDemographics], state_abbr: str) -> list[CountyDemographics]:
    """Filter the list of counties to only include those in the specified state.
    Input:
        counties (list[CountyDemographics]): List of CountyDemographics objects.
        state_abbr (str): The two-letter state abbreviation to filter by.
    Output:
        list[CountyDemographics]: A list of counties in the specified state.
    """
    filtered_counties = [county for county in counties if county.state == state_abbr]
    return filtered_counties

def population_by_education(counties: list[CountyDemographics], education_key: str) -> float:
    """
    Calculate the total sub-population for the specified education level across all counties.

    Input:
        counties (list[CountyDemographics]): List of CountyDemographics objects.
        education_key (str): The education level to look for (e.g., "Bachelor's Degree or Higher").

    Putput:
        float: The total population with the specified education level across the counties.
    """
    total_population = 0.0
    for county in counties:
        # Get the education data for the county
        education_data = county.education
        if education_key in education_data:
            # Calculate sub-population based on percentage of total population
            education_percent = education_data[education_key]
            county_population = county.demographics['2014 Population']
            total_population += (education_percent / 100) * county_population
    return total_population

def population_by_ethnicity(counties: list[CountyDemographics], ethnicity_key: str) -> float:
    """Calculate the total sub-population for the specified ethnicity across all counties.

   Input:
        counties (list[CountyDemographics]): List of CountyDemographics objects.
        ethnicity_key (str): The ethnicity key to look for (e.g., 'Two or More Races').

    Output:
        float: The total population with the specified ethnicity across the counties.
    """
    total_population = 0.0
    for county in counties:
        # Get the ethnicity data for the county
        ethnicity_data = county.ethnicity
        if ethnicity_key in ethnicity_data:
            # Calculate sub-population based on percentage of total population
            ethnicity_percent = ethnicity_data[ethnicity_key]
            county_population = county.demographics['2014 Population']
            total_population += (ethnicity_percent / 100) * county_population
    return total_population

def population_below_poverty_level(counties: list[CountyDemographics]) -> float:
    """Calculate the total population below the poverty level across all counties.

    Input:
        counties (list[CountyDemographics]): List of CountyDemographics objects.

    Output:
        float: The total population below the poverty level across the counties.
    """
    total_population = 0.0
    for county in counties:
        # Get the poverty level data for the county
        poverty_data = county.income
        if 'Persons Below Poverty Level' in poverty_data:
            # Calculate sub-population based on percentage of total population
            poverty_percent = poverty_data['Persons Below Poverty Level']
            county_population = county.demographics['2014 Population']
            total_population += (poverty_percent / 100) * county_population
    return total_population


def percent_by_education(counties: list[CountyDemographics], education_key: str) -> float:
    """Calculate the percentage of the specified education level sub-population
    relative to the total 2014 population across all counties.

    input:
        counties (list[CountyDemographics]): List of CountyDemographics objects.
        education_key (str): The education level to look for (e.g., "Bachelor's Degree or Higher").

    output:
        float: The percentage of the specified education level sub-population.
    """
    # Total population across all counties
    total_population = population_total(counties)

    # Population for the specified education level
    education_population = population_by_education(counties, education_key)

    # Return percentage if total population is greater than 0, otherwise return 0
    if total_population > 0:
        return (education_population / total_population) * 100
    return 0.0


def percent_by_ethnicity(counties: list[CountyDemographics], ethnicity_key: str) -> float:
    """Calculate the percentage of the specified ethnicity sub-population
    relative to the total 2014 population across all counties.

    Input:
        counties (list[CountyDemographics]): List of CountyDemographics objects.
        ethnicity_key (str): The ethnicity key to look for (e.g., 'Two or More Races').

    Output:
        float: The percentage of the specified ethnicity sub-population.
    """
    # Total population across all counties
    total_population = population_total(counties)

    # Population for the specified ethnicity
    ethnicity_population = population_by_ethnicity(counties, ethnicity_key)

    # Return percentage if total population is greater than 0, otherwise return 0
    if total_population > 0:
        return (ethnicity_population / total_population) * 100
    return 0.0


def percent_below_poverty_level(counties: list[CountyDemographics]) -> float:
    """Calculate the percentage of the population below the poverty level relative
    to the total 2014 population across all counties.

    Input:
        counties (list[CountyDemographics]): List of CountyDemographics objects.

    Output:
        float: The percentage of the population below the poverty level.
    """
    # Total population across all counties
    total_population = population_total(counties)

    # Population below poverty level
    poverty_population = population_below_poverty_level(counties)

    # Return percentage if total population is greater than 0, otherwise return 0
    if total_population > 0:
        return (poverty_population / total_population) * 100
    return 0.0

def education_greater_than(counties: list[CountyDemographics], education_key: str, threshold: float) -> list[CountyDemographics]:
    """Return a list of counties where the value for the specified education key is greater than the threshold.

    Input:
        counties (list[CountyDemographics]): List of CountyDemographics objects.
        education_key (str): The education key to filter by (e.g., "Bachelor's Degree or Higher").
        threshold (float): The threshold value.

    Output:
        list[CountyDemographics]: A list of CountyDemographics objects that meet the condition.
    """
    return [county for county in counties if county.education.get(education_key, 0) > threshold]

def education_less_than(counties: list[CountyDemographics], education_key: str, threshold: float) -> list[CountyDemographics]:
    """Return a list of counties where the value for the specified education key is less than the threshold.

    Input:
        counties (list[CountyDemographics]): List of CountyDemographics objects.
        education_key (str): The education key to filter by (e.g., "Bachelor's Degree or Higher").
        threshold (float): The threshold value.

    Output:
        list[CountyDemographics]: A list of CountyDemographics objects that meet the condition.
    """
    return [county for county in counties if county.education.get(education_key, 0) < threshold]

def ethnicity_greater_than(counties: list[CountyDemographics], ethnicity_key: str, threshold: float) -> list[CountyDemographics]:
    """Return a list of counties where the value for the specified ethnicity key is greater than the threshold.

    Input:
        counties (list[CountyDemographics]): List of CountyDemographics objects.
        ethnicity_key (str): The ethnicity key to filter by (e.g., 'Hispanic or Latino').
        threshold (float): The threshold value.

    Output:
        list[CountyDemographics]: A list of CountyDemographics objects that meet the condition.
    """
    return [county for county in counties if county.ethnicity.get(ethnicity_key, 0) > threshold]

def ethnicity_less_than(counties: list[CountyDemographics], ethnicity_key: str, threshold: float) -> list[CountyDemographics]:
    """Return a list of counties where the value for the specified ethnicity key is less than the threshold.

    Input:
        counties (list[CountyDemographics]): List of CountyDemographics objects.
        ethnicity_key (str): The ethnicity key to filter by (e.g., 'Hispanic or Latino').
        threshold (float): The threshold value.

    OUtput:
        list[CountyDemographics]: A list of CountyDemographics objects that meet the condition.
    """
    return [county for county in counties if county.ethnicity.get(ethnicity_key, 0) < threshold]

def below_poverty_level_greater_than(counties: list[CountyDemographics], threshold: float) -> list[CountyDemographics]:
    """Return a list of counties where the percentage of the population below the poverty level is greater than the threshold.

    input:
        counties (list[CountyDemographics]): List of CountyDemographics objects.
        threshold (float): The threshold value for the percentage of people below the poverty level.

    output:
        list[CountyDemographics]: A list of CountyDemographics objects that meet the condition.
    """
    return [county for county in counties if county.income.get('Persons Below Poverty Level', 0) > threshold]

def below_poverty_level_less_than(counties: list[CountyDemographics], threshold: float) -> list[CountyDemographics]:
    """Return a list of counties where the percentage of the population below the poverty level is less than the threshold.

    input:
        counties (list[CountyDemographics]): List of CountyDemographics objects.
        threshold (float): The threshold value for the percentage of people below the poverty level.

  output:
        list[CountyDemographics]: A list of CountyDemographics objects that meet the condition.
    """
    return [county for county in counties if county.income.get('Persons Below Poverty Level', 0) < threshold]

