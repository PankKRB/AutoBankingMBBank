import discord
from discord.ext import commands
import requests
import asyncio
import random
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
def load_sent_transactions(filename='sent_transactions.txt'):
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []
def save_sent_transactions(sent_transactions, filename='sent_transactions.txt'):
    with open(filename, 'w') as file:
        for transaction_id in sent_transactions:
            file.write(transaction_id + '\n')
sent_transactions = load_sent_transactions()
@bot.command()
async def naptien(ctx):
    # Lấy thông tin người dùng Discord thực hiện lệnh
    user_id = ctx.author.id
    
    # Tạo URL với thông tin người dùng
    url = f"https://img.vietqr.io/image/mbbank-(#thay-stk-vao-day)-qr_only.jpg?addInfo=naptien{user_id}&accountName=naptien{user_id}"
    
    # Tạo một embed với ảnh từ URL
    embed = discord.Embed(title="Nạp Tiền", description=f"Ảnh nạp tiền từ URL", color=0x00ff00)
    embed.set_image(url=url)
    
    # Gửi embed vào kênh
    await ctx.send(embed=embed)
async def xulygiaodich():
    # thay thông tin ngân hàng vào đây
    url = 'https://krbs.fun/?phone=xxxxxxxxx&pass=xxxxxxxxx&stk=xxxxxxxxx'

    while True:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            if data is not None:
                try:
                    credit_transactions = []

                    for transaction in data.get('transactionHistoryList', []):
                        if float(transaction.get('creditAmount', '0')) != 0 and transaction['refNo'] not in sent_transactions:
                            credit_transactions.append(transaction)
                            sent_transactions.append(transaction['refNo'])

                    if len(credit_transactions) == 0:
                        print("Không có giao dịch nào trong 2 phút gần đây.")
        
                    for transaction in credit_transactions:
                        sender_name = transaction.get('benAccountName', 'Unknown')
                        amount = transaction.get('creditAmount', 0)
                        content = transaction.get('description', 'No description')
                        
                        # Kiểm tra nếu nội dung chuyển tiền có dạng naptien<mã số>
                        if content.startswith('naptien'):
                            # Tách lấy mã số từ nội dung
                            user_id = content[len('naptien'):]
                            # Gửi tin nhắn vào kênh văn bản cụ thể

                            #phần xử lý giao dịch khi hoàn thành
                            channel = bot.get_channel(1207714583259910214)
                            await channel.send(f"<@{user_id}> đã nạp {amount}")
                            
                        # In thông tin giao dịch vào log
                        print(f"Người gửi: {sender_name}, Số tiền: {amount}, Nội dung: {content}")

                except ValueError as e:
                    print("Response was not valid JSON:", e)
            
            else:
                print("Không có dữ liệu giao dịch trong 2 phút gần đây.")
        
        else:
            print("Failed to retrieve data")
        save_sent_transactions(sent_transactions)
        # thời gian check lịch sử giao dịch
        await asyncio.sleep(120)

@bot.event
async def on_ready():
    print('Bot is ready!')
    bot.loop.create_task(xulygiaodich())
# Kết nối bot với Discord
bot.run('XXXXXX')
