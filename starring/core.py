"""Модуль, реализующий логику программы"""
import sys

try:
    import requests
except ImportError:
    sys.exit("Module 'request' not found")

__all__ = ["Worker"]


class Worker:
    """Класс обработчик"""

    def __init__(self, username: str):
        """Конструктор"""
        self._username = username

    @property
    def username(self):
        return self._username

    def receive_request(self, url: str):
        """Получение ответа от Git API"""
        try:
            request = requests.get(url)
            if request.headers.get("Status").startswith("404"):
                raise WorkerException("User not found.")
            if request.headers.get("Status").startswith("403"):
                raise WorkerException("API rate limit exceeded for current IP")
        except requests.RequestException:
            raise WorkerException("Cannot get a request.")
        return request

    def get_next_page_url(self, request: requests.models.Response):
        """Получение ссылки на следующую страницу со star репозиториями"""
        if len(request.links) == 0:
            return None
        link_to_next_page = request.links.get("next", None)
        if link_to_next_page is None:
            return None
        url_next_page = link_to_next_page.get("url")
        if url_next_page is None:
            return None
        return url_next_page

    def get_starring_rep(self):
        """Получить list из tuple(repName, countOfStar)"""
        print("Getting information...")
        result = []
        request_url = f"https://api.github.com/users/{self.username}/starred"
        while request_url is not None:
            try:
                response = self.receive_request(request_url)
                for rep_info in response.json():
                    rep_name = rep_info.get("name")
                    count_of_star = rep_info.get("stargazers_count")
                    result.append((rep_name, count_of_star))
                request_url = self.get_next_page_url(response)
            except WorkerException as exception:
                sys.exit(f"Cannot get a starring repository. Exception: {exception}")
        return result

    def print_info(self, result):
        """Вывод полученной информации на экран"""
        if len(result) == 0:
            print(f"User '{self.username}' does not have repositories being starred")
        else:
            print(f"User '{self.username}' have {len(result)} repository(ies) being starred")
            for rep in result:
                print(f" {rep[0]} : {rep[1]}")


class WorkerException(Exception):
    """Ошибка, возникающая внутри Worker"""
    pass
