### **Collaboration Guidelines**

This document provides all team members with a clear, consistent framework for collaborating effectively on the project.

---

## **Collaboration Philosophy**

We aim to create a robust and enjoyable application while maintaining a high standard of collaboration. This involves:
- Clear branch workflows for each team member.
- Modular, well-documented code.
- Regular communication to ensure smooth integration.
- Effective use of automated tools (e.g., CI/CD pipelines, linting, testing).

---

## **Setting Up Your Environment**

### 1. **Create a Python Virtual Environment**
   - Use Python 3.12 to create a virtual environment named `sse_env`:
     ```bash
     python3.12 -m venv sse_env
     source sse_env/bin/activate  # On Windows: sse_env\Scripts\activate
     ```

### 2. **Install Project Dependencies**
   - Install required libraries (Flask, PyTest, Flake8):
     ```bash
     pip install -r requirements.txt
     ```

---

## **Branch Workflow**

### **Branch Naming Convention**
1. **Feature Branch**: `feature/<yourname>_<description>` (e.g., `feature/cs824_gameLogic`).
2. **Main Branch**: `main` contains stable production-ready code.
3. **Development Branch**: `develop` is the integration branch.

---

### **Workflow Steps**

#### **1. Creating a New Feature Branch**
- Start from the `develop` branch:
  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b feature/<yourname>_<description>
  ```

#### **2. Making Changes**
- Make your edits and save changes to your branch.

#### **3. Testing and Formatting**

To streamline formatting and testing, we recommend setting up the **Ruff** plugin in VS Code with the following settings:

1. **Install Ruff Plugin**:
   - Open the **Extensions** view in VS Code (`Ctrl+Shift+X` or `Cmd+Shift+X` on macOS).
   - Search for **Ruff** and install the plugin.

2. **Set Up VS Code Formatting**:
   - Go to **Settings** (`Ctrl+,` or `Cmd+,` on macOS).
   - Search for `Editor: Default Formatter` and set it to `Ruff`.
   - Enable `Editor: Format On Save` to auto-format your code when saving.
   - Configure `line length` to 79 characters:
     - Search for **Ruff: Line Length** in settings.
     - Set it to `79`.

3. **Run Automated Tests**:
   - Use `pytest` to run unit tests:
     ```bash
     pytest
     ```

4. **Check Formatting**:
   - Use `flake8` for linting:
     ```bash
     flake8 *.py
     ```

By setting up Ruff for auto-formatting and enabling `Format On Save`, you can significantly simplify the process of maintaining clean, consistent code.

#### **4. Committing Your Work**
- Stage your changes:
  ```bash
  git add .
  ```
- Commit with a descriptive message:
  ```bash
  git commit -m "Implemented game logic for flipping cards"
  ```

#### **5. Pushing Changes**
- Push your branch to the repository:
  ```bash
  git push origin feature/<yourname>_<description>
  ```

---

### **6. Submitting a Pull Request (PR)**
- Go to the GitHub repository and click **Pull Requests**.
- Click **New Pull Request** and select:
  - **Base Branch**: `develop`
  - **Compare Branch**: `feature/<yourname>_<description>`
- Add a description of your changes and assign at least one reviewer.

---

### **7. Reviewing and Merging**
- After the PR is reviewed and CI checks pass:
  - Merge into `develop` (do it in Github).

---

### **8. Final Deployment**
- After all features are integrated into `develop` and tested:
  - Create a PR to merge `develop` into `main` for production deployment.

---

This document ensures all team members are aligned on workflows, responsibilities, and processes for smooth collaboration.