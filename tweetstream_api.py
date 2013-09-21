import tweetstream

stream = tweetstream.SampleStream("hypewizard", "74438100")
for tweet in stream:
    print tweet
