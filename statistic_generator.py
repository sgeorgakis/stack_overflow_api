from service_manager import *


class StatisticGenerator:

    def __init__(self, from_date, to_date):
        """
        (str, str) -> StatisticGenerator
        Constructor of the class.
        Takes as arguments the start date and end date of the search query
        """
        self.__from_date = from_date
        self.__to_date = to_date
        self.__service_manager = ServiceManager(self.__from_date,
                                                self.__to_date)
        self.__answers = self.__service_manager.get_answers()

    def compute_number_of_answers(self):
        """
        (None) -> int
        Returns the number of all answers
        that received from the StackOverflow API.
        Used for debugging reasons
        """
        return len(self.__answers["items"])

    def compute_number_of_accepted_answers(self):
        """
        (None) -> int
        Returns the number of the accepted answers
        that received from the StackOverflow API.
        """
        counter = 0
        for item in self.__answers["items"]:
            if item["is_accepted"]:
                counter += 1
        return counter

    def compute_average_score_of_accepted_answers(self):
        """
        (None) -> float
        Returns the average score of all the accepted answers
        that received from the StackOverflow API rounded in 2 decimal points.
        """
        score = 0.0
        counter = 0
        for item in self.__answers["items"]:
            if item["is_accepted"]:
                score += item["score"]
                counter += 1
        average_score = score / counter
        return round(average_score, 2)

    def average_answer_count(self):
        """
        (None) -> float
        Returns the average answers of all the questions
        that received from the StackOverflow API rounded in 2 decimal points.
        We make the assumption that in the same query result many answers
        for the same question may exist
        """
        answers = 0.0
        question_id_set = set()
        for item in self.__answers["items"]:
            if item["question_id"] not in question_id_set:
                question_id_set.add(item["question_id"])
            answers += 1
        average_answers_per_question = answers / len(question_id_set)
        return round(average_answers_per_question, 2)

    def __get_top_answers(self):
        """
        (None) -> list
        Returns the top 10 answers (answer_id)
        sorted by score descending.
        """
        score_per_answer = {}
        for item in self.__answers["items"]:
            score_per_answer[item["answer_id"]] = item["score"]
        return sorted(score_per_answer, reverse=True,
                      key=score_per_answer.get)[0:10]

    def get_comment_count_per_answer(self):
        """
        (None) -> dict
        Calculates the comments for the top 10 answers.
        Returns a dictionary with the answer ids as key
        and the number of comments as value
        """
        top_answers_id = self.__get_top_answers()
        comments_per_answer = {}
        for id in top_answers_id:
            comments = self.__service_manager.get_comments(id)
            # print(comments)
            comments_per_answer[id] = (len(comments["items"]))
            # print(str(id) + ": " + str(len(comments["items"])))
        return comments_per_answer

    def get_comment_count_per_single_answer(self):
        """
        (None) -> int
        Returns the comment count for the answer with id = 38145415
        Used for debugging
        """
        answer_id = "38145415"
        comments = self.__service_manager.get_comments(answer_id)
        print(comments)
        return len(comments["items"])


if __name__ == "__main__":
    statistic_generator = StatisticGenerator("01.07.2016", "05.07.2016")
    print(statistic_generator.get_comment_count_per_single_answer())
