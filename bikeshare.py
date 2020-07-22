# A special thanks to the many learners and mentors on Udacity - their comments, questions and help/answers were able to lead me in the 
# proper directions to find answers, help and guidance. Also, thanks to StackOverflow where I found most of the answers!

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
    print("\n\nHello Fellow Rider! Why don't we explore some US bikeshare data!?!\n")
    # has user input a city (chicago, new york city, washington).
    city_input = input("Choose a city to explore: Chicago, New York City or Washington!: ").lower()
    while city_input not in ["chicago","new york city","washington"]:
        city_input = input("I didn't quite get that! Please enter the full name of the city: Chicago, New York City or Washington: ").lower()
    city = city_input
    # has user input a month (all, january, february, ... , june)
    month_input = input("\nWould you like to filter by a certain month? Please enter a month - January thru June - or 'all' for no filter!: ").lower()
    while month_input not in ['january', 'february', 'march', 'april', 'may', 'june','all']:
        month_input = input("\nI didn't quite get that! Would you like to filter by a certain month? Please enter a month - January thru June - or 'all' for no filter!: ").lower()
    month = month_input    
    # has user input a day of the week (all, monday, tuesday, ... sunday)
    day_input = input("\nWould you like to filter by a day of the week? Please enter the day of the week - Monday thru Sunday - or 'all' for no filter!: ").title()
    while day_input not in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','All']:
        day_input = input("\nPlease enter that one again! Would you like to filter by a day of the week? Please enter the day of the week - Monday thru Sunday - or 'all' for no filter!: ").title()
    day = day_input
    print('-'*40,'\n\n')  
    return city, month, day



def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day, if applicable
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
        
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # apply filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # apply filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()] 
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\n\n\n','*'*73)  
    print(' ***** Let\'s check out some statistics based on your filtered data!! *****')
    print('','*'*73,'\n\n\n')
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])         

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    common_month = df['month'].mode()[0]
    
    print('The most common month of use (by month number - January = 1): ',common_month)

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    common_day = df['day_of_week'].mode()[0]
    print('The most common day of the week: ',common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('The most common hour (24-hour clock): ',common_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40,'\n\n')  


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('The most commonly used Start Station was {}.\n'.format(common_start))

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('The most commonly used End Station was {}.\n'.format(common_end))

    # create column for the "trip" - start to end stations
    df['trip_stations'] = df['Start Station'] + ' to ' + df['End Station']
    # display most frequent combination of start station and end station trip
    common_station_combo = df['trip_stations'].mode()[0]
    print('The most common combination of start and end stations for a trip was {}.\n'.format(common_station_combo))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40,'\n\n')  
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Durations...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print('The total time spent on all trips/travel was {} seconds!\n'.format(total_travel))
    print('For those of us that don\'t count in seconds, that\'s more than {} days of total ride time!!\n'.format(total_travel//86400))
    
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The average time spent on a trip, however, was only {} seconds or approximately {} minutes!\n'.format(mean_travel_time, mean_travel_time//60))
    print('That means we had a ton of riders making tons of trips!!\n')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40,'\n\n')  

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Of the two main types of Users - Subscribers and Customers - we have:\n')
    print(user_types,'\n\n')

    # Display counts of gender
    print('Are more Subscribers male or female?\n')
    if 'Gender' in df:
        gender_count = df['Gender'].value_counts()
        print(gender_count,'\n\n')
    else:
        print('There is no gender information available for Washington.\n\n')
     
    # Display earliest, most recent, and most common years of birth
    print('Let\'s take a look at when our Subscribers were born!\n')
    if 'Birth Year' in df:
        oldest = df['Birth Year'].min()
        youngest = df['Birth Year'].max()
        common_age = df['Birth Year'].mode()[0]
        print('The oldest rider was born in {}!\n'.format(oldest))
        print('The youngest rider was born in {}!\n'.format(youngest))
        print('But the most common year for a rider to be born was {}!\n\n'.format(common_age))
    else:
        print('There is no birth year information for Washington.\n\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40,'\n\n')  


def show_raw(df):
    """ Receive user input as to whether they'd like to view raw data - 5 lines at a time!"""
    # Ask for only 'yes' or 'no' user input - account for incorrect entries
    i = 0
    see_raw = input('Would you like to see a few lines of the raw data? Please enter yes or no! : ').lower()
    while True:
        if see_raw not in ('yes', 'no'):
            see_raw = input('Please only enter yes or no!: ').lower()
            continue
        elif see_raw == 'no':
            break
        else:
            print(df[i:i+5], '\n\n')
            i += 5
            see_raw = input('Would you like to see more lines of the raw data? Please enter yes or no!: ').lower()
    
    print('-'*40,'\n\n')  
    
def main():
    """ Run all defined functions and restart if user chooses to do so!"""

    while True:
        # Filter and load the data frame
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # Run all desired functions/statistics and provide raw data
        user_stats(df)
        station_stats(df)
        time_stats(df)
        trip_duration_stats(df)
        show_raw(df)

        # Decision to start over or end
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()