from Bot import RedditBot

# The reddit-accounts.csv file should be formatted as follows:
# username:password:email
# You log in to Reddit using the username, not the email
with open('reddit-accounts.txt', 'r') as accounts:
    info = accounts.readline().split(':')
    username = info[2]
    password = info[1]

bot = RedditBot()
bot.username = username
bot.password = password
bot.login()
# Do more stuff here