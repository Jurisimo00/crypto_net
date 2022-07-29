import          os
from pathlib    import Path

coin_info_path = "./pages/coin_info.html"
buy_sell_path = "./pages/buysell.html"

coin_info_script="""
<script>
    window.onload = async() => {{
        path = "/coins/single?symbol={symbol}"

        document.getElementById("gotohomepage").onclick = () => {{
            window.location.href = "/"
        }}

        document.getElementById("trending").onclick = () => {{
            window.location.href = "/trending"
        }}

        document.getElementById("buysell").onclick = () => {{
            window.location.href = "/buysell?symbol={symbol}&coin_id={coin_id}"
        }}

        document.getElementById("userpage").onclick = () => {{
            window.location.href = "/userpage"
        }}

        await fetch(path, {{
            method: "GET"
        }}).then(async res => {{
            res = await res.json();
            document.getElementById("name").textContent = res.name + " (" + res.symbol.toUpperCase() + ")"
            document.getElementById("image").src = res.image.large
            document.getElementById("marketcap").textContent = "Market cap: $ " + res.market_data.market_cap.usd
            document.getElementById("marketcaprank").textContent = "Rank: " + res.market_data.market_cap_rank + "^ place"
            document.getElementById("currentprice").textContent = "Price: $ " + res.market_data.current_price.usd
            document.getElementById("repo").href = res.links.repos_url.github == "" ? "https://github.com" : res.links.repos_url.github[0]
            document.getElementById("homepage").href = res.links.homepage[0]
            document.getElementById("contract").textContent = res.contract_address
            document.getElementById("assetplatform").textContent = "Asset platform: " + res.asset_platform_id
            document.getElementById("description").textContent = "Description: " + res.description.en
        }})
    }}
</script>
"""
coin_info_head = """
<head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Prompt&display=swap');
        .title {
            font-size: 1.9rem;
        }
        
        .info_container {
            display: grid;
            grid-template-columns: 1fr 2fr;
            width: 65%;
            margin: 5em auto;
        }
        
        .info_sec {
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
            padding: 1em;
            height: 200px;
            color: black;
            background-color: white;
            box-shadow: white;
            border-radius: 1em;
            margin: .5em;
            display: inline;
        }
        
        .price_info {
            float: left;
        }
        
        .info_links {
            height: fit-content;
        }
        
        .info_chart {
            height: fit-content;
        }
        
        .info_prices {
            display: grid;
            grid-template-columns: 1fr 1fr;
        }
        
        .nav {
            background-color: rgb(136, 136, 136);
            display: inline-block;
            position: sticky;
            font-size: 1.2rem;
            padding-top: 2em;
            padding-bottom: 2em;
            margin-top: 2em;
            width: 100%;
        }
        
        .nav>div {
            background-color: rgb(64, 211, 51);
            display: inline;
            padding: .5em;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
            margin: 0 1em 0 1em;
            user-select: none;
            cursor: pointer;
        }

        .description {
            height: 100px;
            overflow-y: scroll;
        }
        
        .nav>div:hover {
            opacity: 0.7;
        }
        
        body,
        html {
            background-color: rgb(75, 75, 75);
            overflow-x: hidden;
            font-family: 'Prompt', sans-serif;
        }
        
        body {
            color: white;
            margin: 0;
            text-align: center;
        }
    </style>
</head>
"""

coin_info_body = """
<body>
    <div class="title">
        Crypto Network
    </div>

    <div class="nav">
        <div id="gotohomepage">Homepage</div>
        <div id="trending">Coins</div>
        <div id="buysell">Buy/Sell</div>
        <div id="userpage">Userpage</div>
    </div>

    <div class="info_container">
        <div id="logo" class="info_sec">
            <img height="150px" width="150px" id="image" src="" alt="">
            <p id="name">
            </p>
        </div>
        <div id="info" class="info_sec info_prices">
            <div id="priceinfo" class="price_info">
                <p id="marketcap"></p>
                <p id="marketcaprank"></p>
                <p id="currentprice"></p>
            </div>
            <div id="othersinfo" class="other_info">
                <label for="contract">Contract address</label>
                <p id="contract"></p>
                <p id="assetplatform"></p>
                <p id="description" class="description"></p>
            </div>
        </div>
        <div id="links" class="info_sec info_links">
            links:
            <div>
                <a id="homepage">website</a>
            </div>
            <div>
                <a id="repo">github link</a>
            </div>
        </div>
        <div id="links" class="info_sec info_chart">
            <script src="https://widgets.coingecko.com/coingecko-coin-price-chart-widget.js"></script>
            <coingecko-coin-price-chart-widget coin-id="{coin_id}" currency="usd" height="300" locale="en"></coingecko-coin-price-chart-widget>
        </div>
    </div>
</body>
"""

