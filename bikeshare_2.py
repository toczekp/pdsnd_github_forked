import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
WEEK_DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (int) month - integer representing the month to filter by, or -1 to apply no month filter
        (int) day - integer representing the week to filter by, or -1 to apply no day filter
    """
    
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = None
    while(True):
        city = input('Fill the name of the city of interest. Choose from: Chicago, Washington or New York City.\n').lower()
        if city in CITY_DATA.keys():
            break
        else:
            print('There is no data for the city name provided. Are you sure you spelled it correctly?')
        
    month = None
    # get user input for month (all, january, february, ... , june)
    while(True):
        month = input('Fill the name of the month of interest: \n').lower()
        if month == 'all' or month in MONTHS:
            break
        else:
            print('There is no data for the month provided. Are you sure you spelled it correctly?')
    

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = None
    while(True):
        day = input('Fill the name of the week day of interest: \n').lower()
        if day =='all' or day in WEEK_DAYS:
            break
        else:
            print('There is no data for the day provided. Are you sure you spelled it correctly?')
            
    if day != 'all':
        day_out = WEEK_DAYS.index(day)+1
    else:
        day_out = -1
        
    if month != 'all':
        month_out = MONTHS.index(month)+1
    else:
        month_out = -1
    
    

    print('-'*40)
    return city, month_out, day_out



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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Start Month'] = df['Start Time'].dt.month
    df['Start Day'] = df['Start Time'].dt.dayofweek
    df['Start Hour'] = df['Start Time'].dt.hour
    
    if month != -1:
        df = df[df['Start Month'] == month]
        
    if day != -1:
        df = df[df['Start Day'] == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most popular month/months are: \n')
    mcm = df['Start Month'].mode()
    for i, value in mcm.items():
        print('- ' + MONTHS[value - 1] + '\n')


    # display the most common day of week
    print('Most popular day of week is: \n')
    mcd = df['Start Day'].mode()
    for i, value in mcd.items():
        print('- ' + WEEK_DAYS[value - 1] + '\n')

    # display the most common start hour
    print('Most popular starting hour is/are: \n')
    mch = df['Start Hour'].mode()
    for i, value in mch.items():
        print('- ' + str(value))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most common start station/s is/are:')
    mcss = df['Start Station'].mode()
    for i, value in mcss.items():
        print('- {} \n'.format(str(value)))
    # display most commonly used end station
    print('The most common end station/s is/are:')
    mces = df['End Station'].mode()
    for i, value in mces.items():
        print('- {} \n'.format(str(value)))

    # display most frequent combination of start station and end station trip
    # thanks https://www.statology.org/pandas-count-unique-combinations-of-two-columns/

    station_combo_counts = df[['Start Station', 'End Station']].value_counts().reset_index(name='Count')
    value_count = int(station_combo_counts[['Count']].max())
    print('The most popular combination of start and end station/s is/are: \n')
    for index, row in station_combo_counts.iterrows():
        if row['Count'] == value_count:
            print('- \'{}\' and \'{}\' with number of trips: {} \n'.format(row['Start Station'], row['End Station'], str(row['Count'])))
        else:
            break
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tota_travel_time = df['Trip Duration'].sum() / 3600.0
    print('Total travel time for the specified city and time period is {:.2f} hours'.format(tota_travel_time))
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean() / 60.0
    print('Mean travel time for the specified city and time period is {:.2f} minutes'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    for i, value in df['User Type'].value_counts().items():
        print('\t {}: {}'.format(i, value))
        
    print('\nCalculating gender distribution: ')
    # Display counts of gender
    try:
        for i, value in df['Gender'].value_counts().items():
            print('\t {}: {}'.format(i, value))
    except KeyError:
        print('No gender data available')

    # Display earliest, most recent, and most common year of birth
    print('Calculating year of birth stats: ')
    try:
        most_common_yob = [value for i, value in df['Birth Year'].mode().items()]
        print('Year of birth stats: \n\tearliest: \t{},\n\tmost recent: \t{}, \n\tmost common: \t{}'.format(df['Birth Year'].min(), df['Birth Year'].max(), most_common_yob))
    except KeyError:
        print('No year of birth data available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def check_input(prompt, accepted_input):
    """
    Helper function to ease programming of while loops with user input. Asks the user for input with the provided prompt and validates it towards the accepted_input list.
    Args:
        (str) prompt - message to be displayed by input method.
        (list) accepted_input - list of accepted inputs to check the input towards.
        
    Returns:
        (str) user input validated towards the accepted_input list.
    """
    while True:
        user_input = input(prompt).lower()
        if user_input in accepted_input:
            break
        else:
            print('\nPlease make sure to spell the input correctly\n')
    return user_input

def main():
    stats = {'time': time_stats, 'stations':station_stats, 'trips':trip_duration_stats, 'users':user_stats}
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if not df.empty:
            task_input = check_input('\Would you like to browse the data or see some statistics?\nChoose between \'data\' and \'stats\'\n', ['data', 'stats'])
            if task_input == 'stats':
                while True:
                    stat_input = input('\n What kins of statistics would you like to see? Choose between \n\tTime \n\tStations \n\tTrips \n\tUsers.\nType \'end\' if you want to quit\n').lower()
                    if stat_input in stats.keys():
                        stats[stat_input](df)
                    elif stat_input=='end':
                        break
            elif task_input == 'data':
                start_index = 0
                while start_index < df.shape[0]:
                    print('Here comes 5 rows of data!\n')
                    print(df.iloc[start_index:start_index + 5])
                    start_index += 5
                    if start_index >= df.shape[0]:
                        break
                    data_input = check_input('Would you like to see more data? y/n \n', ['y', 'n'])
                    if data_input == 'n':
                        break
        else:
            print('\nIt seems that we lack data on that particular date and city combo. \n')
            
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes' and restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
