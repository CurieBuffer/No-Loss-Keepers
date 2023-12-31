from enum import Enum

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


SYMBOL_PYTH_MAPPING = {k: v for k, v in PYTH_SYMBOL_MAPPING.items()}

PYTH_FEED_ID_MAPPING = dict(
    [
        (
            "Crypto.1INCH/USD",
            "0x63f341689d98a12ef60a5cff1d7f85c70a9e17bf1575f0e7c0b2512d48b1c8b3",
        ),
        (
            "Crypto.AAVE/USD",
            "0x2b9ab1e972a281585084148ba1389800799bd4be63b957507db1349314e47445",
        ),
        (
            "Crypto.ACM/USD",
            "0xbd640cddb72063e2ede34c6a0baf6699759b9837fcb06aa0e2fbcecb9b65fde7",
        ),
        (
            "Crypto.ADA/USD",
            "0x2a01deaec9e51a579277b34b122399984d0bbf57e2458a7e42fecd2829867a0d",
        ),
        (
            "Crypto.ALGO/USD",
            "0xfa17ceaf30d19ba51112fdcc750cc83454776f47fb0112e4af07f15f4bb1ebc0",
        ),
        (
            "Crypto.ALICE/USD",
            "0xccca1d2b0d9a9ca72aa2c849329520a378aea0ec7ef14497e67da4050d6cf578",
        ),
        (
            "Crypto.ALPACA/USD",
            "0x9095653620547ece988ec51486dc7a6eb2efddbce8ea5bedbd53bf00cca84cf6",
        ),
        (
            "Crypto.AMP/USD",
            "0xd37e4513ebe235fff81e453d400debaf9a49a5df2b7faa11b3831d35d7e72cb7",
        ),
        (
            "Crypto.ANKR/USD",
            "0x89a58e1cab821118133d6831f5018fba5b354afb78b2d18f575b3cbf69a4f652",
        ),
        (
            "Crypto.APE/USD",
            "0x15add95022ae13563a11992e727c91bdb6b55bc183d9d747436c80a483d8c864",
        ),
        (
            "Crypto.APT/USD",
            "0x03ae4db29ed4ae33d323568895aa00337e658e348b37509f5372ae51f0af00d5",
        ),
        (
            "Crypto.ARB/USD",
            "0x3fa4252848f9f0a1480be62745a4629d9eb1322aebab8a791e344b3b9c1adcf5",
        ),
        (
            "Crypto.ARG/USD",
            "0x2394ce86c7d68050ce52797923860f6c1656a73fb11bd10dacb3f9c719acdd1d",
        ),
        (
            "Crypto.ASR/USD",
            "0xb881c6dad5dd3dc9a83222f8032fb439859288119afc742d43adc305cef151cc",
        ),
        (
            "Crypto.ATLAS/USD",
            "0x681e0eb7acf9a2a3384927684d932560fb6f67c6beb21baa0f110e993b265386",
        ),
        (
            "Crypto.ATM/USD",
            "0x8ff1200345393bb25be4f4eeb2d97234e91f7e6213f3745a694b1436e700f271",
        ),
        (
            "Crypto.ATOM/USD",
            "0xb00b60f88b03a6a625a8d1c048c3f66653edf217439983d037e7222c4e612819",
        ),
        (
            "Crypto.AURORA/USD",
            "0x2f7c4f738d498585065a4b87b637069ec99474597da7f0ca349ba8ac3ba9cac5",
        ),
        (
            "Crypto.AUTO/USD ",
            "0xc7c60099c12805bea1ae4df2243d6fe72b63be3adeb2208195e844734219967b",
        ),
        (
            "Crypto.AVAX/USD",
            "0x93da3352f9f1d105fdfe4971cfa80e9dd777bfc5d0f683ebb6e1294b92137bb7",
        ),
        (
            "Crypto.AXS/USD",
            "0xb7e3904c08ddd9c0c10c6d207d390fd19e87eb6aab96304f571ed94caebdefa0",
        ),
        (
            "Crypto.BAL/USD ",
            "0x07ad7b4a7662d19a6bc675f6b467172d2f3947fa653ca97555a9b20236406628",
        ),
        (
            "Crypto.BANANA/USD ",
            "0x909062e999977099a38fe13f6b691cc541d5378e49ca31880add229570506be2",
        ),
        (
            "Crypto.BAR/USD",
            "0x9d23a47f843f5c9284832ae6e76e4aa067dc6072a58f151d39a65a4cc792ef9f",
        ),
        (
            "Crypto.BAT/USD ",
            "0x8e860fb74e60e5736b455d82f60b3728049c348e94961add5f961b02fdee2535",
        ),
        (
            "Crypto.BCH/USD",
            "0x3dd2b63686a450ec7290df3a1e0b583c0481f651351edfa7636f39aed55cf8a3",
        ),
        (
            "Crypto.BETH/USD",
            "0x7f981f906d7cfe93f618804f1de89e0199ead306edc022d3230b3e8305f391b0",
        ),
        (
            "Crypto.BIFI/USD ",
            "0x70cd05521e3bdeaee2cadc1360f0d95397f03275f273199be35a029114f53a3b",
        ),
        (
            "Crypto.BIT/USD",
            "0x70ab610e3ed6642875f4a259dc29175452733316fee440f23fed99154d1d84f7",
        ),
        (
            "Crypto.BLUR/USD",
            "0x856aac602516addee497edf6f50d39e8c95ae5fb0da1ed434a8c2ab9c3e877e9",
        ),
        (
            "Crypto.BNB/USD",
            "0x2f95862b045670cd22bee3114c39763a4a08beeb663b145d283c31d7d1101c4f",
        ),
        (
            "Crypto.BNX/USD",
            "0x59671f59d12dc81bae078754b7469c7434528a66d3fa91193cf204460c198f9b",
        ),
        (
            "Crypto.BONK/USD",
            "0x72b021217ca3fe68922a19aaf990109cb9d84e9ad004b4d2025ad6f529314419",
        ),
        (
            "Crypto.BRZ/USD ",
            "0x1ce9069708fb49e2f1b062fa4f1be0bb151475ca506939d6d8c14386d49f43dc",
        ),
        (
            "Crypto.BSW/USD ",
            "0x48ce0cf436bac22dad33551dfe2eb7bf9991e419a05f25aed4e90c29c3a1cdbe",
        ),
        (
            "Crypto.BTC/USD",
            "0xe62df6c8b4a85fe1a67db44dc12de5db330f7ac66b72dc658afedf0f4a415b43",
        ),
        (
            "Crypto.BTT/USD ",
            "0x097d687437374051c75160d648800f021086bc8edf469f11284491fda8192315",
        ),
        (
            "Crypto.BUSD/USD",
            "0x5bc91f13e412c07599167bae86f07543f076a638962b8d6017ec19dab4a82814",
        ),
        (
            "Crypto.C98/USD",
            "0x2dd14c7c38aa7066c7a508aac299ebcde5165b07d5d9f2d94dfbfe41f0bc5f2e",
        ),
        (
            "Crypto.CAKE/USD",
            "0x2356af9529a1064d41e32d617e2ce1dca5733afa901daba9e2b68dee5d53ecf9",
        ),
        (
            "Crypto.CANTO/USD ",
            "0x972776d57490d31c32279c16054e5c01160bd9a2e6af8b58780c82052b053549",
        ),
        (
            "Crypto.CBETH/USD",
            "0x15ecddd26d49e1a8f1de9376ebebc03916ede873447c1255d2d5891b92ce5717",
        ),
        (
            "Crypto.CELO/USD",
            "0x7d669ddcdd23d9ef1fa9a9cc022ba055ec900e91c4cb960f3c20429d4447a411",
        ),
        (
            "Crypto.CFX/USD ",
            "0x8879170230c9603342f3837cf9a8e76c61791198fb1271bb2552c9af7b33c933",
        ),
        (
            "Crypto.CHR/USD",
            "0xbd4dbcbfd90e6bc6c583e07ffcb5cb6d09a0c7b1221805211ace08c837859627",
        ),
        (
            "Crypto.CHZ/USD",
            "0xe799f456b358a2534aa1b45141d454ac04b444ed23b1440b778549bb758f2b5c",
        ),
        (
            "Crypto.CITY/USD",
            "0x9c479b12a2b2c1051715d4d462dd7a6abbb6dccabf3af31a53f6130a1cd88efc",
        ),
        (
            "Crypto.COW/USD ",
            "0x4e53c6ef1f2f9952facdcf64551edb6d2a550985484ccce6a0477cae4c1bca3e",
        ),
        (
            "Crypto.CRO/USD",
            "0x23199c2bcb1303f667e733b9934db9eca5991e765b45f5ed18bc4b231415f2fe",
        ),
        (
            "Crypto.CRV/USD",
            "0xa19d04ac696c7a6616d291c7e5d1377cc8be437c327b75adb5dc1bad745fcae8",
        ),
        (
            "Crypto.CUSD/USD",
            "0x8f218655050a1476b780185e89f19d2b1e1f49e9bd629efad6ac547a946bf6ab",
        ),
        (
            "Crypto.CVX/USD",
            "0x6aac625e125ada0d2a6b98316493256ca733a5808cd34ccef79b0e28c64d1e76",
        ),
        (
            "Crypto.DAI/USD",
            "0xb0948a5e5313200c632b51bb5ca32f6de0d36e9950a942d19751e833f70dabfd",
        ),
        (
            "Crypto.DAR/USD ",
            "0xd57d90cd8554ea0cf8268de30d5ad67fed9a8f11cce5132a49eb687aed832ea6",
        ),
        (
            "Crypto.DOGE/USD",
            "0xdcef50dd0a4cd2dcc17e45df1676dcb336a11a61c69df7a0299b0150c672d25c",
        ),
        (
            "Crypto.DOT/USD",
            "0xca3eed9b267293f6595901c734c7525ce8ef49adafe8284606ceb307afa2ca5b",
        ),
        (
            "Crypto.DYDX/USD",
            "0x6489800bb8974169adfe35937bf6736507097d13c190d760c557108c7e93a81b",
        ),
        (
            "Crypto.ETH/USD",
            "0xff61491a931112ddf1bd8147cd1b641375f79f5825126d665480874634fd0ace",
        ),
        (
            "Crypto.EVMOS/USD ",
            "0xc19405e4c8bdcbf2a66c37ae05a27d385c8309e9d648ed20dc6ee717e7d30e17",
        ),
        (
            "Crypto.FET/USD",
            "0xb98e7ae8af2d298d2651eb21ab5b8b5738212e13efb43bd0dfbce7a74ba4b5d0",
        ),
        (
            "Crypto.FIDA/USD",
            "0xc80657b7f6f3eac27218d09d5a4e54e47b25768d9f5e10ac15fe2cf900881400",
        ),
        (
            "Crypto.FIL/USD",
            "0x150ac9b959aee0051e4091f0ef5216d941f590e1c5e7f91cf7635b5c11628c0e",
        ),
        (
            "Crypto.FLOKI/USD",
            "0x6b1381ce7e874dc5410b197ac8348162c0dd6c0d4c9cd6322672d6c2b1d58293",
        ),
        (
            "Crypto.FLOW/USD",
            "0x2fb245b9a84554a0f15aa123cbb5f64cd263b59e9a87d80148cbffab50c69f30",
        ),
        (
            "Crypto.FRAX/USD ",
            "0xc3d5d8d6d17081b3d0bbca6e2fa3a6704bb9a9561d9f9e1dc52db47629f862ad",
        ),
        (
            "Crypto.FTM/USD",
            "0x5c6c0d2386e3352356c3ab84434fafb5ea067ac2678a38a338c4a69ddc4bdb0c",
        ),
        (
            "Crypto.FTT/USD",
            "0x6c75e52531ec5fd3ef253f6062956a8508a2f03fa0a209fb7fbc51efd9d35f88",
        ),
        (
            "Crypto.FXS/USD",
            "0x735f591e4fed988cd38df74d8fcedecf2fe8d9111664e0fd500db9aa78b316b1",
        ),
        (
            "Crypto.GAL/USD",
            "0x301377b122716cee1a498e7930a1836c0b1db84667cc78bbbcbad6c330ea6afb",
        ),
        (
            "Crypto.GALA/USD",
            "0x0781209c28fda797616212b7f94d77af3a01f3e94a5d421760aef020cf2bcb51",
        ),
        (
            "Crypto.GMT/USD",
            "0xbaa284eaf23edf975b371ba2818772f93dbae72836bbdea28b07d40f3cf8b485",
        ),
        (
            "Crypto.GMX/USD",
            "0xb962539d0fcb272a494d65ea56f94851c2bcf8823935da05bd628916e2e9edbf",
        ),
        (
            "Crypto.GNS/USD ",
            "0x5a5d5f7fb72cc84b579d74d1c06d258d751962e9a010c0b1cce7e6023aacb71b",
        ),
        (
            "Crypto.GOFX/USD ",
            "0x6034b1f68b9363dff2cf9d53b1a88fb4d0929c65f34d532db53738853efc00ad",
        ),
        (
            "Crypto.HADES/USD ",
            "0x07a8f31e8910c3b52f338d2aca6f4dc2404753ebafcdf53290ef4993911a71f8",
        ),
        (
            "Crypto.HAY/USD ",
            "0x4176cd17d4a1fb517b6535e70084ce85e1bcbe707c66b960c8bd5256accc1b2d",
        ),
        (
            "Crypto.HFT/USD ",
            "0xfa2d39b681f3cef5fa87432a8dbd05113917fffb1b6829a37395c88396522a4e",
        ),
        (
            "Crypto.HNT/USD ",
            "0x649fdd7ec08e8e2a20f425729854e90293dcbe2376abc47197a14da6ff339756",
        ),
        (
            "Crypto.HXRO/USD ",
            "0x95609d32c98a467a72ac419f2e64bb2b8dbd5b00b74f3a0fd72f42343af1743d",
        ),
        (
            "Crypto.INJ/USD",
            "0x7a5bc1d2b56ad029048cd63964b3ad2776eadf812edc1a43a31406cb54bff592",
        ),
        (
            "Crypto.INTER/USD",
            "0xa4702f0f5818258783a1e47f453cb20b0fbec32ca67260e1d19dfcdd6a4d0ebb",
        ),
        (
            "Crypto.IOTA/USD ",
            "0xc7b72e5d860034288c9335d4d325da4272fe50c92ab72249d58f6cbba30e4c44",
        ),
        (
            "Crypto.ITA/USD",
            "0xa5eb88d3ea93f6240d7e54b4466bc1857f7bfc1658d49a07f68096ebc0fdde3b",
        ),
        (
            "Crypto.JET/USD ",
            "0x81a21b01c15b8d01f6cdfed65e00987cc4c901858c821b2089344987de3102e9",
        ),
        (
            "Crypto.JITOSOL/USD ",
            "0x67be9f519b95cf24338801051f9a808eff0a578ccb388db73b7f6fe1de019ffb",
        ),
        (
            "Crypto.JST/USD",
            "0xee42016c303126bd9263724e00f83a8114e84518c6e8ffc9738c001cc301daff",
        ),
        (
            "Crypto.JUV/USD",
            "0xabe4f2b264560a397f38eec024369356e5c1ea4f7aab94729369f144b3d97779",
        ),
        (
            "Crypto.KCS/USD ",
            "0xc8acad81438490d4ebcac23b3e93f31cdbcb893fcba746ea1c66b89684faae2f",
        ),
        (
            "Crypto.LAZIO/USD",
            "0xd1d95644ffc11ca502f21e067a7814144c56b37018515ced4335a886a827a305",
        ),
        (
            "Crypto.LDO/USD",
            "0xc63e2a7f37a04e5e614c07238bedb25dcc38927fba8fe890597a593c0b2fa4ad",
        ),
        (
            "Crypto.LINK/USD",
            "0x8ac0c70fff57e9aefdf5edf44b51d62c2d433653cbb2cf5cc06bb115af04d221",
        ),
        (
            "Crypto.LTC/USD",
            "0x6e3f3fa8253588df9326580180233eb791e03b443a3ba7a1d892e73874e19a54",
        ),
        (
            "Crypto.LUNA/USD",
            "0xe6ccd3f878cf338e6732bf59f60943e8ca2c28402fc4d9c258503b2edbe74a31",
        ),
        (
            "Crypto.LUNC/USD",
            "0x4456d442a152fd1f972b18459263ef467d3c29fb9d667e30c463b086691fbc79",
        ),
        (
            "Crypto.MATIC/USD",
            "0x5de33a9112c2b700b8d30b8a3402c103578ccfa2765696471cc672bd5cf6ac52",
        ),
        (
            "Crypto.MBOX/USD",
            "0x1888f463c27997174f97d2a36af29bf4648b61a5f69e67c45505a80f826bb785",
        ),
        (
            "Crypto.MDX/USD ",
            "0x3b4656b0d92f0e995024c3dacfc28c47d11af83b374a56c26e514e9a7e46a240",
        ),
        (
            "Crypto.MEAN/USD ",
            "0x27d108eb764c912f49d3453a21dd95516619b1c45d0b607ee58a137ac8a6f32d",
        ),
        (
            "Crypto.MIR/USD",
            "0x0b46c1c04e9c914037cc4e0561a7e6787f6db0b89b7b65281f0f6fea1ce45a74",
        ),
        (
            "Crypto.MNGO/USD",
            "0x5b70af49d639eefe11f20df47a0c0760123291bb5bc55053faf797d1ff905983",
        ),
        (
            "Crypto.MSOL/USD",
            "0xc2289a6a43d2ce91c6f55caec370f4acc38a2ed477f58813334c6d03749ff2a4",
        ),
        (
            "Crypto.MTR/USD ",
            "0x8cdc9b2118d2ce55a299f8f1d700d0127cf4036d1aa666a8cd51dcab4254284f",
        ),
        (
            "Crypto.MTRG/USD ",
            "0x20d096e088a9b85f8cf09278965b77aeb05c00769e2ddeda5ea2d07ea554b283",
        ),
        (
            "Crypto.NEAR/USD",
            "0xc415de8d2eba7db216527dff4b60e8f3a5311c740dadb233e13e12547e226750",
        ),
        (
            "Crypto.NFT/USD ",
            "0xd64da7f265f00c456c2ebadf4593848129b9c86b45523e441d2f5ceb838a89cf",
        ),
        (
            "Crypto.OG/USD",
            "0x05934526b94a9fbe4c4ce0c3792213032f086ee4bf58f2168a7085361af9bdc1",
        ),
        (
            "Crypto.OMI/USD ",
            "0x06d9fa501fd2bef47265361ca0eaf6e0a97c3b226cea5ab760240f70818581ad",
        ),
        (
            "Crypto.ONE/USD",
            "0xc572690504b42b57a3f7aed6bd4aae08cbeeebdadcf130646a692fe73ec1e009",
        ),
        (
            "Crypto.OP/USD",
            "0x385f64d993f7b77d8182ed5003d97c60aa3361f3cecfe711544d2d59165e9bdf",
        ),
        (
            "Crypto.ORCA/USD",
            "0x37505261e557e251290b8c8899453064e8d760ed5c65a779726f2490980da74c",
        ),
        (
            "Crypto.OSMO/USD",
            "0x5867f5683c757393a0670ef0f701490950fe93fdb006d181c8265a831ac0c5c6",
        ),
        (
            "Crypto.PERP/USD",
            "0x944f2f908c5166e0732ea5b610599116cd8e1c41f47452697c1e84138b7184d6",
        ),
        (
            "Crypto.PINKSALE/USD ",
            "0x5f1b1a2920f29635157c1733163f832e35ea5ebaf27552e5106b2f5596f5dd26",
        ),
        (
            "Crypto.POR/USD ",
            "0x701223c92a39dbab065c4a7997fef9c41c8de26ca2bf1f808ce0a4ea1cfd421f",
        ),
        (
            "Crypto.PORT/USD",
            "0x0afa3199e0899270a74ddcf5cc960d3c6c4414b4ca71024af1a62786dd24f52a",
        ),
        (
            "Crypto.PORTO/USD",
            "0x88e2d5cbd2474766abffb2a67a58755a2cc19beb3b309e1ded1e357253aa3623",
        ),
        (
            "Crypto.PSG/USD",
            "0x3d253019d38099c0fe918291bd08c9b887f4306a44d7d472c8031529141f275a",
        ),
        (
            "Crypto.RACA/USD ",
            "0xfd0690232b0fae5efdc402c1b9aac74176383ff7daf87d021554bda24a38e0ec",
        ),
        (
            "Crypto.RAY/USD",
            "0x91568baa8beb53db23eb3fb7f22c6e8bd303d103919e19733f2bb642d3e7987a",
        ),
        (
            "Crypto.RETH/USD ",
            "0xa0255134973f4fdf2f8f7808354274a3b1ebc6ee438be898d045e8b56ba1fe13",
        ),
        (
            "Crypto.RLB/USD ",
            "0x2f2d17abbc1e781bd87b4a5d52c8b2856886f5c482fa3593cebf6795040ab0b6",
        ),
        (
            "Crypto.SAMO/USD ",
            "0x49601625e1a342c1f90c3fe6a03ae0251991a1d76e480d2741524c29037be28a",
        ),
        (
            "Crypto.SANTOS/USD",
            "0x26d53c97247ec18d576bbd23f88078acc22b42168dcb1d29a76501a956e26bad",
        ),
        (
            "Crypto.SBR/USD",
            "0x6ed3c7c4427ae2f91707495fc5a891b30795d93dbb3931782ddd77a5d8cb6db7",
        ),
        (
            "Crypto.SCNSOL/USD",
            "0x1021a42d623ab4fe0bf8c47fd21cc10636e39e07f91e9b2478551e137d512aaa",
        ),
        (
            "Crypto.SFP/USD ",
            "0xc9e9d228f565c226dfb8ed5f5c9c4f57ab32b7ade7226c3239ff20911a9c3a7b",
        ),
        (
            "Crypto.SHIB/USD",
            "0xf0d57deca57b3da2fe63a493f4c25925fdfd8edf834b20f93e1f84dbd1504d4a",
        ),
        (
            "Crypto.SLND/USD",
            "0xf8d030e4ef460b91ad23eabbbb27aec463e3c30ecc8d5c4b71e92f54a36ccdbd",
        ),
        (
            "Crypto.SMR/USD ",
            "0xaf5b9ac426ae79591fde6816bc3f043b5e06d5e442f52112f76249320df22449",
        ),
        (
            "Crypto.SNX/USD",
            "0x39d020f60982ed892abbcd4a06a276a9f9b7bfbce003204c110b6e488f502da3",
        ),
        (
            "Crypto.SNY/USD",
            "0x9fb0bd29fe51481b61df41e650346cc374b13c2bab2e3610364cd834a592025a",
        ),
        (
            "Crypto.SOL/USD",
            "0xef0d8b6fda2ceba41da15d4095d1da392a0d2f8ed0c6c7bc0f4cfac8c280b56d",
        ),
        (
            "Crypto.SPELL/USD ",
            "0x1dcf38b0206d27849b0fcb8d2df21aff4f95873cce223f49d7c1ea3c5145ec63",
        ),
        (
            "Crypto.SRM/USD",
            "0x23245bb74254e65a98cc3ff4a37443d79f527e44e449750ad304538b006f21bc",
        ),
        (
            "Crypto.STETH/USD ",
            "0x846ae1bdb6300b817cee5fdee2a6da192775030db5615b94a465f53bd40850b5",
        ),
        (
            "Crypto.STNEAR/USD ",
            "0x956740a4e169e90bb141abfe93652ae3434693bc7ca43cbcea6471408f19ab90",
        ),
        (
            "Crypto.STRK/USD ",
            "0xaaebacfd60ca9d621ff304b79e7d6c7c392a66617479c4898f1f8543d2531331",
        ),
        (
            "Crypto.STSOL/USD",
            "0xa1a6465f4c2ebf244c31d80bc95c27345a3424e428c2def33eced9e90d3f701b",
        ),
        (
            "Crypto.SUN/USD ",
            "0x159b09ed169a3cdbd13fd96ef4b3cda54972058906d38a58f5cd327e5df1478b",
        ),
        (
            "Crypto.SWEAT/USD",
            "0x432a52bde005a010dc32c47733e4595fea0ea04df3b5aaa1c45153a527d646f0",
        ),
        (
            "Crypto.TAPT/USD ",
            "0x5c2416ad4b5fe25c38ea2078927d59dad6a1d4110480c0c96c9b4421744f7507",
        ),
        (
            "Crypto.THETA/USD",
            "0xee70804471fe22d029ac2d2b00ea18bbf4fb062958d425e5830fd25bed430345",
        ),
        (
            "Crypto.THG/USD ",
            "0xa639c04942ebfdeabf25bf1b88d6608ef387219748d77ea130bc2fa486b9614f",
        ),
        (
            "Crypto.TLM/USD ",
            "0x4457960559b812558bb0f8cb7912f8bcb843eb801a3133ef45be998630ff8c05",
        ),
        (
            "Crypto.TUSD/USD",
            "0x433faaa801ecdb6618e3897177a118b273a8e18cc3ff545aadfc207d58d028f7",
        ),
        (
            "Crypto.TWT/USD ",
            "0x35f1e0d9248599d276111821c0fd636b43eef18737c3bb61c7c5c47059787a32",
        ),
        (
            "Crypto.UNI/USD",
            "0x78d185a741d07edb3412b09008b7c5cfb9bbbd7d568bf00ba737b456ba171501",
        ),
        (
            "Crypto.USDC/USD",
            "0xeaa020c61cc479712813461ce153894a96a6c00b21ed0cfc2798d1f9a9e9c94a",
        ),
        (
            "Crypto.USDD/USD ",
            "0x6d20210495d6518787b72e4ad06bc4df21e68d89a802cf6bced2fca6c29652a6",
        ),
        (
            "Crypto.USDT/USD",
            "0x2b89b9dc8fdf9f34709a5b106b472f0f39bb6ca9ce04b0fd7f2e971688e2e53b",
        ),
        (
            "Crypto.USTC/USD",
            "0xef94acc2fb09eb976c6eb3000bab898cab891d5b800702cd1dc88e61d7c3c5e6",
        ),
        (
            "Crypto.VAI/USD ",
            "0x7507a4629ad0143550666bce2e7cae0b961a0f624f821feaab642fe1be632f5c",
        ),
        (
            "Crypto.WIN/USD ",
            "0xb216f7ca372b318985903866e0b6dc44a14564828c49f36d0d363805aa76335c",
        ),
        (
            "Crypto.WOM/USD ",
            "0x43cddc3e1d0b17fec1cf2a230f46e9319887a037dcee56e053af44d8259fb042",
        ),
        (
            "Crypto.WOO/USD",
            "0xb82449fd728133488d2d41131cffe763f9c1693b73c544d9ef6aaa371060dd25",
        ),
        (
            "Crypto.XMR/USD",
            "0x46b8cc9347f04391764a0361e0b17c3ba394b001e7c304f7650f6376e37c321d",
        ),
        (
            "Crypto.XRP/USD ",
            "0xec5d399846a9209f3fe5881d70aae9268c94339ff9817e8d18ff19fa05eea1c8",
        ),
        (
            "Crypto.XVS/USD",
            "0x831624f51c7bd4499fe5e0f16dfa2fd22584ae4bdc496bbbbe9ba831b2d9bce9",
        ),
        (
            "Crypto.XWG/USD ",
            "0x83a6de4ec10bce1c0515d1aac082fd193f268f0c3b62da0c8ed1286319272415",
        ),
        (
            "Crypto.ZBC/USD",
            "0x26852e2d0696e25e6adaad2d7ca3a1f2f15aab68d317ace14d41b4128a7e780f",
        ),
        (
            "Equity.GB.CSPX/USD ",
            "0x6d881ecf489bb24aa10468ca332e3ea262a9bf3a8fb9db1eadac9cce544b16b1",
        ),
        (
            "Equity.GB.IB01/USD ",
            "0x45b05d03edb6081e7ae536b94b450a42f43e6342791c560a481030b41f9b945d",
        ),
        (
            "Equity.GB.IBTA/USD ",
            "0x8086320540b3d7b9b4b564e6756a29a9cb91a7cd97d5fafff63841959d3a09a0",
        ),
        (
            "Equity.US.AAPL/USD",
            "0x49f6b65cb1de6b10eaf75e7c03ca029c306d0357e91b5311b175084a5ad55688",
        ),
        (
            "Equity.US.AMC/USD",
            "0x5b1703d7eb9dc8662a61556a2ca2f9861747c3fc803e01ba5a8ce35cb50a13a1",
        ),
        (
            "Equity.US.AMGN/USD",
            "0x10946973bfcc936b423d52ee2c5a538d96427626fe6d1a7dae14b1c401d1e794",
        ),
        (
            "Equity.US.AMZN/USD",
            "0xb5d0e0fa58a1f8b81498ae670ce93c872d14434b72c364885d4fa1b257cbb07a",
        ),
        (
            "Equity.US.AXP/USD",
            "0x9ff7b9a93df40f6d7edc8184173c50f4ae72152c6142f001e8202a26f951d710",
        ),
        (
            "Equity.US.BA/USD",
            "0x8419416ba640c8bbbcf2d464561ed7dd860db1e38e51cec9baf1e34c4be839ae",
        ),
        (
            "Equity.US.CAT/USD",
            "0xad04597ba688c350a97265fcb60585d6a80ebd37e147b817c94f101a32e58b4c",
        ),
        (
            "Equity.US.COIN/USD ",
            "0xfee33f2a978bf32dd6b662b65ba8083c6773b494f8401194ec1870c640860245",
        ),
        (
            "Equity.US.CRM/USD",
            "0xfeff234600320f4d6bb5a01d02570a9725c1e424977f2b823f7231e6857bdae8",
        ),
        (
            "Equity.US.CSCO/USD",
            "0x3f4b77dd904e849f70e1e812b7811de57202b49bc47c56391275c0f45f2ec481",
        ),
        (
            "Equity.US.CVX/USD",
            "0xf464e36fd4ef2f1c3dc30801a9ab470dcdaaa0af14dd3cf6ae17a7fca9e051c5",
        ),
        (
            "Equity.US.DIS/USD",
            "0x703e36203020ae6761e6298975764e266fb869210db9b35dd4e4225fa68217d0",
        ),
        (
            "Equity.US.DOW/USD",
            "0xf3b50961ff387a3d68217e2715637d0add6013e7ecb83c36ae8062f97c46929e",
        ),
        (
            "Equity.US.EFA/USD ",
            "0x3b7ef6c95ceedbffbb66bff3d6135a200c5d0a0466b0c90812510ceaedebaf04",
        ),
        (
            "Equity.US.GE/USD",
            "0xe1d3115c6e7ac649faca875b3102f1000ab5e06b03f6903e0d699f0f5315ba86",
        ),
        (
            "Equity.US.GME/USD",
            "0x6f9cd89ef1b7fd39f667101a91ad578b6c6ace4579d5f7f285a4b06aa4504be6",
        ),
        (
            "Equity.US.GOOG/USD",
            "0xe65ff435be42630439c96396653a342829e877e2aafaeaf1a10d0ee5fd2cf3f2",
        ),
        (
            "Equity.US.GOVT/USD ",
            "0xe0f87bbde799f33615b83a601b66415e850788000cd7286a3e7295f23c1bb353",
        ),
        (
            "Equity.US.GS/USD",
            "0x9c68c0c6999765cf6e27adf75ed551b34403126d3b0d5b686a2addb147ed4554",
        ),
        (
            "Equity.US.HD/USD",
            "0xb3a83dbe70b62241b0f916212e097465a1b31085fa30da3342dd35468ca17ca5",
        ),
        (
            "Equity.US.HON/USD",
            "0x107918baaaafb79cd9df1c8369e44ac21136d95f3ca33f2373b78f24ba1e3e6a",
        ),
        (
            "Equity.US.HYG/USD ",
            "0x2077043ee3b67b9a70949c8396c110f6cf43de8e6d9e6efdcbd557a152cf2c6e",
        ),
        (
            "Equity.US.IBM/USD",
            "0xcfd44471407f4da89d469242546bb56f5c626d5bef9bd8b9327783065b43c3ef",
        ),
        (
            "Equity.US.INTC/USD",
            "0xc1751e085ee292b8b3b9dd122a135614485a201c35dfc653553f0e28c1baf3ff",
        ),
        (
            "Equity.US.IVV/USD ",
            "0x5967c196ca33171a0b2d140ddc6334b998dd71c2ddd85ba7920c35fd6ed20fe9",
        ),
        (
            "Equity.US.IWM/USD ",
            "0xeff690a187797aa225723345d4612abec0bf0cec1ae62347c0e7b1905d730879",
        ),
        (
            "Equity.US.JNJ/USD",
            "0x12848738d5db3aef52f51d78d98fc8b8b8450ffb19fb3aeeb67d38f8c147ff63",
        ),
        (
            "Equity.US.JPM/USD",
            "0x7f4f157e57bfcccd934c566df536f34933e74338fe241a5425ce561acdab164e",
        ),
        (
            "Equity.US.KO/USD",
            "0x9aa471dccea36b90703325225ac76189baf7e0cc286b8843de1de4f31f9caa7d",
        ),
        (
            "Equity.US.MCD/USD",
            "0xd3178156b7c0f6ce10d6da7d347952a672467b51708baaf1a57ffe1fb005824a",
        ),
        (
            "Equity.US.META/USD ",
            "0x78a3e3b8e676a8f73c439f5d749737034b139bbbe899ba5775216fba596607fe",
        ),
        (
            "Equity.US.MINT/USD ",
            "0x58f4ee3a0fc4de834a2e96274a696d0f3d8ec45fc76131a6a49fcd18d3ca9812",
        ),
        (
            "Equity.US.MMM/USD",
            "0xfd05a384ba19863cbdfc6575bed584f041ef50554bab3ab482eabe4ea58d9f81",
        ),
        (
            "Equity.US.MRK/USD",
            "0xc81114e16ec3cbcdf20197ac974aed5a254b941773971260ce09e7caebd6af46",
        ),
        (
            "Equity.US.MSFT/USD",
            "0xd0ca23c1cc005e004ccf1db5bf76aeb6a49218f43dac3d4b275e92de12ded4d1",
        ),
        (
            "Equity.US.NFLX/USD",
            "0x8376cfd7ca8bcdf372ced05307b24dced1f15b1afafdeff715664598f15a3dd2",
        ),
        (
            "Equity.US.NKE/USD",
            "0x67649450b4ca4bfff97cbaf96d2fd9e40f6db148cb65999140154415e4378e14",
        ),
        (
            "Equity.US.PG/USD",
            "0xad2fda41998f4e7be99a2a7b27273bd16f183d9adfc014a4f5e5d3d6cd519bf4",
        ),
        (
            "Equity.US.QQQ/USD",
            "0x9695e2b96ea7b3859da9ed25b7a46a920a776e2fdae19a7bcfdf2b219230452d",
        ),
        (
            "Equity.US.SHV/USD ",
            "0x765f416f2d676848b5016428bc9295fda3e71d5e97b16df75179a378cef040ec",
        ),
        (
            "Equity.US.SPY/USD",
            "0x19e09bb805456ada3979a7d1cbb4b6d63babc3a0f8e8a9509f68afa5c4c11cd5",
        ),
        (
            "Equity.US.TLT/USD ",
            "0x9f383d612ac09c7e6ffda24deca1502fce72e0ba58ff473fea411d9727401cc1",
        ),
        (
            "Equity.US.TRV/USD",
            "0xd45392f678a1287b8412ed2aaa326def204a5c234df7cb5552d756c332283d81",
        ),
        (
            "Equity.US.TSLA/USD",
            "0x16dad506d7db8da01c87581c87ca897a012a153557d4d578c3b9c9e1bc0632f1",
        ),
        (
            "Equity.US.UNH/USD",
            "0x05380f8817eb1316c0b35ac19c3caa92c9aa9ea6be1555986c46dce97fed6afd",
        ),
        (
            "Equity.US.USO/USD ",
            "0xd00bd77d97dc5769de77f96d0e1a79cbf1364e14d0dbf046e221bce2e89710dd",
        ),
        (
            "Equity.US.V/USD",
            "0xc719eb7bab9b2bc060167f1d1680eb34a29c490919072513b545b9785b73ee90",
        ),
        (
            "Equity.US.VOO/USD ",
            "0x236b30dd09a9c00dfeec156c7b1efd646c0f01825a1758e3e4a0679e3bdff179",
        ),
        (
            "Equity.US.VZ/USD",
            "0x6672325a220c0ee1166add709d5ba2e51c185888360c01edc76293257ef68b58",
        ),
        (
            "Equity.US.WBA/USD",
            "0xed5c2a2711e2a638573add9a8aded37028aea4ac69f1431a1ced9d9db61b2225",
        ),
        (
            "Equity.US.WMT/USD",
            "0x327ae981719058e6fb44e132fb4adbf1bd5978b43db0661bfdaefd9bea0c82dc",
        ),
        (
            "Equity.US.XLE/USD ",
            "0x8bf649e08e5a86129c57990556c8eec30e296069b524f4639549282bc5c07bb4",
        ),
        (
            "FX.AUD/USD",
            "0x67a6f93030420c1c9e3fe37c1ab6b77966af82f995944a9fefce357a22854a80",
        ),
        (
            "FX.EUR/USD",
            "0xa995d00bb36a63cef7fd2c287dc105fc8f3d93779f062f09551b0af3e81ec30b",
        ),
        (
            "FX.GBP/USD",
            "0x84c2dde9633d93d1bcad84e7dc41c9d56578b7ec52fabedc1f335d673df0a7c1",
        ),
        (
            "FX.NZD/USD",
            "0x92eea8ba1b00078cdc2ef6f64f091f262e8c7d0576ee4677572f314ebfafa4c7",
        ),
        (
            "FX.USD/CAD",
            "0x3112b03a41c910ed446852aacf67118cb1bec67b2cd0b9a214c58cc0eaa2ecca",
        ),
        (
            "FX.USD/CHF",
            "0x0b1e3297e69f162877b577b0d6a47a0d63b2392bc8499e6540da4187a63e28f8",
        ),
        (
            "FX.USD/CNH",
            "0xeef52e09c878ad41f6a81803e3640fe04dceea727de894edd4ea117e2e332e66",
        ),
        (
            "FX.USD/HKD",
            "0x19d75fde7fee50fe67753fdc825e583594eb2f51ae84e114a5246c4ab23aff4c",
        ),
        (
            "FX.USD/JPY",
            "0xef2c98c804ba503c6a707e38be4dfbb16683775f195b091252bf24693042fd52",
        ),
        (
            "FX.USD/MXN",
            "0xe13b1c1ffb32f34e1be9545583f01ef385fde7f42ee66049d30570dc866b77ca",
        ),
        (
            "FX.USD/NOK ",
            "0x235ddea9f40e9af5814dbcc83a418b98e3ee8df1e34e1ae4d45cf5de596023a3",
        ),
        (
            "FX.USD/RUB",
            "0x2f6144bae52851efb91082911cb6b83f9d8d08cb6ace5625eaac26f638af710b",
        ),
        (
            "FX.USD/SEK ",
            "0x8ccb376aa871517e807358d4e3cf0bc7fe4950474dbe6c9ffc21ef64e43fc676",
        ),
        (
            "FX.USD/SGD",
            "0x396a969a9c1480fa15ed50bc59149e2c0075a72fe8f458ed941ddec48bdb4918",
        ),
        (
            "FX.USD/ZAR",
            "0x389d889017db82bf42141f23b61b8de938a4e2d156e36312175bebf797f493f1",
        ),
        (
            "Metal.XAG/USD",
            "0xf2fb02c32b055c805e7238d628e5e9dadef274376114eb1f012337cabe93871e",
        ),
        (
            "Metal.XAU/USD",
            "0x765d2ba906dbc32ca17cc11f5310a89e9ee1f6420508c63861f2f8ba4ee34bb2",
        ),
        (
            "Crypto.XRP/USD",
            "0xec5d399846a9209f3fe5881d70aae9268c94339ff9817e8d18ff19fa05eea1c8",
        ),
        (
            "Crypto.TON/USD",
            "0x8963217838ab4cf5cadc172203c1f0b763fbaa45f346d8ee50ba994bbcac3026",
        ),
    ]
)
FEED_ID_PYTH_SYMBOL_MAPPING = {
    SYMBOL_PYTH_MAPPING.get(k, ""): v for k, v in PYTH_FEED_ID_MAPPING.items()
}

ALL_PAIRS = list(PYTH_SYMBOL_MAPPING.values())
PairEnum = Enum("Pair", dict(zip(ALL_PAIRS, ALL_PAIRS)))
