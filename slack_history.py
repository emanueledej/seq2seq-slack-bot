from slacker import Slacker
import argparse

def getHistory(pageableObject, channelId, pageSize = 100):
  messages = []
  lastTimestamp = None

  while(True):
    response = pageableObject.history(
      channel = channelId,
      latest  = lastTimestamp,
      oldest  = 0,
      count   = pageSize
    ).body

    messages.extend(response['messages'])

    if (response['has_more'] == True):
      lastTimestamp = messages[-1]['ts'] # -1 means last element in a list
    else:
      break
  return messages

#fetch and write history for all public channels
def getChannels(slack):
  messages = []
  channels = slack.channels.list().body['channels']
  
  print("\nfound channels: ")
  for channel in channels:
    print(channel['name'])
  
    messages.append(getHistory(slack.channels, channel['id']))
    channelInfo = slack.channels.info(channel['id']).body['channel']
  return messages

def doTestAuth(slack):
  testAuth = slack.auth.test().body
  teamName = testAuth['team']
  currentUser = testAuth['user']
  print("Successfully authenticated for team {0} and user {1} ".format(teamName, currentUser))
  return testAuth

def getChannelsMessage(token):
  slack = Slacker(token)

  testAuth = doTestAuth(slack)

  return getChannels(slack)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='download slack history')
  parser.add_argument('--token', help="an api token for a slack user")
  args = parser.parse_args()
  getChannelsMessage(args.token)