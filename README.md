# COMP70085-Team-Project
A team project for COMP70085 Software Systems Engineering.

## Progress Update
[✔] Implemented database interactions: Added support for storing and retrieving game data, including player scores and card layouts. See app/routes.py for details.
[✔] Random image retrieval API: Developed an API to fetch unique random images using an external service. See app/routes.py for details.

## **Project Overview**

| Feature                     | Description                                                                 |
| --------------------------- | --------------------------------------------------------------------------- |
| **Web Application**         | Based on a modern web architecture, using Flask for the backend and HTML/CSS/JavaScript for the frontend. |
| **Fun, Simple, and Useful** | The game is easy to play, improves memory, and provides a fun challenge.    |
| **Production Deployment**   | Deployed using an Impaas platform, ensuring availability and usability.     |
| **Interactivity**           | Users can click cards to reveal them dynamically, view stats, and save scores post-game. |
| **External API**            | Utilizes Unsplash API to fetch random images, enhancing the gameplay experience. |
| **Database Storage and Query** | Stores user scores using SQLite or PostgreSQL, supporting leaderboard queries.    |
| **Automated Testing**       | Backend APIs and database operations are tested using PyTest to ensure correctness. |
| **Iterative Delivery**      | Development is divided into stages (API integration, game logic, database connection, frontend optimization, deployment). |
| **Automated CI/CD Pipeline** | GitHub Actions ensure continuous integration, testing, and deployment.     |
| **Clean, Modular Code**     | Adheres to PEP8 standards, with a modular structure using Flask Blueprints for separation of concerns. |

---

## **How We Worked as a Team**

Our collaboration relied on a structured workflow with **Branch-Specific CI/CD Pipelines** to ensure smooth teamwork and maintain code quality across shared codebases. Each branch served a specific purpose in the development lifecycle, supported by tailored CI/CD workflows:

- **Feature Branches**: Each team member (e.g., Ziheng Shan, Tiffany Liu, Wenqing Tu, Chujia Song) worked independently on feature branches named `feature/<username>_<feature_description>`. 
- **Develop Branch**: Used for integration testing and deploying to a preview environment after merging feature branches.
- **Main Branch**: Reserved for stable, production-ready code with automated deployment to production.

This structure allowed us to isolate individual contributions, ensure compatibility during integration, and confidently deploy stable updates.

---

## **Branch-Specific CI/CD**

### **Design Principles**

1. **Branch-Specific Workflows**:
   - **Feature Branch Workflow (`feature-ci.yml`)**:
     - Validates individual contributions with unit tests (`pytest`) and code formatting checks (`flake8`).
     - Supports member-specific configurations for dependencies and test markers.
   - **Develop Branch Workflow (`develop-ci.yml`)**:
     - Ensures integrated features pass all tests and are deployed to a preview environment for team review.
   - **Main Branch Workflow (`main-ci.yml`)**:
     - Automates deployment of production-ready code after thorough testing.

2. **Automation**:
   - Repetitive tasks like testing, formatting, and deployment are fully automated to reduce errors and save time.

3. **Modularity**:
   - Separate workflows ensure independent CI/CD pipelines for different branches, preventing interference between development stages.
