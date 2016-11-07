Synopsis: 

python __main__.py -s startDate -f outputFile [options]

Description:

This program fetches all the answers submitted in stackoverflow.com within
a date range from the stackoverflow API
and computes the following statistic data from them.

1. Total number of accepted answers.
2. Average score for all the accepted answers.
3. Average answer count per question.
4. For the top 10 answers, ordered by score descending, the comment count for every answer.

If a request for data fails, the program terminates with exit code -1.

The computed statistic data are exported in 2 tables in an HTML file.

  -s (required),
  Start date of the search in the supported formats.

  -f (required),
  Name of the file that will be created 

  --end (optional),
  End date of the search in the supported formats.
  If no end date is provided, the current date is used.

Supported Date Formats:
  "dd.MM.yyyy”,
  "dd.MM.yyyy HH:mm:ss"

Example of usage:

python __main__.py -s "01.07.2016" -f "./data.html" --end "10.07.2016"

Author:
  Written by Stefanos Georgakis
