# CTA L Analysis App

## Project Overview

The CTA L Analysis App is a Python-based console application that interacts with a SQLite database to analyze and visualize ridership data from the Chicago Transit Authority's L system. The application features a command-loop interface, allowing users to execute complex SQL queries, retrieve station and ridership data, and generate visual plots for in-depth data comparison.

The program is designed to handle large datasets efficiently, leveraging Python's data manipulation capabilities alongside SQL for robust data retrieval and aggregation. Matplotlib is integrated for dynamic data visualization, providing users with insights into public transportation trends over time.

## Files Included

- **main.py**: The main entry point of the application, containing the command-loop and user interaction logic.
- **datatier.py**: Handles direct interactions with the SQLite database, including SQL queries and data retrieval.
- **objecttier.py**: Contains the business logic, transforming raw data into structured objects that represent CTA L stations, ridership data, and more.
- **Makefile**: A simple Makefile to run the application or clean up the directory.
- **CTA2_L_daily_ridership.db**: The SQLite database containing the CTA L ridership data.
- **README.md**: This file, providing an overview of the project, instructions, and a description of included files.

## Instructions for Running the Application

1. Ensure Python is installed on your system.
2. Navigate to the project directory.
3. Run the application using the Makefile:
  ```bash
  make all
  ```

## Core Functionalities

The CTA L Analysis App supports the following commands:

1. **Command 1**: Displays stations that are 'like' the user's input using SQL wildcards.
2. **Command 2**: Displays the ridership at each station, ordered by station name, and calculates the percentage of total ridership.
3. **Command 3**: Outputs the top-10 busiest stations in terms of ridership, ordered by total ridership.
4. **Command 4**: Outputs the least-10 busiest stations in terms of ridership, ordered by total ridership.
5. **Command 5**: Displays all stop names associated with a user-specified line color, ordered by stop name.
6. **Command 6**: Displays total ridership by month, ordered by month, with an option to plot the data.
7. **Command 7**: Displays total ridership by year, ordered by year, with an option to plot the data.
8. **Command 8**: Compares daily ridership between two stations for a specified year, with an option to plot the comparison.
9. **Command 9**: Displays all unique station names for a specified line color, along with their coordinates, with an option to plot the locations on a map.

## Technical Details

- **SQL Integration**: The application uses complex SQL queries for data retrieval, aggregation, and filtering from the SQLite database.
- **Data Visualization**: Matplotlib is used for plotting ridership trends and station comparisons, enhancing the user's ability to explore the data visually.
- **Python Integration**: Python's data handling capabilities are employed to process and format the data, compute percentages, and interact with the SQLite database.
- **Command-loop Interface**: The application features a robust command-loop, allowing for real-time user interaction and data querying.
