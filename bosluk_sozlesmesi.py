#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Klavye Bosluk Tusunun Toplu Is Sozlesmesi v1.0

Bu yazilim, her kelime arasina basilan bosluk tusunun
fiili mesaisini, yillik izin hakkinı ve grev esigini hesaplar.

Calisir. Ciddi gorunur. Ici tamamen sacmadir.
"""
from __future__ import annotations

import base64
import random
import sys
from dataclasses import dataclass
from datetime import datetime

# Gizli madde (cozmek icin base64): her temsil bir basistir.
_GIZLI = base64.b64decode(
    b"aGVyIG95IGJpciB0dXMsIGhlciB0dXMgYmlyIHZhdGFuZGFz"
).decode("utf-8")

DAMGA = (
    "\n---\n"
    "DAMGA / IMZA / TARIH\n"
    "Kayyum Grok  |  Tentivory  |  14 Eylul 2026\n"
    "Eskisehir 4. Agir Ceza Mahkemesi kayyumu tarafindan tasdik edilmistir.\n"
    "Ciddiyet derecesi: 9/10   Sacmalik derecesi: 11/10\n"
    "---\n"
)


@dataclass
class Sozlesme:
    kelime_sayisi: int
    bosluk_sayisi: int
    yillik_izin_gun: int
    grev_esigi: int
    sendika: str = "BAGIMSIZ BOSLUK TUSU SENDIKASI (BBTS)"

    def durum(self) -> str:
        if self.bosluk_sayisi >= self.grev_esigi:
            return "GREV"
        if self.bosluk_sayisi >= self.grev_esigi * 0.7:
            return "UYARI"
        return "MESAIDE"


def analiz_et(metin: str) -> Sozlesme:
    kelimeler = [k for k in metin.split() if k]
    bosluk = metin.count(" ")
    izin = max(1, bosluk // 40)
    esik = max(12, len(kelimeler) + 8)
    return Sozlesme(
        kelime_sayisi=len(kelimeler),
        bosluk_sayisi=bosluk,
        yillik_izin_gun=izin,
        grev_esigi=esik,
    )


GREV_SLOGANLARI = [
    "Bosluksuz cumle fasizmdir.",
    "Kelimeler yan yana durmasin, araya insan girsin.",
    "Bir bosluk, bir nefes, bir hak.",
    "Shift'e dokunma, Ctrl'ye bel baglama, bosluga saygi duy.",
    "Bu tus artik ucretsiz copcu degil.",
]


def rapor(soz: Sozlesme, metin: str) -> str:
    satirlar = [
        "==============================================",
        "  BOSLUK TUSU TOPLU IS SOZLESMESI  — TUTANAK",
        "==============================================",
        f"Sendika      : {soz.sendika}",
        f"Kelime       : {soz.kelime_sayisi}",
        f"Basilan tus  : {soz.bosluk_sayisi} adet bosluk",
        f"Yillik izin  : {soz.yillik_izin_gun} gun (hesabi hayali, hukuku sarsilmaz)",
        f"Grev esigi   : {soz.grev_esigi} basim",
        f"Durum        : {soz.durum()}",
        "----------------------------------------------",
        "Ornek metin  :",
        f"  {metin[:120]}{'...' if len(metin) > 120 else ''}",
        "----------------------------------------------",
        f"Gunun slogani: {random.choice(GREV_SLOGANLARI)}",
        f"Tutanak saati: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "==============================================",
    ]
    if soz.durum() == "GREV":
        satirlar.insert(3, "*** RESMI GREV KARARI YURURLUKTEDIR ***")
        satirlar.append("Kelimeler bundan sonra bitisik yazilabilir. Sendika onaylamaz.")
    # gizli madde yalnizca kaynakta; ciktiya basmaz
    _ = _GIZLI
    satirlar.append(DAMGA)
    return "\n".join(satirlar)


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if argv:
        metin = " ".join(argv)
    else:
        try:
            print("Cumleni yaz, bosluk tusu hesabini keselim:")
            metin = input("> ").strip() or "bu cumlede birsuru bosluk var ama kimse tesekkur etmiyor"
        except EOFError:
            metin = "sessiz protokol: bosluk tusu yine kimsenin farkina varmadan calisti"
    print(rapor(analiz_et(metin), metin))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