buy_sell_page = """
<html>

<head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Prompt&display=swap');
        .list_title {{
            margin: 2em;
            font-size: 1.5rem;
        }}
        
        .list_container {{
            margin-left: 20%;
            margin-right: 20%;
        }}
        
        .loading {{
            font-size: 1.5rem;
        }}
        
        .title {{
            font-size: 1.9rem;
        }}
        
        .buy,
        .sell {{
            width: 70%;
            margin: 3em auto;
        }}
        
        .buyvalues {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            padding: .5em;
        }}
        
        .mktbutton {{
            border-radius: .7em;
            cursor: pointer;
            background-color: white;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
            padding: .5em 2em .5em 2em;
            font-size: 1.4rem;
            appearance: none;
            outline: none;
            border: none;
        }}
        
        .mktinput {{
            text-align: center;
            margin: .5em;
            border-radius: .7em;
            background-color: white;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
            padding: .5em 2em .5em 2em;
            font-size: 1.4rem;
            appearance: none;
            outline: none;
            border: none;
        }}
        
        .nav {{
            background-color: rgb(136, 136, 136);
            display: inline-block;
            position: sticky;
            font-size: 1.2rem;
            padding-top: 2em;
            padding-bottom: 2em;
            margin-top: 2em;
            width: 100%;
        }}
        
        .nav>div {{
            background-color: rgb(64, 211, 51);
            display: inline;
            padding: .5em;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
            margin: 0 1em 0 1em;
            user-select: none;
            cursor: pointer;
        }}
        
        .nav>div:hover {{
            opacity: 0.7;
        }}
        
        .coin_container {{
            background-color: rgb(136, 136, 136);
            padding: 1em;
            margin-top: 1em;
            color: white;
            cursor: pointer;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
            display: grid;
            grid-template-columns: 1fr 1fr;
            user-select: none;
        }}
        
        .container_head {{
            background-color: transparent;
            color: white;
            box-shadow: none;
        }}
        
        .coin_container:hover {{
            opacity: 0.6;
        }}
        
        .container_head:hover {{
            opacity: 1.0;
            cursor: auto;
        }}
        
        body,
        html {{
            background-color: rgb(75, 75, 75);
            overflow-x: hidden;
            font-family: 'Prompt', sans-serif;
        }}
        
        body {{
            color: white;
            margin: 0;
            text-align: center;
        }}
    </style>
</head>

<body>
    <div class="title">
        Crypto Network
    </div>

    <div class="nav">
        <div id="gotohomepage">Homepage</div>
        <div id="trending">Coins</div>
        <div id="userpage">Userpage</div>
    </div>

    <div id="marketarea">
        <div id="loading">Loading user data...</div>
        <div id="buy" class="buy">
            <div class="buyvalues">
                <p name="dollar">USD</p>
                <p name="crypto">{symbol}</p>
                <input id="makebuy" name="inputfield" type="text" class="mktinput" placeholder="You buy">
                <input id="getbuy" name="inputfield" type="text" class="mktinput" placeholder="You get">
            </div>
            <input id="buybtn" type="button" class="mktbutton" value="Buy">
        </div>

        <div class="sell">
            <div class="buyvalues">
                <p name="crypto">{symbol}</p>
                <p name="dollar">USD</p>
                <input id="makesell" name="inputfield" type="text" class="mktinput" placeholder="You sell">
                <input id="getsell" name="inputfield" type="text" class="mktinput" placeholder="You get">
            </div>
            <input id="sellbtn" type="button" class="mktbutton" value="Sell">
        </div>
    </div>

</body>

<script>
    window.onload = async() => {{
        document.getElementById("buybtn").disabled = true
        document.getElementById("sellbtn").disabled = true

        await fetch("/is_authorized", {{
            method: "GET"
        }}).then(async res => {{
            res = await res.json();
            if (res.success === false) {{
                alert("you must be logged in");
                window.location.href = "/";
            }}
        }});

        document.getElementById("gotohomepage").onclick = () => {{
            window.location.href = "/"
        }}

        document.getElementById("trending").onclick = () => {{
            window.location.href = "/trending"
        }}

        document.getElementById("userpage").onclick = () => {{
            window.location.href = "/login"
        }}

        var crypto_info = await fetch("coins/single?symbol={symbol}", {{
            method: "GET"
        }}).then(async res => await res.json());

        var user_data = await fetch("/userdata", {{
            method: "POST",
            headers: {{
                "Content-Type": "application/json"
            }}
        }}).then(async res => {{
            res = await res.json();
            return res.data;
        }});

        if(user_data) {{
            document.getElementById("loading").remove();
            var makebuy = document.getElementById("makebuy");
            makebuy.oninput = () => {{
                value = Number(makebuy.value)
                if (value > 0) {{
                    document.getElementById("getbuy").value = value / crypto_info.market_data.current_price.usd;
                    document.getElementById("buybtn").disabled = value > user_data.dollar_balance
                }}
                if (value === "" || value == undefined || value === null || value === 0) {{
                    document.getElementById("getbuy").value = ""
                }}
            }};

            var makesell = document.getElementById("makesell");
            user_crypto = user_data.wallet.filter(c => c.symbol == crypto_info.symbol)[0];
            makesell.oninput = () => {{
                value = Number(makesell.value);
                if (value > 0) {{
                    document.getElementById("getsell").value = value * crypto_info.market_data.current_price.usd;
                    document.getElementById("sellbtn").disabled = value > user_crypto.balance;
                }}
                if (value === "" || value == undefined || value === null || value === 0) {{
                    document.getElementById("getsell").value = ""
                }}
            }};

            document.getElementById("sellbtn").onclick = async() => {{
                await fetch("/update_wallet", {{
                    method: "POST",
                    headers: {{
                        "Content-type": "application/json"
                    }},
                    body: JSON.stringify({{
                        "symbol": crypto_info.symbol,
                        "crypto_name": crypto_info.name,
                        "dollar_amount": Number(document.getElementById("getsell").value),
                        "crypto_amount": -Number(document.getElementById("makesell").value)
                    }})
                }}).then(async res => {{
                    res = await res.json();
                    alert(res.message);
                    document.getElementsByClassName("inputfield").forEach(e => {{
                        e.value = "";
                    }});
                    document.getElementById("sellbtn").disabled = true;
                    location.reload();
                    if (res.success === false) {{
                        window.location.href = "/";
                    }}
                }})
            }}

            document.getElementById("buybtn").onclick = async() => {{
                await fetch("/update_wallet", {{
                    method: "POST",
                    headers: {{
                        "Content-type": "application/json"
                    }},
                    body: JSON.stringify({{
                        "symbol": crypto_info.symbol,
                        "crypto_name": crypto_info.name,
                        "dollar_amount": -Number(document.getElementById("makebuy").value),
                        "crypto_amount": Number(document.getElementById("getbuy").value)
                    }})
                }}).then(async res => {{
                    res = await res.json();
                    alert(res.message);
                    document.getElementsByName("inputfield").forEach(e => {{
                        e.value = "";
                    }});
                    document.getElementById("makesell").value = "";
                    document.getElementById("buybtn").disabled = true;
                    location.reload();
                    if (res.success === false) {{
                        window.location.href = "/";
                    }}
                }})
            }}

            document.getElementsByName("dollar").forEach(e => {{
                e.textContent += " balance: $" + user_data.dollar_balance;
            }})

            document.getElementsByName("crypto").forEach(e => {{
                e.textContent += " balance: " + user_crypto.balance;
            }})
        }}
    }}
</script>

</html>

"""

"""
Le due funzioni che segueno sono le responsabili della generazione delle pagine
che dipendono dalla valuta selezionata dall'utente.
"""
def create_coin_info_page(symbol, coin_id):
    head = coin_info_head
    body = coin_info_body.format(coin_id=coin_id)
    script = coin_info_script.format(symbol=symbol, coin_id=coin_id)
    page = "<html>\n" + head+ body+ script + "</html>" 
    path = Path(coin_info_path)
    if path.exists():
        os.remove(coin_info_path)
    with open(coin_info_path, "w") as f:
       f.write(page)

def create_buy_sell_page(symbol):
    page = buy_sell_page.format(symbol=symbol)
    path = Path(buy_sell_path)
    if path.exists():
        os.remove(buy_sell_path)
    with open(buy_sell_path, "w") as f:
       f.write(page)
