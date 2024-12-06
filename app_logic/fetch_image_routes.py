import aiohttp
from flask import jsonify, request

import asyncio


# ==============================
# FETCH RANDOM IMAGES FROM EXTERNAL API
# ==============================

DUCK_API_BASE_URL = "https://random-d.uk/api"


async def fetch_image(session):
    """
    Fetch a single image from the Duck API.
    - Makes an HTTP GET request to the API to retrieve a random image.

    Returns:
        A dictionary containing the URL of the fetched image.
    """
    async with session.get(DUCK_API_BASE_URL + "/random") as response:
        data = await response.json()
        return {"url": data["url"]}


async def fetch_unique_images_concurrently(num_images):
    """
    Fetch multiple unique images concurrently from the Duck API.
    - Ensures the fetched image URLs are unique.

    Args:
        num_images (int): The number of unique images to fetch.

    Returns:
        A list of dictionaries containing unique image URLs.
    """
    unique_urls = set()
    images = []

    async with aiohttp.ClientSession() as session:
        while len(images) < num_images:
            # Calculate remaining images to fetch
            remaining = num_images - len(images)
            tasks = [fetch_image(session) for _ in range(remaining)]
            results = await asyncio.gather(*tasks)

            for image in results:
                if image["url"] not in unique_urls:
                    unique_urls.add(image["url"])
                    images.append(image)

    return images


# @api.route("/get_random_images", methods=["GET"])
def get_random_images():
    """
    Fetch a specified number of unique random images from the Duck API.
    - Makes concurrent requests to fetch the specified number of unique images.

    Query Parameters:
        count (int, optional): Number of unique images to fetch.

    Returns:
        JSON list of unique image URLs.
    """
    num_images = request.args.get("count", default=8, type=int)
    if num_images <= 0:
        return jsonify(
            {"error": "The number of images must be greater than 0"}
        ), 400

    try:
        # Use asyncio to fetch unique images concurrently
        images = asyncio.run(fetch_unique_images_concurrently(num_images))
        return jsonify(images), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
