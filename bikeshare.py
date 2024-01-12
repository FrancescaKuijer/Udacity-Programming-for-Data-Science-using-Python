import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        city = input("Let's select a city! Which city are you interested "+
                     "in: Chicago, New York City or Washington?\n\n")
        city = city.lower()
        
        if city in ('new york city', 'chicago', 'washington'):
            break
        print("Please enter a valid city.")
            
    while True:
        month = input("Which month would you like to analyze " + city.title() + 
                      "? You can choose between January, February, March, " +
                      "April, May and June, or type all if you do not wish "+
                      "to specify a month.\n\n Warning!: Only the first six months of the year can be chosen " +
                      "as for the other months there is a lack in user data.")
        month = month.lower()
        
        if month in ('january', 'february', 'march', 'april', 'may', 
                         'june', 'all'):
            break
        print("Please enter a valid month.")

    while True:
        day = input("Let's pick a day." +
                    "You can choose between Monday, Tuesday, Wednesday," +
                    "Thursday, Friday, Saturday, Sunday, or type all if " +
                    "you do not wish to specify a day.\n\n")
        day = day.lower()
        
        if day in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                       'saturday', 'sunday', 'all'):
            break
        print("Please enter a valid day.")            

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    print("\nLoading data...")
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) +1
        df = df[df['month'] == month]
    
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if month == 'All':
        pop_month = df['month'].mode()[0] if not df['month'].mode().empty else 'N/A'

        months = ['January', 'February', 'March', 'April', 'May', 'June']
        pop_month = months(pop_month -1) if pop_month != 'N/A' else pop_month
        print(f"The Most Popular Month is (1 = January, ..., 6 = June): {pop_month}")
    
    if day == 'All':
        pop_day = df['weekday'].mode()[0] if not df['day_of_week'].mode().empty else 'N/A'
        print(f"The Most Popular Day is: {pop_day}")


    df['hour'] = df ['Start Time'].dt.hour
    pop_hour = df['hour'].mode()[0] if not df['hour'].mode().empty else 'N/A'
    print(f"The Most Popular Start Hour: {pop_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    common_start_station = df['Start Station'].mode() [0] if not df['Start Station'].mode().empty else 'N/A'
    print("The most commonly used start station is {}".format(common_start_station))

    common_end_station = df['End Station'].mode()[0] if not df['End Station'].mode().empty else 'N/A'
    print("The most commonly used end station is {}".format(common_end_station))

    df['Combination'] = df['Start Station'] + " to " + df['End Station']
    pop_com = df['Combination'].mode()[0] if not df['Combination'].mode().empty else 'N/A'
    print("The most frequent combination of Start and End Station is {}".format(pop_com))
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_duration = df['Trip Duration'].sum()
    minute,second = divmod(total_duration, 60)
    hour,minute = divmod(minute, 60)

    print("The total trip duration is {} hour(s), {} minute(s) and {} second(s).".format(hour, minute, second))
        
    average_duration = df['Trip Duration'].mean()
    minute,second = divmod(average_duration, 60)
    hour,minute = divmod(minute, 60)

    if minute > 60:
        hour,minute = divmod(minute, 60)
        print("The average trip duration is {} hour(s), {} minute(s) and {} second(s).".format(hour,minute,second))
            
    else:
        print("\nThe average trip duration is {} minute(s) {} second(s).".format(minute,second))
            
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_type = df['User Type'].value_counts()
    print("The user types are:\n", user_type)

    try: 
        gender= df['Gender'].value_counts()
        print(f"\nThe types of users by gender are given below: \n\n{gender}")
    except KeyError: 
        print("There is no 'Gender' column in this file.")

    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f"\nThe earliest year of birth:{earliest}\n\nThe most recent year of birth: {recent}\n\nThe most common year of birth: {common_year}")
        
    except KeyError: 
        print("There are no birth year details in this file.")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays 5 rows of data from the csv file for the selected city.
    
    Args: 
        param1 (df): The data frame you wish to work with.
        
    
    Returns:
        None.
    """

    while True:
        response = ['yes','no']
        choice = input("Would you like to view individual trip data (5 entries)? Type 'Y' or 'N'\n").lower()
        if choice in response:
            if choice == 'yes':
                start = 0
                end = 5
                data = df.iloc[start:end,:9]
                print(data)
            break     
        else:
            print("Please enter a valid response")

    if  choice =='yes':       
            while True:
                choice_2= input("Would you like to view more trip data? Type 'Yes' or 'No'\n").lower()
                if choice_2 in response:
                    if choice_2 =='yes':
                        start += 5
                        end += 5
                        data = df.iloc[start:end,:9]
                        print(data)
                    else:    
                        break  
                else:
                    print("Please enter a valid response.")              



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter 'Yes' or 'No'.\n')
        if restart.lower() != 'yes':
            print('See you next time.')
            break


if __name__ == "__main__":
	main()