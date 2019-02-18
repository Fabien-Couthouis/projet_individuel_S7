from abc import ABC, abstractmethod


class ContentExtraction(ABC):

    @abstractmethod
    def get_title(self):
        raise NotImplementedError('subclasses must override get_title()!')

    @abstractmethod
    def get_publication_date(self):
        raise NotImplementedError(
            'subclasses must override get_publication_date()!')

    @abstractmethod
    def get_author_name(self):
        raise NotImplementedError(
            'subclasses must override get_author_name()!')

    @abstractmethod
    def get_content(self):
        raise NotImplementedError('subclasses must override get_content()!')

    def log_error(self, e):
        print(e)
