from database import get_db
from phrase import Phrase

data = [
    {
        "text": "Would you still love me if I changed?",
        "create_date": "2023-11-12T00:00:00Z",
        "suggested_response": "My love isn't conditional on change; I accept you as you are.",
        "tags": [
            "testing",
            "reassurance",
            "love"
        ],
        "views": 150,
        "meanings": [
            {
                "meaning": "She wants to be sure your love is unconditional.",
                "tone": "Insecure",
                "confidence": 94,
                "warning_level": 4
            },
            {
                "meaning": "She's testing your loyalty and acceptance.",
                "tone": "Hurt / Indirect",
                "confidence": 90,
                "warning_level": 4
            }
        ]
    },
    {
        "text": "What would you do if I didn't answer your messages for a day?",
        "create_date": "2023-11-13T00:00:00Z",
        "suggested_response": "I'd worry and miss you a lot.",
        "tags": [
            "testing",
            "insecurity",
            "communication"
        ],
        "views": 135,
        "meanings": [
            {
                "meaning": "She wants to see how much you care and how much she matters to you.",
                "tone": "Insecure",
                "confidence": 91,
                "warning_level": 3
            },
            {
                "meaning": "She's measuring her fear of distance or neglect.",
                "tone": "Insecure",
                "confidence": 87,
                "warning_level": 4
            }
        ]
    },
    {
        "text": "Do I look fat in this?",
        "create_date": "2023-11-15T00:00:00Z",
        "suggested_response": "You always look amazing to me!",
        "tags": [
            "silly-question",
            "playful-test",
            "relationship"
        ],
        "views": 160,
        "meanings": [
            {
                "meaning": "She's fishing for a compliment and reassurance.",
                "tone": "Insecure",
                "confidence": 95,
                "warning_level": 2
            },
            {
                "meaning": "The real question is about how much you care.",
                "tone": "Playful",
                "confidence": 90,
                "warning_level": 1
            }
        ]
    },
    {
        "text": "So… who's *she*?",
        "create_date": "2023-10-20T00:00:00Z",
        "suggested_response": "Just a random human, I promise. Not a threat. 100% NPC.",
        "tags": [
            "comedic",
            "jealousy",
            "investigation-mode"
        ],
        "views": 123,
        "meanings": [
            {
                "meaning": "I noticed that tiny 2-second look and I'll never forget it.",
                "tone": "Testing",
                "confidence": 95,
                "warning_level": 4
            },
            {
                "meaning": "I'm starting a full FBI-level analysis now.",
                "tone": "Playful",
                "confidence": 93,
                "warning_level": 3
            }
        ]
    },
    {
        "text": "I'm not hungry.",
        "create_date": "2023-10-16T00:00:00Z",
        "suggested_response": "Noted. I'll still get fries... which you'll end up eating.",
        "tags": [
            "comedic",
            "denial",
            "food-related"
        ],
        "views": 445,
        "meanings": [
            {
                "meaning": "I'll eat half of whatever you order.",
                "tone": "Playful",
                "confidence": 90,
                "warning_level": 2
            },
            {
                "meaning": "I want you to insist and guess what I actually want.",
                "tone": "Playful",
                "confidence": 82,
                "warning_level": 1
            }
        ]
    },
    {
        "text": "We need to talk.",
        "create_date": "2023-10-14T00:00:00Z",
        "suggested_response": "Can I at least say goodbye to my happiness first?",
        "tags": [
            "comedic",
            "ominous",
            "emotional-warning"
        ],
        "views": 178,
        "meanings": [
            {
                "meaning": "Something you did has been festering in my soul for weeks.",
                "tone": "Angry / Confrontational",
                "confidence": 98,
                "warning_level": 5
            },
            {
                "meaning": "I'm mentally rehearsing a TED Talk on your mistakes.",
                "tone": "Angry / Confrontational",
                "confidence": 91,
                "warning_level": 5
            }
        ]
    },
    {
        "text": "Go have fun without me.",
        "create_date": "2023-10-13T00:00:00Z",
        "suggested_response": "That was a threat, wasn't it?",
        "tags": [
            "comedic",
            "guilt-tripping",
            "reverse-psychology"
        ],
        "views": 141,
        "meanings": [
            {
                "meaning": "You better *not* have fun without me or you're sleeping on the couch.",
                "tone": "Passive-aggressive",
                "confidence": 96,
                "warning_level": 4
            },
            {
                "meaning": "I'm secretly hoping you cancel your plans.",
                "tone": "Affectionate / Sweet",
                "confidence": 84,
                "warning_level": 3
            }
        ]
    },
    {
        "text": "I'm almost ready.",
        "create_date": "2023-10-12T00:00:00Z",
        "suggested_response": "Should I use this time to learn piano or get a PhD?",
        "tags": [
            "comedic",
            "time-warp",
            "female-logic"
        ],
        "views": 429,
        "meanings": [
            {
                "meaning": "I haven't even picked an outfit yet.",
                "tone": "Playful",
                "confidence": 92,
                "warning_level": 3
            },
            {
                "meaning": "We are 40 minutes away from leaving.",
                "tone": "Playful",
                "confidence": 88,
                "warning_level": 2
            }
        ]
    },
    {
        "text": "Do you think she's pretty?",
        "create_date": "2023-10-11T00:00:00Z",
        "suggested_response": "This feels like a trap and I respectfully decline.",
        "tags": [
            "comedic",
            "trap",
            "relationship-test"
        ],
        "views": 749,
        "meanings": [
            {
                "meaning": "Say no immediately. Don't blink. Don't breathe.",
                "tone": "Angry / Confrontational",
                "confidence": 99,
                "warning_level": 5
            },
            {
                "meaning": "I want to know if I'm prettier (but I'll pretend I don't care).",
                "tone": "Insecure",
                "confidence": 87,
                "warning_level": 4
            }
        ]
    },
    {
        "text": "I'm not mad.",
        "create_date": "2023-10-10T00:00:00Z",
        "suggested_response": "Okay, but should I sleep with one eye open tonight?",
        "tags": [
            "comedic",
            "denial",
            "sarcastic"
        ],
        "views": 114,
        "meanings": [
            {
                "meaning": "I am 1000% mad, but I'm letting you guess why.",
                "tone": "Angry / Confrontational",
                "confidence": 95,
                "warning_level": 4
            },
            {
                "meaning": "I'm planning your emotional punishment in silence.",
                "tone": "Manipulative",
                "confidence": 91,
                "warning_level": 5
            }
        ]
    },
    {
        "text": "Do you even care?",
        "create_date": "2023-10-09T00:00:00Z",
        "suggested_response": "Of course I do. I didn't realize you felt that way.",
        "tags": [
            "emotional",
            "insecure"
        ],
        "views": 62,
        "meanings": [
            {
                "meaning": "I feel ignored and need reassurance.",
                "tone": "Insecure",
                "confidence": 89,
                "warning_level": 2
            },
            {
                "meaning": "You haven't shown that I matter lately.",
                "tone": "Hurt / Indirect",
                "confidence": 82,
                "warning_level": 2
            }
        ]
    },
    {
        "text": "Go ahead.",
        "create_date": "2023-10-08T00:00:00Z",
        "suggested_response": "Only if you're sure. I don't want to make things worse.",
        "tags": [
            "sarcastic",
            "emotional"
        ],
        "views": 58,
        "meanings": [
            {
                "meaning": "I dare you to do the thing I don't want you to do.",
                "tone": "Passive-aggressive",
                "confidence": 90,
                "warning_level": 4
            },
            {
                "meaning": "I'm hoping you say no.",
                "tone": "Insecure",
                "confidence": 84,
                "warning_level": 3
            }
        ]
    },
    {
        "text": "Nothing's wrong.",
        "create_date": "2023-10-07T00:00:00Z",
        "suggested_response": "If I say nothing is wrong, should I run?",
        "tags": [
            "denial",
            "sarcasm"
        ],
        "views": 90,
        "meanings": [
            {
                "meaning": "I'm upset but don't want to talk about it.",
                "tone": "Hurt / Indirect",
                "confidence": 94,
                "warning_level": 4
            },
            {
                "meaning": "I'm testing if you can read between the lines.",
                "tone": "Testing",
                "confidence": 91,
                "warning_level": 4
            }
        ]
    },
    {
        "text": "You never listen to me.",
        "create_date": "2023-10-06T00:00:00Z",
        "suggested_response": "I'm sorry, I'll try harder.",
        "tags": [
            "frustration",
            "complaint"
        ],
        "views": 77,
        "meanings": [
            {
                "meaning": "I'm feeling ignored and frustrated.",
                "tone": "Disappointed",
                "confidence": 90,
                "warning_level": 3
            },
            {
                "meaning": "I want you to acknowledge my feelings.",
                "tone": "Passive-aggressive",
                "confidence": 88,
                "warning_level": 3
            }
        ]
    },
    {
        "text": "I don't care anymore.",
        "create_date": "2023-10-05T00:00:00Z",
        "suggested_response": "That hurts to hear.",
        "tags": [
            "hurt",
            "giving-up"
        ],
        "views": 55,
        "meanings": [
            {
                "meaning": "I'm deeply hurt and withdrawing.",
                "tone": "Hurt / Indirect",
                "confidence": 92,
                "warning_level": 4
            },
            {
                "meaning": "I'm testing if you still want to try.",
                "tone": "Testing",
                "confidence": 85,
                "warning_level": 3
            }
        ]
    },
    {
        "text": "I love you.",
        "create_date": "2023-10-04T00:00:00Z",
        "suggested_response": "I love you too, always.",
        "tags": [
            "love",
            "affection"
        ],
        "views": 1000,
        "meanings": [
            {
                "meaning": "I am expressing genuine affection.",
                "tone": "Affectionate / Sweet",
                "confidence": 99,
                "warning_level": 1
            }
        ]
    },
    {
        "text": "You're impossible.",
        "create_date": "2023-10-03T00:00:00Z",
        "suggested_response": "You love me anyway.",
        "tags": [
            "frustration",
            "playful"
        ],
        "views": 400,
        "meanings": [
            {
                "meaning": "I'm frustrated but still affectionate.",
                "tone": "Playful",
                "confidence": 85,
                "warning_level": 2
            }
        ]
    }
]



def insert_data_from_json():
    """
    Insert data from a JSON file into the specified MongoDB collection.
    """
    try:
        db = get_db()
        
        collections = db.list_collection_names()

        # Check if a collection exists
        if "phrases" not in collections:
            for item in data:
                # Convert each item to a Phrase object
                if isinstance(item, dict):
                    item = Phrase(**item)
                elif isinstance(item, list):
                    item = [Phrase(**i) for i in item]

                Phrase.create(item)

    except Exception as e:
        print(f"An error occurred while inserting data: {e}")
        raise e
