
from telegram import Update,InlineKeyboardMarkup,InlineKeyboardButton,InputMediaPhoto
from telegram.ext import *
import configparser
import logging
from requests import *

import redis
import random



global r
r = redis.StrictRedis(host='redis-11170.c8.us-east-1-3.ec2.cloud.redislabs.com', password='dZleUg0YWWO1a1zSBGoTGfQrf6tm1vnQ', port=11170,decode_responses=True)


def main():
    # Load your token and create an Updater for your Bot

    updater = Updater(token='5326785904:AAH6V2Gr2n94Pbmd6U29lRQA85PFyBmlqsM', use_context=True)
    dispatcher = updater.dispatcher
    # You can set this logging module, so you will know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    
    
    
    
    
    
    dispatcher.add_handler(CommandHandler("start",startCommand))
    
    dispatcher.add_handler(CallbackQueryHandler(queryHandler))

    dispatcher.add_handler(CommandHandler("write",writeCommand))
#     dispatcher.add_error_handler(error)

    dispatcher.add_handler(CommandHandler("read",readCommand))

    # To start the bot:
    updater.start_polling()
    updater.idle()






def startCommand(update,context):
    update.message.reply_text('Here is the movie list!')
    buttons=[]
#     global movies 
#     movies=[]
    for i in range(10):
        x,y = get_random_info() 
        movie_name = y['Movie_title']
        buttons.append([InlineKeyboardButton(movie_name,callback_data=x)])
#         movies.append(x)
    context.bot.send_message(chat_id=update.effective_chat.id,reply_markup = InlineKeyboardMarkup(buttons),text="pick the movie you may like!")
#     print (movies)




def queryHandler(update,context):

    query_data = update.callback_query.data
    print(query_data)
#     print(movies)
    #     query_id = update.callback_query.id

    #     print(update.effective_chat.id)

    #     update.message.reply_text("hello")
    if query_data not in "w_r":
        global movie_id
        global title
        movie_id = query_data
        movie_info = get_movie_info(query_data)
        title = movie_info['Movie_title']
        year = movie_info['Year']
        actor = movie_info['Star1']+'/'+movie_info['Star2']+'/'+movie_info['Star3']+'/'+movie_info['Star4']
        certificate = movie_info['Certificate']
        rating = movie_info['Rating']
        URL = movie_info['URL']
        time = movie_info['Time']
        overview = movie_info['Overview']
        genre = movie_info['Genre']

        image=get(URL).content
        context.bot.sendMediaGroup(chat_id=update.effective_chat.id,media=[InputMediaPhoto(image)])
    #     context.bot.sendPhoto(chat_id=update.effective_chat.id,photo=image)
        buttons = [[InlineKeyboardButton("Read/Write Review",callback_data="w_r")]]
        context.bot.sendMessage(chat_id=update.effective_chat.id,reply_markup = InlineKeyboardMarkup(buttons),text=f'Title:{title}\nActor:{actor}\nRating:{rating}\nCertificate:{certificate}\nTime:{time}\nRelease Year:{year}\nGenre:{genre}\nOverview:{overview}')

    #     context.bot.send_message(chat_id=update.effective_chat.id,text="/reply")

    #     context.bot.send_message(chat_id=update.effective_chat.id,reply_markup = InlineKeyboardMarkup(buttons),text="pick the movie you may like!")
    else:
        context.bot.sendMessage(chat_id=update.effective_chat.id,text=f"Use /write or /read + {movie_id} to write/read the review for {title}.")










    
def writeCommand(update:Update,context:CallbackContext):
    m_info=context.args
    if len(m_info)>0:
        m_id=m_info[0]
        if len(m_info)>1:
            m_title=r.hget(m_id,"Movie_title")
            msg=" ".join(m_info[1:])
            r.rpush(m_title,msg)
            update.message.reply_text("Success comment")
        else:
            update.message.reply_text("Please write some comment")
    else:
         update.message.reply_text("Please select a movie")


def readCommand(update:Update,context:CallbackContext):
    m_info=context.args
    m_id=m_info[0]
    m_title=r.hget(m_id,"Movie_title")
    m_review=r.lrange(m_title,0,10)
    if len(m_review)>0:
        msg="\n".join(m_review)
        update.message.reply_text(msg)
    elif len(m_review)==0:
        update.message.reply_text("This movie has no comment.")
    
    


    
# def reviewCommand(update:Update,context:CallbackContex):
    
    
    
    
def get_random_info():
    global r
    i=random.randint(0,999)
    movie_info = r.hgetall(i)
    return i,movie_info

def get_movie_info(x):
    global r
    movie_info = r.hgetall(x)
    return movie_info
    
    
    

# def error(update,context):
#     print(f"Update{update} caused error {context.error}")
    











if __name__ == '__main__':
    main()