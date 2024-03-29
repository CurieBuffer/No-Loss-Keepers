import os

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"

CHAIN_ID = {
    "arb-sandbox": "421613",
    "arb-testnet": "421613",
    "arb-mainnet": "42161",
    "blast-testnet": "168587773",
}
ROUTER = {
    "arb-sandbox": "0xF7760095561259e9c52A62A7743d3451d010E97b",
    "blast-testnet": "0xC42D0a6d10fd4E0085F82cAE02Bb10a2A6b9650E",
    # "arb-testnet": "0x2430E4aD865423Ed994daD297D66b77F3ec2B008",
    # "arb-mainnet": "0x075EEA84D1122A0c2F2A6C9265F8126F64087d44",
    # "polygon-testnet": "0x3E8d70286567bf962261a81Da5DBDe6cBbc444C4",
    # "polygon-mainnet": "0xBBac5088Ea7E70f21C28058A434Afa64FDf401c7",
}
PYTH = {
    "arb-sandbox": "0x24f72ee89Ad0fd5c44913DF378d2cF4e40107582",
    "blast-testnet": "0xA2aa501b19aff244D90cc15a4Cf739D2725B5729",
}
PYTH_ENDPOINT = "https://hermes.pyth.network"


MULTICALL = {
    "arb-sandbox": "0x20f171c51A9B707D1A6daAb809e2729308406f99",
    "arb-testnet": "0x20f171c51A9B707D1A6daAb809e2729308406f99",
    "arb-mainnet": "0x842eC2c7D803033Edf55E478F461FC547Bc54EB2",
    "polygon-testnet": "0xF6b05f349E64CB2202a6C7D53daaDccC48f82C25",
    "polygon-mainnet": "0xc8E51042792d7405184DfCa245F2d27B94D013b6",
    "blast-testnet": "0x8823C4db31c9e75964c06ee2838E1763a0Cf5cd2",
}


BASE_URL = os.environ.get("BASE_URL")

GRAPH_ENDPOINT = {
    "arb-sandbox": "https://subgraph.satsuma-prod.com/e66b06ce96d2/bufferfinance/no-loss-arbitrum-testnet/api",
    "blast-testnet": "https://no-loss-production.up.railway.app/",
    # "arb-testnet": "https://subgraph.satsuma-prod.com/e66b06ce96d2/bufferfinance/arbitrum-testnet/api",
    # "arb-mainnet": "https://subgraph.satsuma-prod.com/e66b06ce96d2/bufferfinance/v2.5-arbitrum-mainnet/api",
    # "polygon-sandbox": "https://subgraph.satsuma-prod.com/e66b06ce96d2/bufferfinance/polygon-testnet/api",
    # "polygon-mainnet": "https://api.thegraph.com/subgraphs/name/bufferfinance/polygon-mainnet-lite",
    # "polygon-testnet": "https://subgraph.satsuma-prod.com/e66b06ce96d2/bufferfinance/polygon-testnet/api",
}


GAS_PRICE = {
    "arb-sandbox": 0.1e9,
    "arb-testnet": 0.1e9,
    "arb-mainnet": 0.1e9,
    "blast-testnet": 0.1e9,
    "polygon-testnet": 0.1e9,
    "polygon-mainnet": 200e9,
}

GAS_LIMIT_PER_TXN = {
    "arb-sandbox": 10_000_000,
    "blast-testnet": 10_000_000,
    "arb-testnet": 10_000_000,
    "arb-mainnet": 15_000_000,
    "polygon-testnet": 5_000_000,
    "polygon-mainnet": 5_000_000,
}

