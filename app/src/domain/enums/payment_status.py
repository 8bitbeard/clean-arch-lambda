from enum import Enum


class PaymentStatus(Enum):
    REJECTED = "Rejeitado"
    IN_ANALYSIS = "Em análise"
    SUCCEEDED = "Sucesso"
