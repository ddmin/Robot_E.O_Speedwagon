# /u/Robot_EO_Speedwagon
import robot_eo_speedwagon
import config
import praw
import time

# return a Reddit instance
def authenticate():
    reddit = praw.Reddit(
            username = config.username,
            password = config.password,
            client_id = config.client_id,
            client_secret = config.client_secret,
            user_agent = "ddmin's Robot E.O Speedwagon v1.0"
        )
    return reddit


# run the bot. Takes in a Reddit instance
def run_bot(reddit):
    TRIGGER = '!speedwagon'

    ids = get_ids()

    for comment in reddit.subreddit("test").comments(limit=None):

        if TRIGGER + ' ' in comment.body and comment.id not in ids:
            # Only look at words after !speedwagon
            s = comment.body.split()
            index = s.index(TRIGGER) + 1
            stand = ' '.join(s[index:])

            body = robot_eo_speedwagon.format_info(stand)

            print(f'Replying to {comment.id}')
            comment.reply(body)

            with open('replied_to.txt', 'a') as f:
                f.write(comment.id + '\n')


# return ids of comments that have been replied to
def get_ids():
    with open("replied_to.txt", "r") as f:
        ids = f.read().split('\n')

    return ids


def main():
    print("Authenticating Robot E.O Speedwagon...")
    reddit = authenticate()
    print("Authenticated!\n")

    while True:
        try:
            run_bot(reddit)
        except:
            print('An error has occurred. Sleeping for 10 seconds.')
            time.sleep(10)

if __name__ == '__main__':
    main()
