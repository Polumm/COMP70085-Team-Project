from flask import Blueprint, jsonify, request
import aiohttp
import asyncio

# ==============================
# FETCH RANDOM WORDS FROM EXTERNAL API
# ==============================

# Base URL of the Random Word API
RANDOM_WORD_API_BASE_URL = "https://random-word-api.herokuapp.com"


# Function to fetch a single random word from the API
async def fetch_word(session, number, length, lang):
    """
    Fetch random words from the Random Word API.
    - Makes an HTTP GET request with specified parameters.

    Args:
        session: An aiohttp ClientSession.
        number: Number of requested words.
        length: Length of requested words.
        lang: Language of requested words.

    Returns:
        A list of random words.
    """
    params = {"number": number}
    if length:
        params["length"] = length
    if lang:
        params["lang"] = lang

    async with session.get(
        f"{RANDOM_WORD_API_BASE_URL}/word", params=params
    ) as response:
        return await response.json()


# API endpoint for fetching random words
def get_random_words():
    """
    Fetch a specified number of random words from the Random Word API.
    - Makes concurrent requests to fetch the specified number of unique words.

    Query Parameters:
        number (int, optional): Number of words to fetch.
        length (int, optional): Length of the requested words.
        lang (str, optional): Language code of the requested words.

    Returns:
        JSON list of random words.
    """
    number = request.args.get("number", default=1, type=int)
    length = request.args.get("length", default=None, type=int)
    lang = request.args.get("lang", default=None, type=str)

    if number <= 0:
        return jsonify(
            {"error": "The number of words must be greater than 0"}
        ), 400

    try:
        # Use asyncio to fetch random words concurrently
        async def fetch_words():
            async with aiohttp.ClientSession() as session:
                return await fetch_word(session, number, length, lang)

        words = asyncio.run(fetch_words())
        return jsonify(words), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
