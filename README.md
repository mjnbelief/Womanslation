# 🧠 Womanslation
**Womanslation** is a playful, educational backend project that helps decode hidden meanings behind commonly-used phrases in conversations — especially those that may be misunderstood between genders.

Built with **FastAPI** and **MongoDB**, this project is ideal for learning backend development, RESTful APIs, and working with NoSQL databases in a fun and creative way.

---

## 💡 Project Idea

Women (and humans in general!) sometimes say things that carry meanings beyond the literal words. This app stores those phrases, decodes possible interpretations, and suggests thoughtful, non-disastrous responses 😄

Example:
> 🗣️ Phrase: *"Do whatever you want."*  
> 🤯 Hidden meaning: *"If you actually do it, I’ll be furious."*  
> ✅ Suggested response: *"I’d rather decide together if you're okay with that."*

---

## 🔧 Tech Stack

- 🐍 **FastAPI** (Python web framework)
- 🍃 **MongoDB** (NoSQL database)
- 🔄 REST API endpoints for CRUD operations
- 📦 JSON-based data storage
- 📁 Optional frontend or mobile app support (future roadmap)

---

## 🚀 How to Run Locally

1. **Clone this repo**:
   ```bash
   git clone https://github.com/mjnbelief/Womanslation.git
   cd womanslation
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the project**:
   ```bash
   python main.py
   ```

4. **Visit the interactive API docs**:
   [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🗂 Sample Data Format

```json
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
                "tone": "other",
                "confidence": 82,
                "warning_level": 1
            }
        ]
    },
```

---


## 🧪 Future Ideas

- 🔐 User accounts:
    - Favorites
    - View visit history
- 🌍 Multi-language or multi-culture phrase packs.
- 💬 Commenting system.
- 🔁 Reverse Version:
    - What Phrases Do Men Say That Have a Special Meaning?
- 🕵️‍♀️ Admin review and permission

---

## 🧑‍💻 Created By

**Project Name**: Womanslation  
**Concept**: (Woman + Translation) Decode what she said vs what she meant  
**Author**: MJ Noori  
**Date**: 2025

---

> ⚠️ Disclaimer: This app is meant for entertainment, humor, and social insight — not to stereotype or generalize communication styles.
