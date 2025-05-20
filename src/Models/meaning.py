from typing import Optional

from bson import ObjectId
from base import Base, ResponseModel, ToneEnum
from database import get_db


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
    tone: Optional[ToneEnum] = None
    confidence: Optional[int] = None  # Confidence level from 0 to 100
    warning_level: Optional[int] = None  # Warning level from 0 to 5

    def validation(self) -> ResponseModel:
        """
        Validate the meaning object.
            Check if the meaning is a string and at least 3 characters long.
            Check if the confidence level is an integer between 0 and 100.
            Check if the warning level is an integer between 0 and 5.
        """

        if not isinstance(self.meaning, str) or len(self.meaning) < 3:
            return ResponseModel(success=False, message="Meaning must be a string and at least 3 characters long")

        if not (isinstance(self.confidence, Optional[int]) and 0 <= self.confidence <= 100):
            return ResponseModel(success=False, message="Confidence level must be an integer between 0 and 100")

        if not isinstance(self.warning_level, Optional[int]) or self.warning_level < 0 or self.warning_level > 5:
            return ResponseModel(success=False, message="Warning level must be an integer between 0 and 5")

        if not isinstance(self.tone, Optional[ToneEnum]):
            return ResponseModel(success=False, message="Tone must to select from Tone-list.")

        return ResponseModel(success=True, message="Meaning validated successfully")

    def check_duplicate_possibility(self) -> bool:
        """
        Check if the meaning already exists in the database.
        Based on the phrase ID, meaning, and tone.
        If it exists, return a response (TRUE) indicating a duplicate.
        """

        db = get_db()
        data_from_db = db["phrases"].find_one(
            {"_id": ObjectId(self.phrase_id), "meanings.meaning": self.meaning, "meanings.tone": self.tone})

        # Check if the meaning already exists in the database
        if data_from_db:
            return True  # Meaning already exists in the database

        return False  # No duplicate found
    
    @staticmethod
    def get_meanings_by_phrase_id(phrase_id: str) -> ResponseModel:
        """
        Retrieve meanings by phrase ID from the database.
        """
        try:
            db = get_db()
            data_from_db = db["phrases"].find_one({"_id": ObjectId(phrase_id)})

            # Check if the meanings exist in the database
            if not data_from_db["meanings"]:
                return ResponseModel(success=False, message="Meanings not found!")

            result = [Meaning.convert_mongo_to_meaning(meaning) for meaning in data_from_db["meanings"]]
            return ResponseModel(success=True, data=result)

        except Exception as e:
            return ResponseModel(success=False, message=str(e))

    @staticmethod
    def create(self) -> ResponseModel:
        """
        Save the meaning to the database.
        """
        validation_response = self.validation()
        if not validation_response.success:
            return validation_response

        # Check if the meaning already exists in the database
        existing_meaning = self.check_duplicate_possibility(self)

        if existing_meaning:
            return ResponseModel(success=False, message="Meaning already exists in the database")

        try:
            db = get_db()
            data_from_db = db["phrases"].update_one(
                {"_id": ObjectId(self.phrase_id)},
                {"$addToSet": {"meanings": self.dict(exclude={"id"})}}
            )
            self.id = data_from_db.inserted_id
            return ResponseModel(success=True, message="Meaning added successfully", data=self)

        except Exception as e:
            return ResponseModel(success=False, message=str(e))

    @staticmethod
    def update(self, meaning_id: str) -> ResponseModel:
        """
        Update the meaning in the database.
        """
        validation_response = self.validation()
        if not validation_response.success:
            return validation_response

        try:
            db = get_db()
            db["phrases"].update_one(
                {
                    "_id": ObjectId(self.phrase_id),
                    "meanings._id": ObjectId(meaning_id)
                },
                {"$set": {"meanings.$": self.dict(exclude={"id"})}}
            )
            return ResponseModel(success=True, message="Meaning updated successfully")

        except Exception as e:
            return ResponseModel(success=False, message=str(e))

    @staticmethod
    def delete(phrase_id: str, meaning_id: str) -> ResponseModel:
        """
        Delete the meaning from the database.
        """
        try:
            db = get_db()
            db["phrases"].update_one(
                {"_id": ObjectId(phrase_id)},
                {"$pull": {"meanings": {"_id": ObjectId(meaning_id)}}}
            )

            return ResponseModel(success=True, message="Meaning deleted successfully")

        except Exception as e:
            return ResponseModel(success=False, message=str(e))

    @staticmethod
    def delete_meanings_by_phrase_id(phrase_id: str) -> ResponseModel:
        """
        Delete all meanings for a specific phrase from the database.
        """
        try:
            db = get_db()
            db["phrases"].update_one(
                {"_id": ObjectId(phrase_id)},
                {"$set": {"meanings": []}}
            )

            return ResponseModel(success=True, message=f"All meanings for phrase {phrase_id} deleted successfully")

        except Exception as e:
            return ResponseModel(success=False, message=str(e))

    @classmethod
    def convert_mongo_to_meaning(self, data: dict):
        """
            Convert MongoDB doc to Pydantic model
            Args:
                data (dict): The MongoDB document to convert.
            Returns:
                Meaning: The converted Pydantic model.
        """

        data = data.copy()
        data["id"] = str(data.pop("_id"))
        return self(**data)
