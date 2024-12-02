import aiohttp
from flask import jsonify, request

import asyncio


# ==============================
# FETCH RANDOM IMAGES FROM EXTERNAL API
# ==============================

LIKEPOEMS_IMAGE_API = "https://api.likepoems.com/img/bing/"


async def fetch_image(session):
    """
    Fetch a single image from the Likepoems API.
    - Makes an HTTP GET request to the API to retrieve a random image.

    Returns:
        A dictionary containing the URL of the fetched image.
    """
    async with session.get(LIKEPOEMS_IMAGE_API) as response:
        return {"url": str(response.url)}


async def fetch_unique_images_concurrently(num_images):
    """
    Fetch multiple unique images concurrently from the Likepoems API.
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
    Fetch a specified number of unique random images from the Likepoems API.
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
