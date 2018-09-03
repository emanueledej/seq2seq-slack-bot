from slacker import Slacker

#fetch and write history for all public channels
def getChannels(slack):
  channels = slack.channels.list().body['channels']
  
  print("\nfound channels: ")
  for channel in channels:
    print(channel['name'])
  
    messages = getHistory(slack.channels, channel['id'])
    channelInfo = slack.channels.info(channel['id']).body['channel']

return channelInfo, messages
    