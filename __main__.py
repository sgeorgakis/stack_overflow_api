import sys
import time
import datetime
from statistic_generator import *
from template_creator import *
import argparse


# Valid formats of dates
pattern = '%d.%m.%Y %H:%M:%S'
alternative_pattern = '%d.%m.%Y'


def format_date(date):
        """
        (str) -> str
        Returns the date in the accepted format for the query
        """
        try:
            epoch = int(time.mktime(time.strptime(date, pattern)))
        except ValueError:
            epoch = int(time.mktime(time.strptime(date, alternative_pattern)))
        return epoch


def print_comment_count(comment_dictionary):
        """
        (dict) -> None
        Prints the count of comments for the top 10 answers.
        """
        print("\n\n--Comment Count Per Answer (Top 10 Anwers)--")
        for answer_id in comment_dictionary:
                print("{0}:  {1}".format(answer_id,
                                         comment_dictionary[answer_id]))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=(
        'Find statistic data '
        'of answers in stack'
        'overflow in a specific date range')
                                     )
    parser.add_argument('-s', type=str,
                        help='start date of the search')
    parser.add_argument('--end', type=str,
                        help='end date of the search')
    parser.add_argument('-f', type=str,
                        help='file name to export data')

    args = parser.parse_args()
    start_date = format_date(args.start)
    if (args.end):
        end_date = format_date(args.end)
    else:
        end_date = format_date(datetime.datetime.utcnow().strftime(pattern))
    file = args.file

    try:
        statistic_generator = StatisticGenerator(start_date, end_date)
    except ValueError:
        print("\n\nYou did not enter the dates in the accepted formats.")
        print("Restart the program and enter values in the specified "
              "formats (\"dd.MM.yyyy HH.mm.ss\" or \"dd.MM.yyyy\"")
    else:
        accepted_answers = (statistic_generator
                            .compute_number_of_accepted_answers())
        average_score_of_accepted_answers = (
            statistic_generator.compute_average_score_of_accepted_answers()
            )
        average_answer_per_question = (statistic_generator
                                       .average_answer_count())
        print("\n\nTotal number of accepted answers: {0}"
              .format(accepted_answers))
        print("Average score for all the accepted answers: {0}"
              .format(average_score_of_accepted_answers))

        print("Average answer count per question: {0}"
              .format(average_answer_per_question))
        comment_count = statistic_generator.get_comment_count_per_answer()
        print_comment_count(comment_count)
        creator = TemplateCreator(file)
        creator.generate_html_file(
            [accepted_answers,
             average_score_of_accepted_answers,
             average_answer_per_question],
            comment_count)
