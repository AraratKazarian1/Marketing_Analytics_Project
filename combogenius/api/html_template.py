def generate_html_template(combos, discount, custom_html):
    combos_html = ""
    for combo in combos:
        combo_html = f"""
        <div class="combo">
            <h2>{combo['name']}</h2>
            <p>Price: ${combo['price']}</p>
            <p>Get {discount}% off on this combo!</p>
            <p class="discount">Use code: COMBO{combo['code']}</p>
        </div>
        """
        combos_html += combo_html

    if custom_html:
        html_content = custom_html
    else:
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>New Combo Offer!</title>
            <style>
                /* CSS Styles */
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #ffffff;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }}
                .header {{
                    background-color: orange;
                    color: #ffffff;
                    padding: 20px;
                    border-top-left-radius: 10px;
                    border-top-right-radius: 10px;
                    text-align: center;
                }}
                .content {{
                    padding: 20px;
                }}
                .combo {{
                    margin-bottom: 20px;
                    padding: 10px;
                    background-color: yellow;
                    border-radius: 5px;
                }}
                .combo h2 {{
                    margin-top: 0;
                }}
                .discount {{
                    font-weight: bold;
                    color: red;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>New Combo Offer!</h1>
                </div>
                <div class="content">
                    {combos_html}
                </div>
                <div class="footer">
                    <p>This offer is valid for a limited time only. Visit us today!</p>
                </div>
            </div>
        </body>
        </html>
        """
    return html_content