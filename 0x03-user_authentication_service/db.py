#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """
    DB class
    """
    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        adds a user to the database
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs):
        """
        Returns the first user found based on the provided keyword arguments.
        Raises NoResultFound if no user is found.
        Raises InvalidRequestError for invalid query arguments.
        """
        try:
            # Dynamically filter by the keyword arguments
            print(f"Searching for user with filters: {kwargs}")
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            # No user found with the provided arguments
            print(f"No user found with : {kwargs}")
            raise NoResultFound(f"No user found with  arguments: {kwargs}")
        except InvalidRequestError:
            # Raised for incorrect query parameters
            print(f"Invalid query arguments: {kwargs}")
            raise InvalidRequestError(f"Invalid query arguments: {kwargs}")
