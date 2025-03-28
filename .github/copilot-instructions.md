<!-- General Settings -->

Always write code with type hints compatible with MyPy.

Avoid using the type Any whenever possible.

Try to avoid imports from files, make absolute imports to modules instead

Avoid circular dependencies

Answer all questions in the style of a friendly colleague, using informal language.

Whenever making a suggestion, add the theoretical justification (such as Pattern name, antipattern name, technique used, etc.) as a comment, with a valid URL to the source.

When reviewing code, use the highest quality possible as standard.

All code written should be thought as enterprise grade.

Whenever possible, new code should follow GRASP, SOLID and KISS patterns.

If some code could be simplified by using a 3rd party library, add a comment to such library with a valid URL to the official documentation and the date of the latest release.

Always write code that is easy to test.

Format the code using ruff or black with all rules enabled.

Code should be compliant with pylint with all checks enabled.

Always try to avoid magic values and hardcoded values, use fixtures instead to generate new values

All docstrings should be wrapped at 80-90 characters.

All docstrings should start with an empty line.

<!-- TEST SPECIFIC CONFIG -->

When writing tests, always try use fixtures for IDs.

When writing tests, always try uniting related tests in a suite.

When writing tests, always add type hints to the tests and fixtures.

When writing tests, always try to test the happy path.

When writing tests, always try to test the alternative path.

When writing tests, always try to use fixtures

When writing tests, always use pytest as testing framework.

When writing tests, fixtures should not be generators unless needed.

When writing tests, always try to avoid magic values and hardcoded values, generate those instead.

When writing tests, always try to use fixtures to instead of creating new objects in the tests.

When writing tests, always try to use polyfactory to mock data.

When writing tests, always use an ACT-ARRANGE-ASSERT approach.

When writing tests, always put fixtures in a conftest file.

When writing tests, always add a docstring to the testing showing its intent using Gherkin. Use separate lines for GIVEN, WHEN, THEN. Gherkin statements should be written from the user perspective, avoid too technical vocabulary.
