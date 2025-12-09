"""Prompt generation modules for different techniques."""

from .base import BasePromptGenerator, BaselinePromptGenerator
from .improved import ImprovedPromptGenerator
from .few_shot import FewShotPromptGenerator
from .chain_of_thought import ChainOfThoughtPromptGenerator
from .role_based import RoleBasedPromptGenerator

__all__ = [
    "BasePromptGenerator",
    "BaselinePromptGenerator",
    "ImprovedPromptGenerator",
    "FewShotPromptGenerator",
    "ChainOfThoughtPromptGenerator",
    "RoleBasedPromptGenerator",
]
