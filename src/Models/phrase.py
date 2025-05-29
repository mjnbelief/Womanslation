import pymongo
import datetime
from typing import List, Optional
from bson import ObjectId
from datalayer import Base, ResponseModel, SortEnum, my_logger, get_db
from .meaning import Meaning


class Phrase(Base):
    """
    Phrase class to represent a phrase with its suggested response, meanings, and tags.

    schema:
    - text: str - The phrase to be analyzed.
    - suggested_response: str - The suggested response to the phrase.
    - meanings: List[Meaning] - The meanings of the phrase.
    - tags: List[str] - The tags associated with the phrase.
    - views: int - The number of views for the phrase.
    """

    text: str
    suggested_response: Optional[str]
    meanings: Optional[List[Meaning]] = []
    tags: Optional[List[str]] = []
    views: Optional[int] = 0

    def __init__(self, **data):
        super().__init__(**data)
        self.tags = [tag.strip().lower() for tag in self.tags]

    def validate(self) -> ResponseModel:
        # Check if the phrase is a string and at least 3 characters long
        if not isinstance(self.text, str) or len(self.text) < 3:
            return ResponseModel(success=False, message="Phrase must be a string and at least 3 characters long")

        return ResponseModel(success=True, message="Phrase validated successfully")

    @staticmethod
    def Phrase_viewed(phrase_id: str) -> ResponseModel:
        """
        Increment the view count of the phrase.
        """
        try:
            db = get_db()
            data_from_db = db["phrases"].find_one_and_update({"_id": ObjectId(phrase_id)}, {
                                                             "$inc": {"views": 1}}, return_document=pymongo.ReturnDocument.AFTER)

            return ResponseModel(success=True, message="Phrase viewed successfully", data=Phrase.convert_mongo_to_phrase(data_from_db))

        except Exception as e:
            my_logger.error(f"Error viewing phrase {phrase_id}: {e}")
            return ResponseModel(success=False, message=str(e))

    @staticmethod
    def get_phrase_by_id(phrase_id: str) -> ResponseModel:
        """
        Retrieve a phrase by ID from the database.
        """
        try:
            db = get_db()
            data_from_db = db["phrases"].find_one({"_id": ObjectId(phrase_id)})

            # Check if the phrase exists in the database
            if not data_from_db:
                return ResponseModel(success=False, message="Phrase not found!")

            return ResponseModel(success=True, data=Phrase.convert_mongo_to_phrase(data_from_db))

        except Exception as e:
            my_logger.error(f"Error retrieving phrase {phrase_id}: {e}")
            return ResponseModel(success=False, message=str(e))

    @staticmethod
    def get_phrase_by_text(text: str) -> ResponseModel:
        """
        Retrieve a phrase by text from the database.
        """
        try:
            db = get_db()
            data_from_db = db["phrases"].find_one({"text": text})

            # Check if the phrase exists in the database
            if not data_from_db:
                return ResponseModel(success=False, message="Phrase not found!")

            return ResponseModel(success=True, data=Phrase.convert_mongo_to_phrase(data_from_db))

        except Exception as e:
            my_logger.error(f"Error retrieving phrase by text '{text}': {e}")
            return ResponseModel(success=False, message=str(e))

    @staticmethod
    def create(self) -> ResponseModel:
        """
        Save the phrase to the database.
        """
        validation_response = self.validate()
        if not validation_response.success:
            return validation_response

        # Check if the phrase already exists in the database
        existing_phrase = Phrase.get_phrase_by_text(self.text)

        if existing_phrase.success:
            return ResponseModel(success=False, message="Phrase already exists in the database")

        try:
            """
            to save the meanings, we need first to save the phrase
            and then use the phrase ID to save the meanings.
            """
            meanings = self.meanings

            self.meanings = []  # Clear meanings to avoid saving them with the phrase
            self.create_date = datetime.datetime.now()

            db = get_db()
            result = db["phrases"].insert_one(self.dict(exclude={"id"}))

            self.id = str(result.inserted_id)

            if meanings:
                meanings_result = Meaning.create_meanings(meanings, self.id)
                phrase_with_meanings = Phrase.get_phrase_by_id(self.id)
                return ResponseModel(success=True, message=f"Phrase saved successfully. {meanings_result.message}", data=phrase_with_meanings.data)

            return ResponseModel(success=True, message="Phrase saved successfully", data=self)

        except Exception as e:
            my_logger.error(f"Error saving phrase '{self.text}': {e}")
            return ResponseModel(success=False, message=str(e))

    @staticmethod
    def update(self, phrase_id: str) -> ResponseModel:
        """
        Update the phrase in the database.
        """
        validation_response = self.validate()
        if not validation_response.success:
            return validation_response

        try:
            db = get_db()
            data_from_db = db["phrases"].find_one_and_update(
                {"_id": ObjectId(phrase_id)},
                {"$set": self.dict(exclude={"id", "create_date", "views", "meanings"})}, # Exclude fields that should not be updated
                return_document=pymongo.ReturnDocument.AFTER)
            
            return ResponseModel(success=True, message="Phrase updated successfully", data=Phrase.convert_mongo_to_phrase(data_from_db))

        except Exception as e:
            my_logger.error(f"Error updating phrase {phrase_id}: {e}")
            return ResponseModel(success=False, message=str(e))

    @staticmethod
    def delete(phrase_id: str) -> ResponseModel:
        """
        Delete the phrase from the database.
        """
        try:
            db = get_db()
            db["phrases"].delete_one({"_id": ObjectId(phrase_id)})
            return ResponseModel(success=True, message="Phrase deleted successfully")

        except Exception as e:
            my_logger.error(f"Error deleting phrase {phrase_id}: {e}")
            return ResponseModel(success=False, message=str(e))

    @staticmethod
    def get_phrases(pageIndex: int = 0, pageSize: int = 10, pageOrder: SortEnum = SortEnum.newest, searchText: str = "", tags: str = "") -> ResponseModel:
        """
        Retrieve all phrases from the database.
        """
        try:
            # Create a query based on the search text and tags
            query = {}
            
            if searchText:
                query["text"] = {
                    "$regex": searchText.strip().lower(), "$options": "i"}
                
            if tags:
                query["tags"] = {"$in": [tag.strip().lower() for tag in tags.split(",")]}

            order_by = ("create_date", pymongo.DESCENDING)
            match pageOrder:
                case SortEnum.A_Z:
                    order_by = ("text", pymongo.ASCENDING)
                case SortEnum.Z_A:
                    order_by = ("text", pymongo.DESCENDING)
                case SortEnum.oldest:
                    order_by = ("create_date", pymongo.ASCENDING)
                case SortEnum.newest:
                    order_by = ("create_date", pymongo.DESCENDING)
                case SortEnum.most_viewed:
                    order_by = ("views", pymongo.DESCENDING)

            db = get_db()
            data_from_db = db["phrases"].find(query).sort(order_by[0], order_by[1]).skip(pageIndex * pageSize).limit(pageSize)

            phrases: list[Phrase] = [Phrase.convert_mongo_to_phrase(phrase) for phrase in data_from_db]

            return ResponseModel(success=True, data=phrases)

        except Exception as e:
            my_logger.error(f"Error retrieving phrases: {e}")
            return ResponseModel(success=False, message=str(e))

    @staticmethod
    def search_phrases_by_tag(tag: str) -> ResponseModel:
        """
        Search for phrases by tag in the database.
        """
        try:
            db = get_db()
            data_from_db = db["phrases"].find({"tags": tag})

            phrases = [Phrase.convert_mongo_to_phrase(
                phrase) for phrase in data_from_db]
            return ResponseModel(success=True, data=phrases)

        except Exception as e:
            my_logger.error(f"Error searching phrases by tag '{tag}': {e}")
            return ResponseModel(success=False, message=str(e))

    @staticmethod
    def search_phrases(text: str) -> ResponseModel:
        """
        Search for phrases by text in the database.
        """
        try:
            db = get_db()
            data_from_db = db["phrases"].find(
                {"text": {"$regex": text, "$options": "i"}})

            phrases = [Phrase.convert_mongo_to_phrase(
                phrase) for phrase in data_from_db]
            return ResponseModel(success=True, data=phrases)

        except Exception as e:
            my_logger.error(f"Error searching phrases by text '{text}': {e}")
            return ResponseModel(success=False, message=str(e))

    @classmethod
    def convert_mongo_to_phrase(self, data: dict):
        """
            Convert MongoDB doc to Pydantic model
            Args:
                data (dict): The MongoDB document to convert.
            Returns:
                Phrase: The converted Pydantic model.
        """

        data = data.copy()
        data["id"] = str(data.pop("_id"))
        return self(**data)
