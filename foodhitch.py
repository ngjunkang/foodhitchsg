#!/usr/bin/env python
# coding: utf-8

import logging

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

DEAL_TYPE, DELIVERY_REGION, PURCHASE_REGION, CUT_OFF_TIME, DELIVERY_FEE, DELIVERY_ADDRESS, PURCHASE_LOCATION, STORE_NAME, FOOD_DETAILS, FEE, ARR_TIME, CONFIRMATION, FEEDBACK = range(13)

def start(update, context):
    reply_keyboard = [['Buy', 'Deliver']]

    update.message.reply_text(
        'Hi! Welcome to SG Food Hitch. I will be taking your order. '
        'Send /cancel to stop talking to me.\n\n'
        'Do you want to buy or deliver?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return DEAL_TYPE 

def deal_type(update, context):
    text = update.message.text
    context.user_data['deal_type'] = text 
    if text == 'Buy': 
        update.message.reply_text('Please enter the delivery address \n(The address at which you want your food to be delivered to):')
    else: 
        update.message.reply_text('Please enter the delivery region \n(The area you would like to deliver to):')

        
    return DELIVERY_ADDRESS if text == 'Buy' else DELIVERY_REGION

def delivery_region(update, context):
    text = update.message.text
    context.user_data['delivery_region'] = text 
    update.message.reply_text('Please enter the purchase region \n(The area you are purchasing food from):')

    return PURCHASE_REGION

def purchase_region(update, context):
    text = update.message.text
    context.user_data['purchase_region'] = text 
    update.message.reply_text('Please enter cut-off timing \n(The time at which you will stop accepting any more delivery requests):')

    return CUT_OFF_TIME

def cut_off_time(update, context):
    text = update.message.text
    context.user_data['cut_off_time'] = text
    update.message.reply_text('Please enter the delivery fee that you would want to receive to fulfil an order:')

    return DELIVERY_FEE

def delivery_fee(update,context):
    text = update.message.text
    context.user_data['delivery_fee'] = text
    summary_2 = "Deal Type: {0}\nDelivery Region: {1}\nPurchase Region: {2}\nCut-off Time: {3}\nDelivery Fee: {4}".format(str(context.user_data['deal_type']),
                                                                                                                          str(context.user_data['delivery_region']),
                                                                                                                          str(context.user_data['purchase_region']),
                                                                                                                          str(context.user_data['cut_off_time']),
                                                                                                                          str(context.user_data['delivery_fee']))
    reply_keyboard = [['Yes', 'No']]
    update.message.reply_text('Thank you.' + '\n' + summary_2 + '\n' + 'Confirm order? (y/n)', parse_mode='HTML',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return CONFIRMATION

def confirmation(update, context):
    text = update.message.text.lower()
    context.user_data['confirmation'] = text
    text2 = context.user_data['deal_type']
    userid = update.message.from_user['id']
    first_name = update.message.from_user['first_name']
    if (text == 'yes' or text == 'y') and text2 == 'Deliver': 
        summary_1 = "Deal Type: {0}\nDelivery Region: {1}\nPurchase Region: {2}\nCut off time: {3}\nDelivery Fee: {4}\nContact: {5}\n\nCreate a request via @foodhitchsgbot".format(str(context.user_data['deal_type']),
                                                                                                                               str(context.user_data['delivery_region']),
                                                                                                                               str(context.user_data['purchase_region']),
                                                                                                                               str(context.user_data['cut_off_time']),
                                                                                                                               str(context.user_data['delivery_fee']),
                                                                                                                               '<a href="tg://user?id=' + str(userid) + '">'+ str(first_name) + '</a>')
        sent = context.bot.send_message(chat_id='@FOODHITCHSG', text = summary_1, parse_mode='HTML')
        context.user_data['message_id'] = sent['message_id']
        context.user_data['message'] = sent['text']
    elif (text == 'yes' or text == 'y') and text2 == 'Buy':
        summary_2 = "Deal Type: {0}\nDelivery Address: {1}\nPurchase Location: {2}\nStore Name: {3}\nFood Details: {4}\nFee: {5}\nArrival Time: {6}\nContact: {7}\n\nCreate a request via @foodhitchsgbot".format(str(context.user_data['deal_type']),
                                                                                                                                                   str(context.user_data['delivery_address']),
                                                                                                                                                   str(context.user_data['purchase_location']),
                                                                                                                                                   str(context.user_data['store_name']),
                                                                                                                                                   str(context.user_data['food_details']),
                                                                                                                                                   str(context.user_data['fee']),
                                                                                                                                                   str(context.user_data['arr_time']),
                                                                                                                                                   '<a href="tg://user?id=' + str(userid) + '">'+ str(first_name) + '</a>')
        sent = context.bot.send_message(chat_id='@FOODHITCHSG', text = summary_2, parse_mode='HTML')
        context.user_data['message_id'] = sent['message_id']
        context.user_data['message'] = sent['text']
    else:
        update.message.reply_text('Ok your order is cancelled.')
        
    return ConversationHandler.END
        
def delivery_address(update, context):
    text = update.message.text
    context.user_data['delivery_address'] = text
    update.message.reply_text('Please enter purchase location \n(Location of the food that you want to purchase from):')
    return PURCHASE_LOCATION

def purchase_location(update, context):
    text = update.message.text
    context.user_data['purchase_location'] = text
    update.message.reply_text('Please enter store name \n(The stall to buy your food from):')

    return STORE_NAME

def store_name(update, context):
    text = update.message.text
    context.user_data['store_name'] = text
    update.message.reply_text('Please enter food details \n(Basic description of the items you want to purchase):')

    return FOOD_DETAILS

def food_details(update, context):
    text = update.message.text
    context.user_data['food_details'] = text
    update.message.reply_text('Please enter proposed service fee \n(Fees that you are willing to pay as an incentive for people to fulfill your order):')

    return FEE

def fee(update, context):
    text = update.message.text
    context.user_data['fee'] = text
    update.message.reply_text('Please enter time to arrive by \n(The time at which you want your food to arrive by):')

    return ARR_TIME

def arr_time(update, context):
    text = update.message.text
    context.user_data['arr_time'] = text
    userid = update.message.from_user['id']
    first_name = update.message.from_user['first_name']
    summary_2 = "Deal Type: {0}\nDelivery Address: {1}\nPurchase Location: {2}\nStore Name: {3}\nFood Details: {4}\nFee: {5}\nArrival Time: {6}\nContact: {7}\n".format(str(context.user_data['deal_type']),
                                                                                                                                                   str(context.user_data['delivery_address']),
                                                                                                                                                   str(context.user_data['purchase_location']),
                                                                                                                                                   str(context.user_data['store_name']),
                                                                                                                                                   str(context.user_data['food_details']),
                                                                                                                                                   str(context.user_data['fee']),
                                                                                                                                                   str(context.user_data['arr_time']),
                                                                                                                                                   '<a href="tg://user?id=' + str(userid) + '">'+ str(first_name) + '</a>')
    reply_keyboard = [['Yes', 'No']]
    update.message.reply_text('Thank you.' + '\n' + summary_2 + '\n' + 'Confirm order? (y/n)', parse_mode='HTML',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return CONFIRMATION

def timeout(update,context):
    update.message.reply_text('Session has timed out')

    return ConversationHandler.END

def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def delete(update, context):
    if 'message_id' in context.user_data:
        if context.user_data['message_id'] != "":
            text = context.user_data['message']
            message_id = context.user_data['message_id']
            context.bot.edit_message_text(chat_id='@FOODHITCHSG', message_id=message_id, text = text+"\n===Deal Deleted===")
            update.message.reply_text('Ok your order is deleted.')
        else:
            update.message.reply_text('No order......')
    else:
        update.message.reply_text('No order......')
    return ConversationHandler.END

def feedback_query(update, context):
    update.message.reply_text('Please share your feedback with us so that we can improve to serve you better')

    return FEEDBACK

def feedback(update, context):
    userid = update.message.from_user['id']
    first_name = update.message.from_user['first_name']
    text = update.message.text
    context.bot.send_message(chat_id='-1001152411909', text='Feedback by {0}\n\n{1}'.format('<a href="tg://user?id=' + str(userid) + '">'+ str(first_name) + '</a>', text), parse_mode='HTML')
    update.message.reply_text('Thank you for your feedback. Bye!',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater('1236316190:AAGUjo7jeCp8d5dQrt2TFQa1Jfz6PpNxvT0', use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),CommandHandler('delete',delete),CommandHandler('feedback',feedback_query)],

        states={
            DEAL_TYPE: [CommandHandler('cancel', cancel),
                        MessageHandler(Filters.regex('^(Buy|Deliver$)'),
                                      deal_type),
                       ],

            DELIVERY_REGION: [CommandHandler('cancel', cancel),
                              MessageHandler(Filters.text,
                                           delivery_region)
                            ],
            PURCHASE_REGION: [CommandHandler('cancel', cancel),
                              MessageHandler(Filters.text,
                                           purchase_region)
                            ],
            CUT_OFF_TIME: [CommandHandler('cancel', cancel),
                           MessageHandler(Filters.text,
                                           cut_off_time)
                            ],
            DELIVERY_FEE: [CommandHandler('cancel', cancel),
                           MessageHandler(Filters.text,
                                           delivery_fee)
                            ],
            DELIVERY_ADDRESS: [ CommandHandler('cancel', cancel),
                               MessageHandler(Filters.text,
                                           delivery_address)
                            ],
            PURCHASE_LOCATION: [CommandHandler('cancel', cancel),
                                MessageHandler(Filters.text,
                                           purchase_location)
                            ],
            STORE_NAME: [CommandHandler('cancel', cancel),
                         MessageHandler(Filters.text,
                                           store_name)
                            ],
            FOOD_DETAILS: [CommandHandler('cancel', cancel),
                           MessageHandler(Filters.text,
                                           food_details)
                            ],
            FEE: [CommandHandler('cancel', cancel),
                  MessageHandler(Filters.text,
                                           fee)
                            ],
            ARR_TIME: [CommandHandler('cancel', cancel),
                       MessageHandler(Filters.text,
                                           arr_time)
                            ],
            CONFIRMATION: [CommandHandler('cancel', cancel),
                           MessageHandler(Filters.regex('^(Yes|No|yes|no|y|n)$'),
                                      confirmation)
                            ],
            FEEDBACK: [CommandHandler('cancel', cancel),
                       MessageHandler(Filters.text,
                                           feedback)
                            ],
            ConversationHandler.TIMEOUT: [MessageHandler(Filters.text, timeout)],
        },
        conversation_timeout = 180,
        fallbacks=[]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
