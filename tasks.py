# importerer Task fra CrewAI biblioteket
from crewai import Task
# henter de tre agenter
from agents import architect, coder, tester

# opretter en ny opgave og gemmer den i variablen Task
design_task = Task(
    description=(
        "Design a simple Todo web app in HTML/CSS/JS.\n\n"

        "You must produce a design document that PRECISELY covers:\n"
        "  1. LAYOUT: Overall page layout (header, main, footer). "
        "Describe each section's visual purpose and position.\n"
        "  2. COMPONENTS: List all UI components (input field, buttons, "
        "todo list, todo item, checkbox, delete button). For each component "
        "state its responsibility and the HTML tag that should be used "
        "(semantic HTML).\n"
        "  3. USER INTERACTIONS: Describe exactly what happens step-by-step "
        "when the user: (a) adds a todo, (b) marks a todo as completed, "
        "(c) deletes a todo.\n"
        "  4. DATA MODEL: Define the structure of a todo object in JSON "
        "(fields, types, example values).\n"
        "  5. PERSISTENCE STRATEGY: Describe the localStorage approach: "
        "which key is used, when data is saved, when it is loaded, and what "
        "happens if localStorage is empty on first visit.\n"
        "  6. LIMITATIONS AND RISKS: Name at least 2 known limitations of "
        "localStorage (e.g. no cross-tab sync, size limit, not suitable for "
        "sensitive data).\n\n"

        "Keep the document concise but complete. It must be readable in under "
        "5 minutes and give a developer everything they need."
    ),

    expected_output=(
        "A structured design document with the following sections:\n"
        "- Layout (overall page structure with section descriptions)\n"
        "- Components (complete list with HTML tag and responsibility)\n"
        "- User Interactions (step-by-step for add / complete / delete)\n"
        "- Data Model (JSON structure with fields and types)\n"
        "- localStorage Strategy (key name, save/load timing, empty-state fallback)\n"
        "- Known Limitations (minimum 2 bullet points)\n\n"
        "The document must be written in English and must not exceed 400 words."
    ),

    agent=architect,
    # No context — this is the first task in the pipeline
)

code_task = Task(
    description=(
        "Build a complete Todo web app as a single index.html file.\n\n"

        "IMPORTANT: Read the design document in your context carefully BEFORE "
        "writing any code. Follow the architect's specifications precisely.\n\n"

        "TECHNICAL REQUIREMENTS:\n"
        "  - HTML, CSS and vanilla JavaScript only — no frameworks, no npm "
        "packages, no CDN imports\n"
        "  - All CSS and JS must be embedded in index.html (no separate files)\n"
        "  - Use semantic HTML5 elements (e.g. <main>, <header>, <ul>, <li>, "
        "<button>, <label for=...>)\n\n"

        "FUNCTIONAL REQUIREMENTS (all MUST be implemented):\n"
        "  1. Add todo: the HTML MUST contain a visible <input> with id='input-field' "
        "AND a <button> with id='add-btn' inside the <body>. "
        "Clicking the button or pressing Enter appends a new todo. "
        "Empty input is silently ignored.\n"
        "  2. Mark as completed: every todo item MUST have a clickable element that "
        "toggles completed state. After toggling, saveTodos() MUST be called "
        "immediately so the state persists across reloads.\n"
        "  3. Delete todo: a delete button next to each todo removes it from "
        "the DOM AND calls saveTodos() immediately after.\n"
        "  4. Persistence: all todos are saved to localStorage under the key 'todos'. "
        "Data is loaded automatically when the page opens. If localStorage is empty, "
        "an empty list is shown (no errors).\n\n"

        "WIRING REQUIREMENTS (common source of bugs — follow exactly):\n"
        "  - The add button and input MUST exist in the HTML before the <script> runs. "
        "Do NOT rely on JavaScript to create them.\n"
        "  - Buttons inside dynamically created todo items MUST use event delegation: "
        "attach ONE click listener to the <ul> and use e.target to identify which "
        "button was clicked. Do NOT add individual listeners inside loops.\n"
        "  - Every function that changes the todos array MUST call saveTodos() "
        "before returning.\n\n"

        "CODE QUALITY REQUIREMENTS:\n"
        "  - Use `const` and `let` (never `var`)\n"
        "  - All functions must have a descriptive name and a short comment\n"
        "  - localStorage.getItem() MUST use null-coalescing: "
        "JSON.parse(localStorage.getItem('todos') ?? '[]')\n"
        "  - Use textContent (never innerHTML) when inserting user-supplied text "
        "to prevent XSS\n"
        "  - All <button> elements must have visible text or an aria-label\n\n"

        "DELIVERABLE:\n"
        "Write the complete index.html file as your response. "
        "Begin with <!-- index.html --> as the very first line."
    ),

    expected_output=(
        "A complete index.html file that:\n"
        "  - Starts with <!-- index.html -->\n"
        "  - Contains all HTML, CSS and JS in a single file\n"
        "  - Implements all 4 functional requirements (add, complete, delete, "
        "localStorage)\n"
        "  - Uses semantic HTML5\n"
        "  - Has comments on all non-trivial JS functions\n"
        "  - Handles null values from localStorage explicitly\n"
        "  - Has ARIA labels on interactive elements without visible text\n"
        "The file must be openable directly in a browser and work without "
        "any console errors."
    ),

    agent=coder,
    context=[design_task],  # Coder receives the architect's design document
)

