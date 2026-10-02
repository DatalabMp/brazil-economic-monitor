import json
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class RegistroSGS:
    data: date
    valor: float


def parse_sgs_json(payload: str) -> list[RegistroSGS]:
    try:
        dados = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise ValueError("A resposta do SGS não contém JSON válido.") from exc

    if not isinstance(dados, list):
        raise ValueError("A resposta do SGS deve ser uma lista de registros.")

    registros: list[RegistroSGS] = []
    datas: set[date] = set()

    for indice, item in enumerate(dados, start=1):
        if not isinstance(item, dict) or set(item) != {"data", "valor"}:
            raise ValueError(
                f"Registro SGS inválido na posição {indice}: esperado apenas 'data' e 'valor'."
            )

        try:
            data_registro = date.fromisoformat(item["data"][6:10] + "-" + item["data"][3:5] + "-" + item["data"][:2])
            valor = float(item["valor"].replace(",", "."))
        except (TypeError, ValueError, AttributeError) as exc:
            raise ValueError(f"Registro SGS inválido na posição {indice}.") from exc

        if data_registro in datas:
            raise ValueError(f"Data duplicada na resposta do SGS: {item['data']}.")

        datas.add(data_registro)
        registros.append(RegistroSGS(data=data_registro, valor=valor))

    return registros
