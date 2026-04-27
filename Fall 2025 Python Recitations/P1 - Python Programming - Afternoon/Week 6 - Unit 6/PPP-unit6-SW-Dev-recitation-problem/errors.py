# errors.py

class AccountNotFoundError(Exception):
    """Raised when an account does not exist."""
    pass

class InsufficientFundsError(Exception):
    """Raised when a withdrawal amount exceeds the account balance."""
    pass

class InvalidAmountError(Exception):
    """Raised when a deposit or withdrawal amount is invalid (zero or negative)."""
    pass

class DuplicateAccountError(Exception):
    """Raised when trying to create an account that already exists."""
    pass