test_task = Task(
    description=(
        "Review the Todo app code from your context and produce a detailed "
        "QA report.\n\n"

        "IMPORTANT: Read the code LINE BY LINE. Verify each functional "
        "requirement explicitly — do not assume something works because it "
        "looks correct.\n\n"

        "YOUR REVIEW MUST COVER THESE 4 PERSPECTIVES:\n\n"

        "1. FUNCTIONALITY (mentally test each requirement):\n"
        "   - Does 'add todo' work with both Enter key AND button click? "
        "What happens with empty input?\n"
        "   - Does 'mark as completed' work? Is the styling updated correctly?\n"
        "   - Does 'delete' work? Is the item removed from both the DOM AND "
        "localStorage?\n"
        "   - Are existing todos loaded on page reload? "
        "What happens with empty localStorage?\n\n"

        "2. JAVASCRIPT CORRECTNESS:\n"
        "   - Are there null-checks on localStorage.getItem()?\n"
        "   - Are JSON.parse() and JSON.stringify() used correctly?\n"
        "   - Is there any XSS risk via innerHTML with user input? "
        "(Check whether input is sanitised)\n"
        "   - Is there any use of `var` (should be const/let)?\n"
        "   - Are there any unhandled exceptions (e.g. JSON.parse() called on "
        "corrupt data)?\n\n"

        "3. ACCESSIBILITY (a11y):\n"
        "   - Do all <button> elements have visible text or an aria-label?\n"
        "   - Do all <input> fields have an associated <label>?\n"
        "   - Can the app be operated with keyboard only (Tab, Enter, Space)?\n"
        "   - Are completed todos communicated in a way that is understandable "
        "to screen readers (e.g. aria-checked or role)?\n\n"

        "4. CODE QUALITY AND MAINTAINABILITY:\n"
        "   - Do functions have descriptive names and comments?\n"
        "   - Is there duplicated code that should be extracted?\n"
        "   - Is the CSS clear and consistent?\n"
        "   - Are there hardcoded strings that should be constants?\n\n"

        "SEVERITY LEVELS:\n"
        "Tag each finding with one of the following:\n"
        "  [CRITICAL]    — app does not work / data is lost / security risk\n"
        "  [MAJOR]       — feature is missing or fails on edge cases\n"
        "  [MINOR]       — cosmetic issue or small UX problem\n"
        "  [ENHANCEMENT] — not wrong, but could be improved\n"
    ),

    expected_output=(
        "A QA report structured into these sections:\n\n"
        "## Summary\n"
        "  - Finding count per severity (Critical / Major / Minor / Enhancement)\n"
        "  - Overall verdict: Ready for release? Yes / No / With reservations\n\n"
        "## Functionality Findings\n"
        "  - Each finding in format: [SEVERITY] Description. Recommended fix.\n\n"
        "## JavaScript Correctness Findings\n"
        "  - Each finding with line number where possible\n\n"
        "## Accessibility (a11y) Findings\n"
        "  - Each finding with reference to a WCAG guideline where relevant\n\n"
        "## Code Quality\n"
        "  - General observations and concrete suggestions\n\n"
        "The report must be written in English and must be directly usable by "
        "the developer to prioritise fixes."
    ),

    agent=tester,
    context=[code_task],  # Tester receives the developer's code
)