import datetime
from typing import Optional
from base import Base, ResponseModel
from database import get_db

class User_Vote(Base):
    
    meaning_id: str
    ip: str
    vote: bool #True -> like | False -> unlike
    
    def validation(self) -> ResponseModel:
        """
        Validate the meaning object.
            Check if the meaning is a string and at least 3 characters long.
            Check if the confidence level is an integer between 0 and 100.
            Check if the warning level is an integer between 0 and 10.
        """
        if not isinstance(self.meaning_id, str) or self.check_if_meaning_id_exists() == False:
            return ResponseModel(success=False, message="the meaning_id does not exist!")

        if not isinstance(self.ip, str) or len(self.ip) < 7:
            return ResponseModel(success=False, message="IP must be a string and at least 7 characters long!")
        
        if not isinstance(self.vote, bool):
            return ResponseModel(success=False, message="Vote must be a boolean value (True or False)!")
        
    def check_duplicate_possibility(self) -> Optional[str]:
        """
        Check if the user-ip with same meaning-id already exists.
        If it exists, return a response (TRUE) indicating a duplicate.
        """
        db = get_db()
        data_from_db = db["user_votes"].find_one(
            {"meaning_id": self.meaning_id, "ip": self.ip})

        # Check if the vote already exists in the database
        return data_from_db["_id"] if data_from_db else None


    def check_if_meaning_id_exists(self) -> bool:
        """
        Check if the meaning_id already exists in the database.
        """
        
        db = get_db()
        data_from_db = db["meanings"].find_one({"_id": self.meaning_id})

        # Check if the meaning_id already exists in the database
        return bool(data_from_db)
    
    
    def get_votes_by_meaning_id(self, meaning_id: str) -> ResponseModel:

        try:
            db = get_db()
            data_from_db = db["user_votes"].find({"meaning_id": meaning_id})

            # Check if the votes exist in the database
            if not data_from_db:
                return ResponseModel(success=False, message="Votes not found!")

            result = [User_Vote(**data) for data in data_from_db]
            return ResponseModel(success=True, data=result)

        except Exception as e:
            return ResponseModel(success=False, message=str(e))

    def create(self) -> ResponseModel:
        """
        Create a new vote in the database.
        """
        try:
            validation_response = self.validation()
            if not validation_response.success:
                return validation_response

            # if User already voted, update the vote
            if self.check_duplicate_possibility():
                self._id = self.check_duplicate_possibility()
                self.update(self)
                return ResponseModel(success=True, message="Vote Updated successfully", data=self)
            
            self.create_date = datetime.datetime.now()
            
            db = get_db()
            result = db["user_votes"].insert_one(self)
            
            self.id = result.inserted_id

            return ResponseModel(success=True, message="Vote created successfully", data=self)

        except Exception as e:
            return ResponseModel(success=False, message=str(e))
    
    def update(self) -> ResponseModel:
        """
        Update the vote in the database.
        """
        try:
            validation_response = self.validation()
            if not validation_response.success:
                return validation_response

            db = get_db()
            db["user_votes"].update_one({"id": self.id}, {"$set": self})
            
            return ResponseModel(success=True, message="Vote updated successfully")

        except Exception as e:
            return ResponseModel(success=False, message=str(e))
    
    def delete(vote_id: str) -> ResponseModel:
        """
        Delete the vote from the database.
        """
        try:
            db = get_db()
            db["user_votes"].delete_one({"_id": vote_id})

            return ResponseModel(success=True, message="Vote deleted successfully")

        except Exception as e:
            return ResponseModel(success=False, message=str(e))
        
    def delete_by_meaning_id(meaning_id: str) -> ResponseModel:
        """
        Delete the vote from the database by meaning_id.
        """
        try:
            db = get_db()
            db["user_votes"].delete_many({"meaning_id": meaning_id})

            return ResponseModel(success=True, message="Vote(s) deleted successfully")

        except Exception as e:
            return ResponseModel(success=False, message=str(e))