from repositories.CategoryRepository import CategoryRepository
from repositories.MessageRepository import MessageRepository
from repositories.ChannelRepository import ChannelRepository

categoryRepository = CategoryRepository()
messageRepository = MessageRepository()
channelRepository = ChannelRepository()

async def sendNotif(bot):
    await sendNotifByCategory(bot, "G")
    categories = categoryRepository.getAllCategories()
    for category in categories:
        await sendNotifByCategory(bot, category.code)
    await sendOtherNotif(bot)

async def sendNotifByCategory(bot, categoryCode): 
    channelId = channelRepository.getLogChannelId(categoryCode)
    messages = messageRepository.getMessagesByCategory(categoryCode)
    channel = bot.get_channel(channelId)
    for i in range(0, len(messages), 20):
        message = '\n'.join([m.message for m in messages[i:i+20]])
        await channel.send(message)
    messageRepository.deleteMessagesByCategory(categoryCode)

async def sendOtherNotif(bot):
    messages = messageRepository.getAllMessages()
    messagesByCategory = {}
    for message in messages:
        if message.category not in messagesByCategory:
            messagesByCategory[message.category] = []
        messagesByCategory[message.category].append(message)
    messageIdToDelete = []
    for category, messagesInCategory in messagesByCategory.items():
        channelId = channelRepository.getLogChannelId(category)
        channel = bot.get_channel(channelId)
        for i in range(0, len(messagesInCategory), 20):
            message = '\n'.join([m.message for m in messagesInCategory[i:i+20]])
            await channel.send(message)
        messageIdToDelete.extend([m.id for m in messagesInCategory])
    messageRepository.deleteMessagesByIds(messageIdToDelete)