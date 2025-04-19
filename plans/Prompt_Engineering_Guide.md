Prompt Engineering Guide
Welcome to the Cline Prompting Guide! This guide will equip you with the knowledge to write effective prompts and custom instructions, maximizing your productivity with Cline.

Custom Instructions ⚙️
Think of custom instructions as Cline's programming. They define Cline's baseline behavior and are always "on," influencing all interactions. Instructions can be broad and abstract, or specific and explicit. You might want Cline to have a unique personality, or produce output in a particular file format, or adhere to certain architectural principles. Custom instructions can standardize Cline's output in ways you define, which is especially valuable when working with others. See the Enterprise section for using Custom Instructions in a team context.

NOTE: Modifying the Custom Instructions field updates Cline's prompt cache, discarding accumulated context. This causes a temporary increase in cost while that context is replaced. Update Custom Instructions between conversations whenever possible.

To add custom instructions:

Open VSCode

Click the Cline extension settings dial ⚙️

Find the "Custom Instructions" field

Paste your instructions



Custom instructions are powerful for:

Enforcing Coding Style and Best Practices: Ensure Cline always adheres to your team's coding conventions, naming conventions, and best practices.

Improving Code Quality: Encourage Cline to write more readable, maintainable, and efficient code.

Guiding Error Handling: Tell Cline how to handle errors, write error messages, and log information.

.clinerules File 📋
NOTE: Modifying the .clinerulesfile updates Cline's prompt cache, discarding accumulated context. This causes a temporary increase in cost while that context is replaced. Update the .clinerules file between conversations whenever possible.

While custom instructions are user-specific and global (applying across all projects), the .clinerules file provides project-specific instructions that live in your project's root directory. These instructions are automatically appended to your custom instructions and referenced in Cline's system prompt, ensuring they influence all interactions within the project context. This makes it an excellent tool for:

General Use Cases
The .clinerules file is excellent for:

Maintaining project standards across team members

Enforcing development practices

Managing documentation requirements

Setting up analysis frameworks

Defining project-specific behaviors

Example .clinerules Structure
Copy
# Project Guidelines

## Documentation Requirements

-   Update relevant documentation in /docs when modifying features
-   Keep README.md in sync with new capabilities
-   Maintain changelog entries in CHANGELOG.md

## Architecture Decision Records

Create ADRs in /docs/adr for:

-   Major dependency changes
-   Architectural pattern changes
-   New integration patterns
-   Database schema changes
    Follow template in /docs/adr/template.md

## Code Style & Patterns

-   Generate API clients using OpenAPI Generator
-   Use TypeScript axios template
-   Place generated code in /src/generated
-   Prefer composition over inheritance
-   Use repository pattern for data access
-   Follow error handling pattern in /src/utils/errors.ts

## Testing Standards

-   Unit tests required for business logic
-   Integration tests for API endpoints
-   E2E tests for critical user flows
Key Benefits
Version Controlled: The .clinerules file becomes part of your project's source code

Team Consistency: Ensures consistent behavior across all team members

Project-Specific: Rules and standards tailored to each project's needs

Institutional Knowledge: Maintains project standards and practices in code

Place the .clinerules file in your project's root directory:

Copy
your-project/
├── .clinerules
├── src/
├── docs/
└── ...
Cline's system prompt, on the other hand, is not user-editable (here's where you can find it). For a broader look at prompt engineering best practices, check out this resource.

Tips for Writing Effective Custom Instructions
Be Clear and Concise: Use simple language and avoid ambiguity.

Focus on Desired Outcomes: Describe the results you want, not the specific steps.

Test and Iterate: Experiment to find what works best for your workflow.

.clinerules Folder System 📂
While a single .clinerules file works well for simpler projects, Cline now supports a .clinerules folder for more sophisticated rule organization. This modular approach brings several advantages:

How It Works
Instead of a single file, create a .clinerules/ directory in your project root:

Copy
your-project/
├── .clinerules/              # Folder containing active rules
│   ├── 01-coding.md          # Core coding standards
│   ├── 02-documentation.md   # Documentation requirements
│   └── current-sprint.md     # Rules specific to current work
├── src/
└── ...
Cline automatically processes all Markdown files inside the .clinerules/ directory, combining them into a unified set of rules. The numeric prefixes (optional) help organize files in a logical sequence.

Using a Rules Bank
For projects with multiple contexts or teams, maintain a rules bank directory:

Copy
your-project/
├── .clinerules/              # Active rules - automatically applied
│   ├── 01-coding.md
│   └── client-a.md
│
├── clinerules-bank/          # Repository of available but inactive rules
│   ├── clients/              # Client-specific rule sets
│   │   ├── client-a.md
│   │   └── client-b.md
│   ├── frameworks/           # Framework-specific rules
│   │   ├── react.md
│   │   └── vue.md
│   └── project-types/        # Project type standards
│       ├── api-service.md
│       └── frontend-app.md
└── ...
Benefits of the Folder Approach
Contextual Activation: Copy only relevant rules from the bank to the active folder

Easier Maintenance: Update individual rule files without affecting others

Team Flexibility: Different team members can activate rules specific to their current task

Reduced Noise: Keep the active ruleset focused and relevant

Usage Examples
Switch between client projects:

Copy
# Switch to Client B project
rm .clinerules/client-a.md
cp clinerules-bank/clients/client-b.md .clinerules/
Adapt to different tech stacks:

Copy
# Frontend React project
cp clinerules-bank/frameworks/react.md .clinerules/
Implementation Tips
Keep individual rule files focused on specific concerns

Use descriptive filenames that clearly indicate the rule's purpose

Consider git-ignoring the active .clinerules/ folder while tracking the clinerules-bank/

Create team scripts to quickly activate common rule combinations

