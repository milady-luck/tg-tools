import logging

import pytest

from tgtools.parsing import parse_coin_call_resp, find_ticker
from tgtools.types import ParsedCoinCallResp, TgUser

logger = logging.getLogger(__name__)

class TestFindTicker:
    def test_single_dollar(self):
        ticker_line = "foo bar $WIF"
        ticker = find_ticker(ticker_line)
        assert ticker == 'WIF'

    def test_multi_dollar(self):
        for i in range(10):
            prefix = '$' * i
            ticker = find_ticker(f"foo bar ${prefix}WIF")
            assert ticker == prefix + 'WIF'
        

class TestRickRespParse:
    
    def test_k_fdv(self):
        s = """🔥 I CHOOSE RICH EVERYTIME! [694.0K/53.3K%] $NICK
🌐 Solana @ Raydium
💰 USD: $0.0006939
💎 FDV: $694.0K 
💦 Liq: $44.7K [x31.0] 
📊 Vol: $318K 🕰️ Age: 1h
⛰️ ATH: $694.0K 
🚀 1H: 3.1K% | $280.3K 🅑 1161 🅢 809
👥 TH: 5.0 | 5.0 | 3.4 | 3.4 | 3.4 [37%]
🖨️ Mint: ✅ | LP: 🔥

G3q2zUkuxDCXMnhdBPujjPHPw9UTMDbXqzcc2UHM3jiy
BAN | BNK | DEX | BRD | DT | JUP | RAY
UNI | STB | PHO | EXP | RUG | SOC | TW
CAL | MNZ | MAG | ORC | FLX | SRM

🏆 [redacted] @ 15.6K 👀 211
⚔️ TIP: Farm Cambria Duel Arena"""
        parsed = parse_coin_call_resp(s)
        expected = ParsedCoinCallResp("NICK", "Solana", "Raydium", 694_000.0, 694_000.0)

        assert parsed == expected

    def test_m_fdv(self):
        s = """💊 Nailong [25.7M/52.1%] $NAILONG 🔼
🌐 Solana @ Raydium
💰 USD: $0.02571
💎 FDV: $25.7M 
💦 Liq: $1.1M 🐡 [x46.5] 
📊 Vol: $3M 🕰️ Age: 1mo
⛰️ ATH: $27.8M [6d ago] 
📈 1H: 38.9% ⋅ $658K 🅑 251 🅢 382
👥 TH: 2.3⋅2.1⋅2.1⋅2.1⋅1.8 [18%]
🖨️ Mint: ✅ ⋅ LP: 🔥
🧰 More: 📊 🫧 🎨 💪 💬 🌍 🐦 [♺]

mkvXiNBpa8uiSApe5BrhWVJaT87pJFTZxRy7zFapump
MAE⋅BAN⋅BNK⋅SHU⋅PEP⋅MVX⋅DEX
TRO⋅STB⋅PHO⋅BLX⋅GMG⋅EXP⋅TW

🏆 lasercat397 @ 1.3M⋅19x⋅1mo 👀 8.6K
📈 TIP: Trade pump.fun on Photon"""
        parsed = parse_coin_call_resp(s)
        expected = ParsedCoinCallResp(
            "NAILONG", "Solana", "Raydium", 25_700_000.0, 27_800_000.0
        )

        assert parsed == expected

    def test_b_fdv(self):
        s = """🟡 dogwifhat [1.7B/-0.7%] $$WIF 🔼
🌐 Solana @ Orca Wp
💰 USD: $1.75
💎 FDV: $1.7B 
� Liq: $1.7M 🐡 [x2033.5] 
�📊 Vol: $24M 🕰️ Age: 4mo
⛰️ ATH: $3.4B [3mo ago] 
📉 1H: -0.9% ⋅ $664.6K 🅑 682 🅢 624
🖨️ Mint: ✅ | LP: ‼️
🧰 More: 📊 🫧 💪 💬 TG⋅X⋅WEB

EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm
MAE⋅BAN⋅BNK⋅SHU⋅PEP⋅DEX⋅BRD
TRO⋅STB⋅PHO⋅BLX⋅EXP⋅RUG⋅TW

🏆 rightcalibre @ 1.7B⋅2mo 👀 1950  # noqa: W29150
📢 AD: Snipe, trade & win 10 $SOL - DEX3"""
        parsed = parse_coin_call_resp(s)
        expected = ParsedCoinCallResp(
            "$WIF", "Solana", "Orca", 1_700_000_000, 3_400_000_000
        )

        assert parsed == expected

    # TODO: test non-call messages
