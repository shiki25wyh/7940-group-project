from telegram import Update,InlineKeyboardMarkup,InlineKeyboardButton,InputMediaPhoto
from telegram.ext import *
import configparser
import logging
from requests import *

import redis
import random
import os


global r
r = redis.StrictRedis(host=(os.environ['HOST']), password=(os.environ['PASSWORD']), port=(os.environ['REDISPORT']),decode_responses=True)


def main():
    # Load your token and create an Updater for your Bot

    updater = Updater(token=(os.environ['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher
    # You can set this logging module, so you will know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    
    
    
    
    
    dispatcher.add_handler(CommandHandler("start",startCommand))
    dispatcher.add_handler(CommandHandler("movie",movieCommand))
    dispatcher.add_handler(CallbackQueryHandler(queryHandler))
    dispatcher.add_handler(CommandHandler("write",writeCommand))
    dispatcher.add_handler(CommandHandler("read",readCommand))
    dispatcher.add_handler(CommandHandler("foodtype",foodtypeCommand))
    dispatcher.add_handler(CommandHandler("food",foodCommand))    
    dispatcher.add_handler(CommandHandler("sharefood",sharefoodCommand))  
    dispatcher.add_error_handler(error)    
    
    
    # To start the bot:
    updater.start_polling()
    updater.idle()

def startCommand(update,context):
     update.message.reply_text("Hello, I'm very glad to help you! I have two function.\nA READ and WRITE review for the movies!\n  /movie -randomly recommend you 10 movies\n  /write+movie id+YOUR COMMENT  -share your reviews.\n  /read+movie id -read movie's review\nB SHARE food video with your friends!\n  /foodtype -food type list\n        Western Food-we\n        Chinese Food-cn\n        Japanese Food-ja\n        French Cuisine-fr\n        Indian Cuisine-in\n        Thai Food-th\n  /sharefood+food type+url -share the food's video\n  /food+food type+id -search the food video your friends share to you")



def movieCommand(update,context):
    update.message.reply_text('Here is the movie list!')
    buttons=[]
    global m_id_list
    m_id_list=[]
#     global movies 
#     movies=[]
    for i in range(10):
        x,y = get_random_info() 
        movie_name = y['Movie_title']
        buttons.append([InlineKeyboardButton(movie_name,callback_data=x)])
        m_id_list.append(str(x))
    context.bot.send_message(chat_id=update.effective_chat.id,reply_markup = InlineKeyboardMarkup(buttons),text="pick the movie you may like!")
#     print (movies)

    
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
    

# cook vedio---------------------------------------------------------------------------------------------------------------------

    
def foodtypeCommand(update:Update,context:CallbackContext):
    m_id_list=[]
    update.message.reply_text('Here is the Foof list!')
    buttons=[[InlineKeyboardButton('Western Food',callback_data='we')],
            [InlineKeyboardButton('Chinese Food',callback_data='cn')],
            [InlineKeyboardButton('Janpanese Food',callback_data='ja')],
            [InlineKeyboardButton('French Cuisine',callback_data='fr')],
            [InlineKeyboardButton('Indian Cuisine',callback_data='in')],
             [InlineKeyboardButton('Thai Food',callback_data='th')]]


    context.bot.send_message(chat_id=update.effective_chat.id,reply_markup = InlineKeyboardMarkup(buttons),text="Choose your favorite kinds of food!")

    
    
def foodCommand(update:Update,context:CallbackContext):   
    
    
    f_info=context.args
    if len(f_info)>0:
        f_type = f_info[0].lower()
        
        if len(f_info)>1:
            f_id = f_info[1]
            if f_type == 'we':
                url = get_food('we',f_id)
                context.bot.send_message(chat_id=update.effective_chat.id,text=f'Western Food\n{url}',disable_web_page_preview=False)
            elif f_type == 'cn':
                url = get_food('cn',f_id)
                context.bot.send_message(chat_id=update.effective_chat.id,text=f'Chinese Food\n{url}',disable_web_page_preview=False)
            elif f_type == 'ja':
                url = get_food('ja',f_id)
                context.bot.send_message(chat_id=update.effective_chat.id,text=f'Janpanese Food\n{url}',disable_web_page_preview=False)
            elif f_type == 'fr':
                url = get_food('fr',f_id)
                context.bot.send_message(chat_id=update.effective_chat.id,text=f'French Cuisine\n{url}',disable_web_page_preview=False)
            elif f_type == 'in':
                url = get_food('in',f_id)
                context.bot.send_message(chat_id=update.effective_chat.id,text=f'Indian Cuisine\n{url}',disable_web_page_preview=False)
            elif f_type == 'th':
                url = get_food('th',f_id)
                context.bot.send_message(chat_id=update.effective_chat.id,text=f'Thai Food\n{url}',disable_web_page_preview=False)
                
            
       
            
            
        else:
            update.message.reply_text('Please enter food id.')
        
    else:
        update.message.reply_text('Please choose a kind of food.')
        
    
            
def sharefoodCommand(update:Update,context:CallbackContext):
    f_info=context.args
    if len(f_info)>0:
        f_type = f_info[0].lower()
        if f_type in ['we','cn','in','ja','fr','th']:
            if len(f_info)>1:
                url = f_info[1]
                if f_type in ['we','cn','in','ja','fr','th']:
                    r.rpush(f_type,url)
                    f_id = r.llen(f_type)-1
                    update.message.reply_text(f'Share food success, id:{f_id}\nPlease use /food+{f_type}+id to search the food.')
                else:
                    update.message.reply_text('Please enter the correct food type.')
            else:
                update.message.reply_text('Please enter URL you want to share.')
        else:
            update.message.reply_text('Please enter the correct food type.')

    else:
        update.message.reply_text('Please enter the type of food you want to share..')
    
    
    
def get_random_food(x):
    name = str(x)
    list_len=r.llen(name)-1
    i=random.randint(0,list_len)
    url=r.lindex(name, i)
    return url

def get_food(x,y):
    name = str(x)
    url=r.lindex(name, y)
    return url   
    
    
# query----------------------------------------------------------------------------------------    
    
    
def queryHandler(update,context):

    query_data = update.callback_query.data
    

#     print(movies)
    #     query_id = update.callback_query.id

    #     print(update.effective_chat.id)

    #     update.message.reply_text("hello")
    if query_data in m_id_list:
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
    
    
    
    
    elif query_data in ['we']:
        url = get_random_food('we')
        context.bot.send_message(chat_id=update.effective_chat.id,text=f'Western Food\n{url}',disable_web_page_preview=False)
        
        
    elif query_data in ['cn']:
        url = get_random_food('cn')
        context.bot.send_message(chat_id=update.effective_chat.id,text=f'Chinese Food\n{url}',disable_web_page_preview=False)

        
    elif query_data in ['ja']:
        url = get_random_food('ja')
        context.bot.send_message(chat_id=update.effective_chat.id,text=f'Japanese Food\n{url}',disable_web_page_preview=False)
        
    elif query_data in ['fr']:
        url = get_random_food('fr')
        context.bot.send_message(chat_id=update.effective_chat.id,text=f'French Cuisine\n{url}',disable_web_page_preview=False)

    elif query_data in ['in']:
        url = get_random_food('in')
        context.bot.send_message(chat_id=update.effective_chat.id,text=f'Indian Cuisine Food\n{url}',disable_web_page_preview=False)
        

    elif query_data in ['th']:
        url = get_random_food('th')    
        context.bot.send_message(chat_id=update.effective_chat.id,text=f'Thai Food\n{url}',disable_web_page_preview=False)

   
    elif query_data in 'w_r':
        context.bot.sendMessage(chat_id=update.effective_chat.id,text=f"Use /write or /read + {movie_id} to write/read the review for {title}.")



    
    

    
def error(update,context):
    print(f"Update{update} caused error {context.error}")
    
    
    







if __name__ == '__main__':
    main()