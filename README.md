# TwRemover

usage

```bash
./run.sh --consumer-key "CONSUMER_KEY" \
  --consumer-secret "CONSUMER_SECRET" \
  --token-key "ACCESS_TOKEN_KEY" \
  --token-secret "ACCESS_TOKEN_SECRET" \
  --remove-tweet --remove-like \
  --data ./twitter/data --keep ./keep.txt \
  | tee log.txt
```

keep list

```txt
https://twitter.com/yourname/status/1/
https://twitter.com/yourname/status/2/
3
4
```
