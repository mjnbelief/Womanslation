from src.base import Base, ResponseModel, ToneEnum
from src.database import get_db

class Meaning(Base):
    """
    Meaning class to represent the meaning of a phrase.

    schema:
    - phrase_id: str - ID of the phrase this meaning belongs to.
    - meaning: str - The meaning of the phrase.
    - tone: ToneEnum - The tone of the phrase.
    - confidence: int - Confidence level from 0 to 100.
    - warning_level: int - Warning level from 0 to 10.
    """
    phrase_id: str  # ID of the phrase this meaning belongs to
    meaning: str
    meaning_over_tone: ToneEnum
    confidence: int  # Confidence level from 0 to 100
    warning_level: int  # Warning level from 0 to 10

    def validation(self) -> ResponseModel:
        """
        Validate the meaning object.
            Check if the meaning is a string and at least 3 characters long.
            Check if the confidence level is an integer between 0 and 100.
            Check if the warning level is an integer between 0 and 10.
        """

        if not isinstance(self.meaning, str) or len(self.meaning) < 3:
            return ResponseModel(success=False, message="Meaning must be a string and at least 3 characters long")

        if not isinstance(self.confidence, int) or self.confidence < 0 or self.confidence > 100:
            return ResponseModel(success=False, message="Confidence level must be an integer between 0 and 100")

        if not isinstance(self.warning_level, int) or self.warning_level < 0 or self.warning_level > 10:
            return ResponseModel(success=False, message="Warning level must be an integer between 0 and 10")

        return ResponseModel(success=True, message="Meaning validated successfully")

    def check_dublicate_possibility(self) -> bool:
        """
        Check if the meaning already exists in the database.
        Basisd on the phrase ID, meaning, and tone.
        If it exists, return a response (TRUE) indicating a duplicate.
        """
        
        db = get_db()
        data_from_db = db["meanings"].find_one(
            {"phrase_id": self.phrase_id, "meaning": self.meaning, "tone": self.meaning_over_tone})

        # Check if the meaning already exists in the database
        if data_from_db:
            return True  # Meaning already exists in the database

        return False  # No duplicate found

    def get_meanings_by_phrase_id(self, phrase_id: str) -> ResponseModel:
        """
        Retrieve meanings by phrase ID from the database.
        """
        try:
            db = get_db()
            data_from_db = db["meanings"].find({"phrase_id": phrase_id})

            # Check if the meanings exist in the database
            if not data_from_db:
                return ResponseModel(success=False, message="Meanings not found!")

            result = [Meaning(**data) for data in data_from_db]
            return ResponseModel(success=True, data=result)

        except Exception as e:
            return ResponseModel(success=False, message=str(e))

    def create(self) -> ResponseModel:
        """
        Save the meaning to the database.
        """
        validation_response = self.validation()
        if not validation_response.success:
            return validation_response

        # Check if the meaning already exists in the database
        existing_meaning = self.check_dublicate_possibility(self)

        if existing_meaning:
            return ResponseModel(success=False, message="Meaning already exists in the database")

        try:
            db = get_db()
            db["meanings"].insert_one(self)
            return ResponseModel(success=True, message="Meaning created successfully")

        except Exception as e:
            return ResponseModel(success=False, message=str(e))
    
    def update(self) -> ResponseModel:
        """
        Update the meaning in the database.
        """
        validation_response = self.validation()
        if not validation_response.success:
            return validation_response

        try:
            db = get_db()
            db["meanings"].update_one({"id": self.id}, {"$set": self})
            return ResponseModel(success=True, message="Meaning updated successfully")

        except Exception as e:
            return ResponseModel(success=False, message=str(e))
    
    def delete(self) -> ResponseModel:
        """
        Delete the meaning from the database.
        """
        try:
            db = get_db()
            db["meanings"].delete_one({"id": self.id})
            return ResponseModel(success=True, message="Meaning deleted successfully")

        except Exception as e:
            return ResponseModel(success=False, message=str(e))
    
    def delete_by_phrase_id(self, phrase_id: str) -> ResponseModel:
        """
        Delete meanings by phrase ID from the database.
        """
        try:
            db = get_db()
            db["meanings"].delete_many({"phrase_id": phrase_id})
            return ResponseModel(success=True, message="Meanings deleted successfully")

        except Exception as e:
            return ResponseModel(success=False, message=str(e))
