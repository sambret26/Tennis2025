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
    for message in messages:
        await channel.send(message.message)
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
        for message in messagesInCategory:
            await channel.send(message.message)
            messageIdToDelete.append(message.id)
    messageRepository.deleteMessagesByIds(messageIdToDelete)