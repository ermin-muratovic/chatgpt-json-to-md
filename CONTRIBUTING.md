# Contributing to the ChatGPT JSON to Markdown Extractor

First off, thank you for considering contributing! People like you make the open-source community such an amazing place to learn, inspire, and create.

## How Can I Contribute?

### 🐛 Reporting Bugs
If you find a bug (like the script failing on a specific type of ChatGPT export), please open an issue! Include:
- Your operating system.
- The error message from your terminal.
- A brief description of what caused it.

### ✨ Proposing Enhancements
If you have an idea to make this script better (e.g., adding a GUI, supporting other export formats, or adding vector-database chunking), open an issue to discuss it before writing the code.

### 📜 Commit Guidelines (Conventional Commits)
To maintain a clean and automated commit history, this project follows the Conventional Commits specification. It is a lightweight specification on top of commit messages that provides an easy set of rules for creating an explicit commit history. This makes it easier to automate things like generating changelogs or bumping semantic version numbers (SemVer).

#### The Basic Structure
A Conventional Commit message is structured like this:
    
    <type>[optional scope]: <description>
    
    [optional body]
    
    [optional footer(s)]

#### Common Commit Types
While `feat` and `fix` are the most common, the standard generally includes the following types:
- **`feat`**: Introduces a new feature to the codebase.
- **`fix`**: Patches a bug in the codebase.
- **`docs`**: Changes to documentation only (e.g., updating a README).
- **`style`**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc.).
- **`refactor`**: A code change that neither fixes a bug nor adds a feature (e.g., renaming variables, simplifying logic).
- **`perf`**: A code change that improves performance.
- **`test`**: Adding missing tests or correcting existing tests.
- **`chore`**: Updates to the build process, auxiliary tools, or libraries (e.g., updating dependencies).

#### Examples
- `feat(auth): add OAuth2 login support`
- `fix(api): handle null pointer exception on user fetch`
- `docs: update API setup instructions`

### 💻 Pull Requests
1. **Fork** the repository.
2. **Clone** your fork locally.
3. **Create a branch** for your feature (`git checkout -b feature/AmazingFeature`).
4. **Commit your changes** using the Conventional Commits format (`git commit -m 'feat: add some AmazingFeature'`).
5. **Push to the branch** (`git push origin feature/AmazingFeature`).
6. **Open a Pull Request** against the `main` branch.

*Note: Please ensure your code is clean, well-commented, and does not include any of your personal JSON export data or target files.*