PYTH_SYMBOL_MAPPING = dict(
    [
        ("Crypto.1INCH/USD", "1INCHUSD"),
        ("Crypto.AAVE/USD", "AAVEUSD"),
        ("Crypto.ACM/USD", "ACMUSD"),
        ("Crypto.ADA/USD", "ADAUSD"),
        ("Crypto.ALGO/USD", "ALGOUSD"),
        ("Crypto.ALICE/USD", "ALICEUSD"),
        ("Crypto.ALPACA/USD", "ALPACAUSD"),
        ("Crypto.AMP/USD", "AMPUSD"),
        ("Crypto.ANKR/USD", "ANKRUSD"),
        ("Crypto.APE/USD", "APEUSD"),
        ("Crypto.APT/USD", "APTUSD"),
        ("Crypto.ARB/USD", "ARBUSD"),
        ("Crypto.ARG/USD", "ARGUSD"),
        ("Crypto.ASR/USD", "ASRUSD"),
        ("Crypto.ATLAS/USD", "ATLASUSD"),
        ("Crypto.ATM/USD", "ATMUSD"),
        ("Crypto.ATOM/USD", "ATOMUSD"),
        ("Crypto.AURORA/USD", "AURORAUSD"),
        ("Crypto.AVAX/USD", "AVAXUSD"),
        ("Crypto.AXS/USD", "AXSUSD"),
        ("Crypto.BAR/USD", "BARUSD"),
        ("Crypto.BCH/USD", "BCHUSD"),
        ("Crypto.BETH/USD", "BETHUSD"),
        ("Crypto.BIT/USD", "BITUSD"),
        ("Crypto.BNB/USD", "BNBUSD"),
        ("Crypto.BNX/USD", "BNXUSD"),
        ("Crypto.BONK/USD", "BONKUSD"),
        ("Crypto.BTC/USD", "BTCUSD"),
        ("Crypto.BUSD/USD", "BUSDUSD"),
        ("Crypto.C98/USD", "C98USD"),
        ("Crypto.CAKE/USD", "CAKEUSD"),
        ("Crypto.CBETH/USD", "CBETHUSD"),
        ("Crypto.CELO/USD", "CELOUSD"),
        ("Crypto.CHR/USD", "CHRUSD"),
        ("Crypto.CHZ/USD", "CHZUSD"),
        ("Crypto.CITY/USD", "CITYUSD"),
        ("Crypto.CRO/USD", "CROUSD"),
        ("Crypto.CRV/USD", "CRVUSD"),
        ("Crypto.CUSD/USD", "CUSDUSD"),
        ("Crypto.CVX/USD", "CVXUSD"),
        ("Crypto.DAI/USD", "DAIUSD"),
        ("Crypto.DOGE/USD", "DOGEUSD"),
        ("Crypto.DOT/USD", "DOTUSD"),
        ("Crypto.DYDX/USD", "DYDXUSD"),
        ("Crypto.ETH/USD", "ETHUSD"),
        ("Crypto.FET/USD", "FETUSD"),
        ("Crypto.FIDA/USD", "FIDAUSD"),
        ("Crypto.FIL/USD", "FILUSD"),
        ("Crypto.FLOKI/USD", "FLOKIUSD"),
        ("Crypto.FLOW/USD", "FLOWUSD"),
        ("Crypto.FTM/USD", "FTMUSD"),
        ("Crypto.FTT/USD", "FTTUSD"),
        ("Crypto.GAL/USD", "GALUSD"),
        ("Crypto.GALA/USD", "GALAUSD"),
        ("Crypto.GMT/USD", "GMTUSD"),
        ("Crypto.GMX/USD", "GMXUSD"),
        ("Crypto.INJ/USD", "INJUSD"),
        ("Crypto.INTER/USD", "INTERUSD"),
        ("Crypto.JST/USD", "JSTUSD"),
        ("Crypto.JUV/USD", "JUVUSD"),
        ("Crypto.LAZIO/USD", "LAZIOUSD"),
        ("Crypto.LDO/USD", "LDOUSD"),
        ("Crypto.LINK/USD", "LINKUSD"),
        ("Crypto.LTC/USD", "LTCUSD"),
        ("Crypto.LUNA/USD", "LUNAUSD"),
        ("Crypto.LUNC/USD", "LUNCUSD"),
        ("Crypto.MATIC/USD", "MATICUSD"),
        ("Crypto.MBOX/USD", "MBOXUSD"),
        ("Crypto.MIR/USD", "MIRUSD"),
        ("Crypto.MNGO/USD", "MNGOUSD"),
        ("Crypto.MSOL/USD", "MSOLUSD"),
        ("Crypto.NEAR/USD", "NEARUSD"),
        ("Crypto.OG/USD", "OGUSD"),
        ("Crypto.ONE/USD", "ONEUSD"),
        ("Crypto.OP/USD", "OPUSD"),
        ("Crypto.ORCA/USD", "ORCAUSD"),
        ("Crypto.PERP/USD", "PERPUSD"),
        ("Crypto.PORT/USD", "PORTUSD"),
        ("Crypto.PORTO/USD", "PORTOUSD"),
        ("Crypto.PSG/USD", "PSGUSD"),
        ("Crypto.RAY/USD", "RAYUSD"),
        ("Crypto.SBR/USD", "SBRUSD"),
        ("Crypto.SCNSOL/USD", "SCNSOLUSD"),
        ("Crypto.SHIB/USD", "SHIBUSD"),
        ("Crypto.SLND/USD", "SLNDUSD"),
        ("Crypto.SNY/USD", "SNYUSD"),
        ("Crypto.SOL/USD", "SOLUSD"),
        ("Crypto.SRM/USD", "SRMUSD"),
        ("Crypto.STSOL/USD", "STSOLUSD"),
        ("Crypto.SWEAT/USD", "SWEATUSD"),
        ("Crypto.THETA/USD", "THETAUSD"),
        ("Crypto.TUSD/USD", "TUSDUSD"),
        ("Crypto.UNI/USD", "UNIUSD"),
        ("Crypto.USDC/USD", "USDCUSD"),
        ("Crypto.USDT/USD", "USDTUSD"),
        ("Crypto.USTC/USD", "USTCUSD"),
        ("Crypto.WOO/USD", "WOOUSD"),
        ("Crypto.XMR/USD", "XMRUSD"),
        ("Crypto.XVS/USD", "XVSUSD"),
        ("Crypto.ZBC/USD", "ZBCUSD"),
        ("Crypto.XRP/USD", "XRPUSD"),
        ("Crypto.TON/USD", "TONUSD"),
        ("FX.AUD/USD", "AUDUSD"),
        ("FX.EUR/USD", "EURUSD"),
        ("FX.GBP/USD", "GBPUSD"),
        ("FX.NZD/USD", "NZDUSD"),
        ("FX.USD/CAD", "USDCAD"),
        ("FX.USD/CHF", "USDCHF"),
        ("FX.USD/CNH", "USDCNH"),
        ("FX.USD/HKD", "USDHKD"),
        ("FX.USD/JPY", "USDJPY"),
        ("FX.USD/MXN", "USDMXN"),
        ("FX.USD/SGD", "USDSGD"),
        ("FX.USD/ZAR", "USDZAR"),
        ("Metal.XAG/USD", "XAGUSD"),
        ("Metal.XAU/USD", "XAUUSD"),
    ]
)


SYMBOL_PYTH_MAPPING = {v: k for k, v in PYTH_SYMBOL_MAPPING.items()}
