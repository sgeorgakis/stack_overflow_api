import requests
import sys


answers_url = (
    'https://api.stackexchange.com/2.2/answers?fromdate={0}'
    '&todate={1}'
    '&site=stackoverflow'
    )

comments_url = (
    'https://api.stackexchange.com/2.2/answers/{0}'
    '/comments?site=stackoverflow'
    '&order=desc&sort=creation'
    )


class ServiceManager:

    def __init__(self, from_date, to_date):
        """
        (str, str) -> ServiceManager
        Constructor of the class.
        Takes as arguments the search dates for the query.
        """
        self.__from_date = from_date
        self.__to_date = to_date
        self.__answers_submit_url = (answers_url.format(
            self.__from_date,
            self.__to_date
            ))

    def __make_request(self, url):
        """
        (str) -> dict
        Makes an http request in the specified url
        and returns the response decoded in json format
        """
        response = requests.get(url).json()
        try:
            if (response["error_id"]):
                raise Exception("{0}: {1}".format(
                    response["error_name"],
                    response["error_message"])
                                )
            return response
        except Exception as e:
                print("Error while requesting data from server")
                print("{0}: {1}".format(response["error_name"],
                                        response["error_message"]))
                sys.exit(-1)

    def get_answers(self):
        """
        (None) -> dict
        Returns the answers from the execution of the query
        to the StackOverflow API in json format
        """
        return self.__make_request(self.__answers_submit_url)

    def get_comments(self, answer_id):
        """
        (int) -> dict
        Returns the comments for an answer from the execution of the query
        to the StackOverflow API in json format
        We make the assumption that we want all the comments for this answer,
        overlooking the posting date
        """
        url = comments_url.format(answer_id)
        return self.__make_request(url)


if __name__ == "__main__":

    service_manager = ServiceManager("02.07.2016", "06.07.2016 10.40.00")
    print(service_manager.get_answers())
