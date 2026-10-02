from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class SerieSGS:
    codigo: int
    nome: str
    periodicidade: str
    unidade: str


SELIC_META = SerieSGS(
    codigo=432,
    nome="Meta Selic definida pelo Copom",
    periodicidade="diária",
    unidade="percentual ao ano",
)


def url_sgs(serie: SerieSGS, inicio: date, fim: date) -> str:
    if inicio > fim:
        raise ValueError("A data inicial não pode ser posterior à data final.")
    base = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{serie.codigo}/dados"
    return (
        f"{base}?formato=json"
        f"&dataInicial={inicio.strftime('%d/%m/%Y')}"
        f"&dataFinal={fim.strftime('%d/%m/%Y')}"
    )
