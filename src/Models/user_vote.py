import datetime
from typing import Optional
from bson import ObjectId
from base import Base, ResponseModel, my_logger
from database import get_db

class User_Vote(Base):
    """
    User_Vote class to represent a user's vote on a meaning.

    schema:
        - phrase_id: str - ID of the phrase this vote belongs to (it's just for deleting).
        - meaning_id: str - ID of the meaning this vote belongs to.
        - ip: str - IP address of the user.
        - like: bool - True for like, False for unlike.
    """
    phrase_id: str # we need phrase_id just when we want to delete the vote by phrase_id
    meaning_id: str
    ip: Optional[str] = None
    like: bool = False
        
    def validation(self) -> ResponseModel:

        if not isinstance(self.ip, str) or len(self.ip) < 7:
            return ResponseModel(success=False, message="IP must be a string and at least 7 characters long!")
        
        if not isinstance(self.like, bool):
            return ResponseModel(success=False, message="Vote must be a boolean value (True or False)!")

        return ResponseModel(success=True, message="Vote validated successfully")

    def check_duplicate_possibility(self) -> Optional[str]:
        """
        Check if the user-ip with same meaning-id already exists.
        If it exists, return a response (TRUE) indicating a duplicate.
        """
        db = get_db()
        data_from_db = db["user_votes"].find_one(
            {"meaning_id": self.meaning_id, "ip": self.ip})

        # Check if the vote already exists in the database
        return str(data_from_db.pop("_id")) if data_from_db else None

    @staticmethod
    def get_by_ip(user_ip: str) -> ResponseModel:
        """
        Get all votes by user IP.
        """
        try:
            db = get_db()
            data_from_db = db["user_votes"].find({"ip": user_ip, "like": True})

            if not data_from_db:
                return ResponseModel(success=False, message="No votes found for this User")

            votes = [User_Vote.convert_mongo_to_user_vote(data) for data in data_from_db]
            return ResponseModel(success=True, message="Votes retrieved successfully", data=votes)

        except Exception as e:
            my_logger.error(f"Error retrieving votes by IP {user_ip}: {e}")
            return ResponseModel(success=False, message=str(e))
    
    @staticmethod
    def create(self) -> ResponseModel:
        """
        Create a new vote in the database.
        """
        try:
            validation_response = self.validation()
            if not validation_response.success:
                return validation_response

            # if User already voted, update the vote
            existing_id = self.check_duplicate_possibility()
            if existing_id:
                self.id = existing_id
                updated_vote_response = User_Vote.update(self)
                return updated_vote_response

            self.create_date = datetime.datetime.now()
            
            db = get_db()
            result = db["user_votes"].insert_one(self.dict(exclude={"id"}))
            
            self.id = str(result.inserted_id)

            return ResponseModel(success=True, message="Vote created successfully", data=self)

        except Exception as e:
            my_logger.error(f"Error creating vote: {e}")
            return ResponseModel(success=False, message=str(e))
    
    @staticmethod
    def update(self) -> ResponseModel:
        """
        Update the vote in the database.
        """
        try:
            validation_response = self.validation()
            if not validation_response.success:
                return validation_response

            self.create_date = datetime.datetime.now()
            
            db = get_db()
            data_from_db = db["user_votes"].find_one_and_update({"_id": ObjectId(self.id)}, {"$set": self.dict(exclude={"id"})})

            return ResponseModel(success=True, message="Vote updated successfully", data=User_Vote.convert_mongo_to_user_vote(data_from_db))

        except Exception as e:
            my_logger.error(f"Error updating vote: {e}")
            return ResponseModel(success=False, message=str(e))
    
    @staticmethod
    def delete(vote_id: str) -> ResponseModel:
        """
        Delete the vote from the database.
        """
        try:
            db = get_db()
            db["user_votes"].delete_one({"_id": ObjectId(vote_id)})

            return ResponseModel(success=True, message="Vote deleted successfully")

        except Exception as e:
            my_logger.error(f"Error deleting vote {vote_id}: {e}")
            return ResponseModel(success=False, message=str(e))
    
    @staticmethod    
    def delete_by_meaning_id(meaning_id: str) -> ResponseModel:
        """
        Delete the vote from the database by meaning_id.
        """
        try:
            db = get_db()
            db["user_votes"].delete_many({"meaning_id": meaning_id})

            return ResponseModel(success=True, message="Vote(s) deleted successfully")

        except Exception as e:
            my_logger.error(f"Error deleting vote by meaning_id {meaning_id}: {e}")
            return ResponseModel(success=False, message=str(e))
    
    @staticmethod
    def delete_by_phrase_id(phrase_id: str) -> ResponseModel:
        """
        Delete the vote from the database by phrase_id.
        """
        try:
            db = get_db()
            db["user_votes"].delete_many({"phrase_id": phrase_id})

            return ResponseModel(success=True, message="Vote(s) deleted successfully")

        except Exception as e:
            my_logger.error(f"Error deleting vote by phrase_id {phrase_id}: {e}")
            return ResponseModel(success=False, message=str(e))
        
    @classmethod
    def convert_mongo_to_user_vote(self, data: dict):
        """
            Convert MongoDB doc to Pydantic model
            Args:
                data (dict): The MongoDB document to convert.
            Returns:
                User_Vote: The converted Pydantic model.
        """

        data = data.copy()
        data["id"] = str(data.pop("_id"))
        return self(**data)
        