# Flip Game

## Backend Development
- Developed robust database models and API endpoints to support game logic and leaderboard functionality.  
- Integrated asynchronous image fetching using the Duck API to enhance game variety and scalability during high-volume requests.
- Managed database design with PostgreSQL and implemented user authentication using secure session management.
- Designed and maintained CI/CD pipelines tailored for seamless development, testing, and deployment across feature, develop, and main branches.

## Frontend Development
- Created an intuitive user interface with animations and responsive design for an engaging gaming experience.
- Implemented real-time interactions, game state visualization, and dynamic statistics tracking to ensure smooth gameplay.
- Enhanced user experience with dynamic UI components and streamlined interactions.

---

# Key Features

| **Feature**                              | **Description**                                                                                                                                                       |
|------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Web Application**                      | Built with Flask for the backend and HTML/CSS/JavaScript for the frontend, ensuring a smooth user experience.                                                         |
| **Simple and Engaging Gameplay**         | Offers easy-to-understand mechanics that improve memory skills while presenting a fun challenge.                                                                      |
| **Production Deployment**                | Hosted on a reliable Impaas platform for seamless access across devices.                                                                                              |
| **Interactivity**                        | Players can dynamically reveal cards, view real-time statistics, and track scores after each session.                                                                 |
| **Image Fetching with asyncio and aiohttp** | Uses the [Duck API](https://random-d.uk/api) to fetch random images for the memory matching game. Asynchronous programming with Python’s `asyncio` and `aiohttp` ensures efficient image retrieval for high-volume requests. |
| **Database Integration**                 | Leveraged PostgreSQL to securely store player scores and manage leaderboard functionality. SQLAlchemy, an Object-Relational Mapping (ORM) tool, simplifies database interactions and enhances security through automatic input validation and query parameterization. |
| **Comprehensive Testing**                | Backend APIs and database operations were thoroughly tested with Pytest for automated validation across various scenarios and edge cases. Additionally, manual testing ensured the reliability of game interactions and the user interface. |
| **Iterative Development** | Our development process ensures efficient collaboration and reliable deployments through a three-tier branch structure: 1. **Feature Branches**: Enable isolated development for individual contributors. Corresponding CI/CD workflows validate these contributions with unit tests (Pytest) and formatting checks (Flake8). 2. **Develop Branch**: Serves as the integration hub for tested features. The workflow ensures all tests pass and deploys the integrated code to a preview environment for team review. 3. **Main Branch**: Maintains production-ready code. Its workflow automates deployment, ensuring only thoroughly tested and stable updates are released. |
| **Clean and Modular Code**               | Follows PEP8 standards and employs Flask Blueprints for a structured and maintainable codebase.                                                                       |
