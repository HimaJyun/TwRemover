import twitter
import argparse
import os
import re
import json

api: twitter.Api = None


def unlike_all(data: os.PathLike, run: bool):
    like = []
    with open(os.path.join(data, "like.js"), mode="r", encoding="utf-8") as f:
        s = f.read().replace("window.YTD.like.part0 = ", "")
        like = json.loads(s)
        print(f"target likes: {len(like)}")
    for l in like:
        tid = l["like"]["tweetId"]
        print(f"unlike: {tid}")
        if run:
            try:
                api.DestroyFavorite(status_id=int(tid))
            except twitter.TwitterError as e:
                print(f"error: {e.message}")


def remove_tweet(data: os.PathLike, keep: set, run: bool):
    tweet = []
    with open(os.path.join(data, "tweet.js"), mode="r", encoding="utf-8") as f:
        s = f.read().replace("window.YTD.tweet.part0 = ", "")
        tweet = json.loads(s)
        print(f"target tweets: {len(tweet)}")
    for t in tweet:
        tid = t["tweet"]["id"]
        if tid in keep:
            print(f"skip: {tid}")
            continue
        print(f"remove: {tid}")
        if run:
            try:
                api.DestroyStatus(status_id=int(tid))
            except twitter.TwitterError as e:
                print(f"error: {e.message}")


def keep_list(path: os.PathLike) -> set:
    p = re.compile(
        r"^(?:https?://(?:.*?)\.?twitter\.com/(?:.+?)?/status/)?([0-9]+)[?/]?(?:.*)$"
    )
    r = set()
    with open(path, mode="r") as f:
        for line in f:
            m = p.match(line)
            if m:
                r.add(m.group(1))
    return r


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--consumer-key", required=True, type=str)
    parser.add_argument("--consumer-secret", required=True, type=str)
    parser.add_argument("--token-key", required=True, type=str)
    parser.add_argument("--token-secret", required=True, type=str)
    parser.add_argument("-d",
                        "--data",
                        type=str,
                        metavar="./data",
                        required=True,
                        help="Twitter data directory")
    parser.add_argument("-t",
                        "--remove-tweet",
                        action="store_true",
                        help="remove all tweets")
    parser.add_argument("-l",
                        "--remove-like",
                        action="store_true",
                        help="remove all likes")
    parser.add_argument("-k",
                        "--keep-list",
                        type=str,
                        metavar="./keep.txt",
                        help="keep tweet list")
    parser.add_argument(
        "--summer-bugs-entering-the-fire",
        action="store_true",
        help="If specified, the operation will be executed." +
        " I'm aware of all the risks and I'm ready not to regret if I make a mistake."
    )
    args = parser.parse_args()

    run = args.summer_bugs_entering_the_fire
    if run:
        global api
        api = twitter.Api(consumer_key=args.consumer_key,
                          consumer_secret=args.consumer_secret,
                          access_token_key=args.token_key,
                          access_token_secret=args.token_secret,
                          sleep_on_rate_limit=True)

    keep = set()
    if args.keep_list is not None:
        keep = keep_list(args.keep_list)
        print(f"keep: {keep}")

    if args.remove_tweet:
        remove_tweet(args.data, keep, run)
    if args.remove_like:
        unlike_all(args.data, run)


if __name__ == "__main__":
    main()