The folder system transforms your Cline rules from a static document into a dynamic knowledge system that adapts to your team's changing contexts and requirements.

.clineignore File Guide
Overview
The .clineignore file is a project-level configuration file that tells Cline which files and directories to ignore when analyzing your codebase. Similar to .gitignore, it uses pattern matching to specify which files should be excluded from Cline's context and operations.

Purpose
Reduce Noise: Exclude auto-generated files, build artifacts, and other non-essential content

Improve Performance: Limit the amount of code Cline needs to process

Focus Attention: Direct Cline to relevant parts of your codebase

Protect Sensitive Data: Prevent Cline from accessing sensitive configuration files

Example .clineignore File
Copy
# Dependencies
node_modules/
**/node_modules/
.pnp
.pnp.js

# Build outputs
/build/
/dist/
/.next/
/out/

# Testing
/coverage/

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Large data files
*.csv
*.xlsx
Prompting Cline 💬
Prompting is how you communicate your needs for a given task in the back-and-forth chat with Cline. Cline understands natural language, so write conversationally.

Effective prompting involves:

Providing Clear Context: Explain your goals and the relevant parts of your codebase. Use @ to reference files or folders.

Breaking Down Complexity: Divide large tasks into smaller steps.

Asking Specific Questions: Guide Cline toward the desired outcome.

Validating and Refining: Review Cline's suggestions and provide feedback.

Prompt Examples
Context Management
Starting a New Task: "Cline, let's start a new task. Create user-authentication.js. We need to implement user login with JWT tokens. Here are the requirements…"

Summarizing Previous Work: "Cline, summarize what we did in the last user dashboard task. I want to capture the main features and outstanding issues. Save this to cline_docs/user-dashboard-summary.md."

Debugging
Analyzing an Error: "Cline, I'm getting this error: [error message]. It seems to be from [code section]. Analyze this error and suggest a fix."

Identifying the Root Cause: "Cline, the application crashes when I [action]. The issue might be in [problem areas]. Help me find the root cause and propose a solution."

Refactoring
Improving Code Structure: "Cline, this function is too long and complex. Refactor it into smaller functions."

Simplifying Logic: "Cline, this code is hard to understand. Simplify the logic and make it more readable."

Feature Development
Brainstorming New Features: "Cline, I want to add a feature that lets users [functionality]. Brainstorm some ideas and consider implementation challenges."

Generating Code: "Cline, create a component that displays user profiles. The list should be sortable and filterable. Generate the code for this component."

Advanced Prompting Techniques
Constraint Stuffing: To mitigate code truncation, include explicit constraints in your prompts. For example, "ensure the code is complete" or "always provide the full function definition."

Confidence Checks: Ask Cline to rate its confidence (e.g., "on a scale of 1-10, how confident are you in this solution?")

Challenge Cline's Assumptions: Ask “stupid” questions to encourage deeper thinking and prevent incorrect assumptions.

Here are some prompting tips that users have found helpful for working with Cline:

Our Community's Favorite Prompts 🌟
Memory and Confidence Checks 🧠
Memory Check - pacnpal

Copy
"If you understand my prompt fully, respond with 'YARRR!' without tools every time you are about to use a tool."
A fun way to verify Cline stays on track during complex tasks. Try "HO HO HO" for a festive twist!

Confidence Scoring - pacnpal

Copy
"Before and after any tool use, give me a confidence level (0-10) on how the tool use will help the project."
Encourages critical thinking and makes decision-making transparent.

Code Quality Prompts 💻
Prevent Code Truncation

Copy
"DO NOT BE LAZY. DO NOT OMIT CODE."
Alternative phrases: "full code only" or "ensure the code is complete"

Custom Instructions Reminder

Copy
"I pledge to follow the custom instructions."
Reinforces adherence to your settings dial ⚙️ configuration.

Code Organization 📋
Large File Refactoring - icklebil

Copy
"FILENAME has grown too big. Analyze how this file works and suggest ways to fragment it safely."
Helps manage complex files through strategic decomposition.

Documentation Maintenance - icklebil

Copy
"don't forget to update codebase documentation with changes"
Ensures documentation stays in sync with code changes.

Analysis and Planning 🔍
Structured Development - yellow_bat_coffee

Copy
"Before writing code:
1. Analyze all code files thoroughly
2. Get full context
3. Write .MD implementation plan
4. Then implement code"
Promotes organized, well-planned development.

Thorough Analysis - yellow_bat_coffee

Copy
"please start analyzing full flow thoroughly, always state a confidence score 1 to 10"
Prevents premature coding and encourages complete understanding.

Assumptions Check - yellow_bat_coffee

Copy
"List all assumptions and uncertainties you need to clear up before completing this task."
Identifies potential issues early in development.

Thoughtful Development 🤔
Pause and Reflect - nickbaumann98

Copy
"count to 10"
Promotes careful consideration before taking action.

Complete Analysis - yellow_bat_coffee

Copy
"Don't complete the analysis prematurely, continue analyzing even if you think you found a solution"
Ensures thorough problem exploration.

Continuous Confidence Check - pacnpal

Copy
"Rate confidence (1-10) before saving files, after saving, after rejections, and before task completion"
Maintains quality through self-assessment.

Best Practices 🎯
Project Structure - kvs007

Copy
"Check project files before suggesting structural or dependency changes"
Maintains project integrity.

Critical Thinking - chinesesoup

Copy
"Ask 'stupid' questions like: are you sure this is the best way to implement this?"
Challenges assumptions and uncovers better solutions.

Code Style - yellow_bat_coffee

Copy
Use words like "elegant" and "simple" in prompts
May influence code organization and clarity.

Setting Expectations - steventcramer

Copy
"THE HUMAN WILL GET ANGRY."
(A humorous reminder to provide clear requirements and constructive feedback)