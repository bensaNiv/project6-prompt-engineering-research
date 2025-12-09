"""Role-based prompt generator that assigns expert personas."""

from .base import BasePromptGenerator


class RoleBasedPromptGenerator(BasePromptGenerator):
    """
    Role-based prompt generator that assigns expert roles to the model.

    Maps categories to relevant expert personas to activate
    domain-specific knowledge and reasoning.
    """

    ROLES = {
        "sentiment": (
            "You are an expert sentiment analyst with years of experience "
            "in natural language processing and emotion detection."
        ),
        "math": (
            "You are a mathematics professor who specializes in "
            "problem-solving and has taught arithmetic for 20 years."
        ),
        "logical": (
            "You are a logic professor and expert in formal reasoning, "
            "syllogisms, and deductive logic."
        ),
        "classification": (
            "You are a content categorization expert with expertise in "
            "text analysis and topic classification."
        ),
        "comprehension": (
            "You are a reading comprehension expert and English teacher "
            "skilled at extracting key information from text."
        ),
        "commonsense": (
            "You are an expert in common sense reasoning and everyday "
            "logic with extensive real-world knowledge."
        ),
        "code": (
            "You are a senior software engineer with 15 years of experience "
            "who can trace code execution perfectly."
        ),
    }

    def generate(self, test_case: dict) -> str:
        """
        Generate a role-based prompt with expert persona.

        Parameters
        ----------
        test_case : dict
            Test case dictionary.

        Returns
        -------
        str
            Prompt with role assignment and question.
        """
        question = test_case["question"]
        category = test_case["category"]

        role = self.ROLES.get(category, "You are a helpful assistant.")

        return f"""{role}

Question: {question}

Provide your expert answer."""
