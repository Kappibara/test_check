import enum

class PaymentType(str, enum.Enum):
    CASH = "CASH"
    CASHLESS = "CASHLESS"